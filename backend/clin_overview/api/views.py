from rest_framework import viewsets

from .serializers import ClinicalDataSerializer, TimelineRecordSerializer
from ..models import ClinicalData, TimelineRecord
import simplejson
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Max, Min
import numpy as np
import pandas as pd


class ClinicalViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the clinical data of the patients. Provides
    `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    serializer_class = ClinicalDataSerializer
    queryset = ClinicalData.objects.all()

    def retrieve(self, request, pk=None):

        serializer_class = ClinicalDataSerializer
        queryset = ClinicalData.objects.all()
        patient = get_object_or_404(queryset, pk=pk)
        timelinerecords = TimelineRecord.objects.filter(patient=patient, event="laboratory")
        date_relative_max = timelinerecords.aggregate(Max("date_relative"))['date_relative__max']
        date_relative_min = timelinerecords.aggregate(Min("date_relative"))['date_relative__min']
        ca125 = timelinerecords.filter(name="ca125").order_by("date_relative")
        hb = timelinerecords.filter(name="hb").order_by("date_relative")
        neut = timelinerecords.filter(name="neut").order_by("date_relative")
        leuk = timelinerecords.filter(name="leuk").order_by("date_relative")
        platelets = timelinerecords.filter(name="platelets").order_by("date_relative")

        thresholds = {
                        'ca125':        [0, 35],
                        'leuk':         [3.4, 8.2],
                        'platelets':    [150, 360],
                        'hb':           [117, 155],
                        'neut':         [1.5, 6.7],
                }

        colors = {
                        'ca125':        [
                                            "rgba(54, 150, 165, 1)",
                                            "rgba(255, 255, 255, 1)",
                                            "rgba(0, 242, 255, 1)",
                                        ],
                        'leuk':         [
                                            "rgba(165, 121, 54, 1)",
                                            "rgba(255, 255, 255, 1)",
                                            "rgba(255, 123, 0,1)",
                                        ],
                        'platelets':    [
                                            "rgba(165, 121, 54, 1)",
                                            "rgba(255, 255, 255, 1)",
                                            "rgba(255, 123, 0,1)",
                                        ],
                        'hb':           [
                                            "rgba(165, 54, 134, 1)",
                                            "rgba(255, 255, 255, 1)",
                                            "rgba(255, 0, 106, 1)",
                                        ],
                        'neut':         [
                                            "rgba(165, 54, 134, 1)",
                                            "rgba(255, 255, 255, 1)",
                                            "rgba(255, 0, 106, 1)",
                                        ],
                }

        def add_data(data, range_min, range_max, thresholds, colors):
            date_relative = np.arange(range_min, range_max + 1)
            result        = np.empty_like(date_relative, dtype=np.float32)
            result[:]     = np.nan
            for item in data.iterator():
                result[item.date_relative-range_min] = item.result
            newdict = {'y': result.tolist(),
                       'x': date_relative.tolist(),
                       'colors': colors,
                       'thresholds': thresholds,
                      }
            return newdict

        ca125_dict     = add_data(ca125,       date_relative_min, date_relative_max, thresholds["ca125"], colors["ca125"])
        hb_dict        = add_data(hb,          date_relative_min, date_relative_max, thresholds["hb"], colors["hb"])
        leuk_dict      = add_data(leuk,        date_relative_min, date_relative_max, thresholds["leuk"], colors["leuk"])
        platelets_dict = add_data(platelets,   date_relative_min, date_relative_max, thresholds["platelets"], colors["platelets"])
        neut_dict      = add_data(neut,        date_relative_min, date_relative_max, thresholds["neut"], colors["neut"])

        time_series = {
            'ca125': ca125_dict,
            'hb': hb_dict,
            'leuk': leuk_dict,
            'platelets': platelets_dict,
            'neut' : neut_dict,
        }

        patient.time_series = simplejson.dumps(time_series, ignore_nan=True)
        # patient.bmi = patient.weight/(patient.height**2)
        return Response(serializer_class(patient).data)

    # def retrieve(self, request, pk=None):
    #     serializer_class = ClinicalDataSerializer
    #     if pk == None:
    #         queryset = ClinicalData.objects.all()
    #         return Response(serializer_class(queryset))
    #     else:
    #         patient = ClinicalData.objects.filter(pk=pk)
    #         queryset = TimelineRecord.objects.filter(patient_id=pk, event="laboratory")
    #         ca125 = queryset.filter(name="ca125").order_by("date_relative")
    #         hb = queryset.filter(name="hb").order_by("date_relative")
    #         leuk = queryset.filter(name="leuk").order_by("date_relative")
    #         platelets = queryset.filter(name="platelets").order_by("date_relative")
    #
    #         ca125_dict = {'result':         [c.result for c in list(ca125)],
    #                       'date_relative':  [c.date_relative for c in list(ca125)]}
    #         hb_dict = {'result':         [c.result for c in list(hb)],
    #                       'date_relative':  [c.date_relative for c in list(hb)]}
    #         leuk_dict = {'result':         [c.result for c in list(leuk)],
    #                       'date_relative':  [c.date_relative for c in list(leuk)]}
    #         platelets_dict = {'result':         [c.result for c in list(platelets)],
    #                       'date_relative':  [c.date_relative for c in list(platelets)]}
    #
    #         time_series =   {
    #                             'ca125'     :ca125_dict,
    #                             'hb'        : hb_dict,
    #                             'leuk'      : leuk_dict,
    #                             'platelets' : platelets_dict,
    #                         }
    #
    #         patient.time_series = time_series
    #         # serializer = UserSerializer(user)
    #         return Response(serializer_class(patient))

class TimelineViewSet(viewsets.ModelViewSet): # id paziente
    """
    API endpoint for the clinical data of the patients. Provides
    `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """

    queryset = TimelineRecord.objects.all()
    serializer_class = TimelineRecordSerializer

    def retrieve(self, request, patient_id=None):
        queryset = TimelineRecord.objects.filter(patient_id=patient_id, event="laboratory")
        ca125 = queryset.filter(name="ca125").order_by("date_relative")
        hb = queryset.filter(name="hb").order_by("date_relative")
        leuk = queryset.filter(name="leuk").order_by("date_relative")
        platelets = queryset.filter(name="platelets").order_by("date_relative")

        ca125_dict = {'result':         [c.result for c in list(ca125)],
                      'date_relative':  [c.date_relative for c in list(ca125)]}
        hb_dict = {'result':         [c.result for c in list(hb)],
                      'date_relative':  [c.date_relative for c in list(hb)]}
        leuk_dict = {'result':         [c.result for c in list(leuk)],
                      'date_relative':  [c.date_relative for c in list(leuk)]}
        platelets_dict = {'result':         [c.result for c in list(platelets)],
                      'date_relative':  [c.date_relative for c in list(platelets)]}

        time_series =   {
                            'ca125'     :ca125_dict,
                            'hb'        : hb_dict,
                            'leuk'      : leuk_dict,
                            'platelets' : platelets_dict,
                        }

        # serializer = UserSerializer(user)
        return Response(simplejson.dump(time_series))

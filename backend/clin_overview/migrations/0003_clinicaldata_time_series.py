# Generated by Django 3.2.15 on 2022-09-15 14:27

import clin_overview.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clin_overview', '0002_alter_clinicaldata_cud_current_treatment_phase'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinicaldata',
            name='time_series',
            field=models.TextField(default=clin_overview.models.fetchTimeSeries),
        ),
    ]

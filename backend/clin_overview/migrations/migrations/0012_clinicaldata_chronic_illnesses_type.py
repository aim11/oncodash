# Generated by Django 3.2.16 on 2022-11-03 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clin_overview', '0011_auto_20221103_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinicaldata',
            name='chronic_illnesses_type',
            field=models.CharField(blank=True, choices=[('ASTMA', 'Asma'), ('ARTHRORISARTRITIS', 'Arthroris/artritis'), ('PARPI', 'Flimmer'), ('COPD', 'COPD'), ('COLITIS ULSEROSA', 'Colitis ulserosa'), ('DEPRESSION', 'Depression'), ('DIABETES TYPE2', 'Diabetes type2'), ('EPILEPSY', 'Epilepsy'), ('FIBROMYALGIA', 'Fibromyalgia'), ('GLAUCOMA', 'Glaucoma'), ('HYPERCHOLESTEROLEMIA', 'Hypercholesterolemia'), ('HYPERTENSION', 'Hypertension'), ('HYPOTHYREOSIS', 'Hypothyreosis'), ('MCC', 'MCC'), ('MYOCARDIAL INFARCT', 'Myocardial infarct'), ('OSTEOPOROSIS', 'Osteoporosis'), ('PULMONARY EMBO', 'Pulmonary Embo'), ('STROKE', 'Stroke'), ('REFLUX', 'Reflux'), ('RENAL INSUFFIENCY', 'Renal insuffiency'), ('REUMATOID ARTRITIS', 'Reumatoid artritis'), ('SCHITZOPHRENIA', 'Schitzophrenia'), ('VENOUS TROMB', 'Venous tromb'), ('OTHER', 'Other')], max_length=100),
        ),
    ]

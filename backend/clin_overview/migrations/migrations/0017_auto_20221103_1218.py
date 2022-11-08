# Generated by Django 3.2.16 on 2022-11-03 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clin_overview', '0016_auto_20221103_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinicaldata',
            name='platinum_free_interval_at_update',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='clinicaldata',
            name='followup_time',
            field=models.IntegerField(null=True),
        ),
    ]
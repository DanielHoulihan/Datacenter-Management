# Generated by Django 3.2.12 on 2022-02-07 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='data_center_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='endTime',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='pue',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='startTime',
            field=models.CharField(max_length=20, null=True),
        ),
    ]

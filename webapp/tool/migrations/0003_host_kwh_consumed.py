# Generated by Django 3.2.12 on 2022-03-19 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0002_hostenergy_kwh_consumed'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='kWh_consumed',
            field=models.FloatField(null=True),
        ),
    ]

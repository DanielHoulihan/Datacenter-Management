# Generated by Django 3.2.12 on 2022-03-26 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0005_auto_20220321_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostenergy',
            name='app_waste_cost_3',
            field=models.FloatField(null=True),
        ),
    ]
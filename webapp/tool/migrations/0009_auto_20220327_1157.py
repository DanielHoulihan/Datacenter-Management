# Generated by Django 3.2.12 on 2022-03-27 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0008_auto_20220327_1016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='carbon_used',
        ),
        migrations.RemoveField(
            model_name='budget',
            name='energy_used',
        ),
        migrations.AddField(
            model_name='budget',
            name='energy_dict',
            field=models.TextField(null=True),
        ),
    ]
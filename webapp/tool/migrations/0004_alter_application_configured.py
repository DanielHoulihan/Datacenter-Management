# Generated by Django 3.2.12 on 2022-03-31 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0003_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='configured',
            field=models.IntegerField(default=0, null=True),
        ),
    ]

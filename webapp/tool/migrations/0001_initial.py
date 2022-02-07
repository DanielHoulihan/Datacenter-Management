# Generated by Django 3.2.12 on 2022-02-07 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reportId', models.CharField(blank=True, max_length=75, null=True)),
                ('createDate', models.CharField(blank=True, max_length=75, null=True)),
                ('message', models.CharField(blank=True, max_length=75, null=True)),
                ('hosts', models.IntegerField(null=True)),
                ('racks', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HostReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostId', models.CharField(max_length=10)),
                ('hostName', models.CharField(max_length=75)),
                ('IPAddress', models.CharField(max_length=50)),
                ('cpu_usage', models.FloatField()),
                ('energyConsumption', models.FloatField(null=True)),
                ('operationalCost', models.FloatField(null=True)),
                ('apparentWastageCost', models.FloatField(null=True)),
                ('carbonFootprint', models.FloatField(null=True)),
                ('reportId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tool.report')),
            ],
        ),
    ]

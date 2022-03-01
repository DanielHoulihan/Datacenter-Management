# Generated by Django 3.2.12 on 2022-03-01 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguredDataCenters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('masterip', models.CharField(max_length=25, null=True)),
                ('sub_id', models.CharField(max_length=15, null=True)),
                ('datacenterid', models.CharField(max_length=20)),
                ('startTime', models.DateField()),
                ('endTime', models.DateField(null=True)),
                ('pue', models.FloatField()),
                ('energy_cost', models.FloatField()),
                ('carbon_conversion', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Count',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('configured', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentDatacenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('masterip', models.CharField(max_length=25, null=True)),
                ('current', models.CharField(max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Datacenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('masterip', models.CharField(max_length=25, null=True)),
                ('datacenterid', models.CharField(max_length=20, null=True)),
                ('datacentername', models.CharField(max_length=25, null=True)),
                ('description', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('masterip', models.CharField(max_length=25, null=True)),
                ('datacenterid', models.CharField(max_length=20, null=True)),
                ('floorid', models.IntegerField()),
                ('floorname', models.CharField(max_length=25, null=True)),
                ('description', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('masterip', models.CharField(max_length=25, null=True)),
                ('sub_id', models.CharField(max_length=15, null=True)),
                ('datacenterid', models.CharField(max_length=20, null=True)),
                ('floorid', models.IntegerField(null=True)),
                ('rackid', models.IntegerField()),
                ('hostid', models.IntegerField()),
                ('hostname', models.CharField(max_length=30)),
                ('hostdescription', models.CharField(max_length=50)),
                ('hostType', models.CharField(max_length=20)),
                ('processors', models.IntegerField()),
                ('ipaddress', models.CharField(max_length=25)),
                ('lastTime', models.CharField(max_length=25, null=True)),
                ('cpu_usage', models.FloatField(null=True)),
                ('responses', models.IntegerField(null=True)),
                ('total_cpu', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HostEnergy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('masterip', models.CharField(max_length=25, null=True)),
                ('datacenterid', models.CharField(max_length=20, null=True)),
                ('sub_id', models.CharField(max_length=20, null=True)),
                ('floorid', models.IntegerField(null=True)),
                ('rackid', models.IntegerField()),
                ('hostid', models.IntegerField()),
                ('ipaddress', models.CharField(max_length=25)),
                ('TCO', models.FloatField(null=True)),
                ('carbon_footprint', models.FloatField(null=True)),
                ('ops_cons', models.FloatField(null=True)),
                ('total_watts', models.FloatField(null=True)),
                ('minutes', models.FloatField(null=True)),
                ('hours', models.FloatField(null=True)),
                ('kWh', models.FloatField(null=True)),
                ('watt_hour', models.FloatField(null=True)),
                ('capital', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MasterIP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('master', models.CharField(max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('masterip', models.CharField(max_length=25, null=True)),
                ('datacenterid', models.CharField(max_length=20, null=True)),
                ('floorid', models.IntegerField()),
                ('rackid', models.IntegerField()),
                ('rackname', models.CharField(max_length=25, null=True)),
                ('description', models.CharField(max_length=100, null=True)),
                ('pdu', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Threshold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('low', models.FloatField(max_length=25, null=True)),
                ('medium', models.FloatField(max_length=25, null=True)),
            ],
        ),
    ]

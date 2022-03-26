from django.db import models
from django.http import HttpResponseBadRequest
from django.urls import reverse

# Datacenter database model
class Datacenter(models.Model):
    masterip = models.CharField(null=True, max_length=25)
    datacenterid = models.CharField(max_length=20,null=True)
    datacentername = models.CharField(max_length=25, null=True)
    description = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.datacenterid)

    def get_absolute_url(self):
        return reverse('datacenterid', args=[str(self.id)])   

# Floor (asset) database model
class Floor(models.Model):
    masterip = models.CharField(null=True, max_length=25)
    datacenterid = models.CharField(max_length=20,null=True)
    floorid = models.IntegerField()
    floorname = models.CharField(max_length=25, null=True)
    description = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return str(self.floorid)

    def get_absolute_url(self):
        return reverse('floorid', args=[str(self.id)])   

# Rack (asset) database model
class Rack(models.Model):
    masterip = models.CharField(null=True, max_length=25)
    datacenterid = models.CharField(max_length=20,null=True)
    floorid = models.IntegerField()
    rackid = models.IntegerField()
    rackname = models.CharField(max_length=25, null=True)
    description = models.CharField(max_length=100, null=True)
    pdu = models.IntegerField(null=True)
    
    def __str__(self):
        return str(self.rackid)

    def get_absolute_url(self):
        return reverse('rackid', args=[str(self.id)]) 

# Host (asset) database model
class Host(models.Model):
    masterip = models.CharField(null=True, max_length=25)
    sub_id = models.CharField(null=True,max_length=15)
    datacenterid = models.CharField(max_length=20,null=True)
    floorid = models.IntegerField(null=True)
    rackid = models.IntegerField()
    hostid = models.IntegerField()
    hostname = models.CharField(max_length=30)
    hostdescription = models.CharField(max_length=50)
    hostType = models.CharField(max_length=20)
    processors = models.IntegerField()
    ipaddress = models.CharField(max_length=25)
    lastTime = models.CharField(max_length=25, null=True)
    cpu_usage = models.FloatField(null=True)
    responses = models.IntegerField(null=True)
    total_cpu = models.FloatField(null=True)

    def __str__(self):
        return str(self.hostid)

# Stores the current datacenter 
class CurrentDatacenter(models.Model):
    masterip = models.CharField(null=True, max_length=25)
    current = models.CharField(null=True, max_length=25)

# Configured datacenters
class ConfiguredDataCenters(models.Model):
    masterip = models.CharField(null=True, max_length=25)
    sub_id = models.CharField(max_length=15, null=True)
    datacenterid = models.CharField(max_length=20)
    startTime = models.DateField()
    endTime = models.DateField(null=True)
    pue = models.FloatField()
    energy_cost = models.FloatField()
    carbon_conversion = models.FloatField()
    budget = models.IntegerField(null=True)
    
    def __str__(self):
        return str(self.datacenterid)

    def get_absolute_url(self):
        return reverse('datacenterid', args=[str(self.id)])   
    
# Configured count database model
class Count(models.Model):
    configured = models.IntegerField(null=True)

# Stores selected master
class MasterIP(models.Model):
    master = models.CharField(null=True, max_length=25)

# Host energy (TCO + budget) database model
class HostEnergy(models.Model):
    masterip = models.CharField(null=True, max_length=25)
    datacenterid = models.CharField(max_length=20,null=True)
    sub_id = models.CharField(max_length=20,null=True)
    floorid = models.IntegerField(null=True)
    rackid = models.IntegerField()
    hostid = models.IntegerField()
    ipaddress = models.CharField(max_length=25)
    TCO = models.FloatField(null=True)
    carbon_footprint_3 = models.FloatField(null=True)
    ops_cons = models.FloatField(null=True)
    total_watt_hour = models.FloatField(null=True)
    minutes = models.FloatField(null=True)
    hours = models.FloatField(null=True)
    avg_kWh = models.FloatField(null=True)
    avg_watt_hour = models.FloatField(null=True)
    capital = models.IntegerField(null=True)
    ops_cons_3 = models.FloatField(null=True)
    op_cost_3 = models.FloatField(null=True)
    kWh_consumed = models.FloatField(null=True)
    app_waste_cost_3 = models.FloatField(null=True)

# Stores Threshold for host CPU % usage
class Threshold(models.Model):
    low = models.FloatField(null=True, max_length=25)
    medium = models.FloatField(null=True, max_length=25)

# Model to allow updating Budget (TODO)
class Budget(models.Model):
    masterip = models.CharField(max_length=20,null=True)
    sub_id = models.CharField(max_length=20,null=True)
    carbon_used = models.FloatField(null=True)
    energy_used = models.FloatField(null=True)
    time = models.IntegerField(null=True)
    

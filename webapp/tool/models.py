from django.db import models
from django.urls import reverse

class Datacenter(models.Model):
    datacenterid = models.CharField(max_length=20,null=True)
    datacentername = models.CharField(max_length=25, null=True)
    description = models.CharField(max_length=100, null=True)
    startTime = models.IntegerField()

    def __str__(self):
        return str(self.datacenterid)

    def get_absolute_url(self):
        return reverse('datacenterid', args=[str(self.id)])   

class Floor(models.Model):
    datacenterid = models.CharField(max_length=20,null=True)
    floorid = models.IntegerField()
    floorname = models.CharField(max_length=25, null=True)
    description = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return str(self.floorid)

    def get_absolute_url(self):
        return reverse('floorid', args=[str(self.id)])   

class Rack(models.Model):
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

class Host(models.Model):
    datacenterid = models.CharField(max_length=20,null=True)
    floorid = models.IntegerField(null=True)
    rackid = models.IntegerField()
    hostid = models.IntegerField()
    hostname = models.CharField(max_length=30)
    hostdescription = models.CharField(max_length=50)
    hostType = models.CharField(max_length=20)
    processors = models.IntegerField()
    ipaddress = models.CharField(max_length=25)

    def __str__(self):
        return str(self.hostid)

class Hostactivity(models.Model):
    sub_id = models.CharField(null=True,max_length=15)
    datacenterid = models.CharField(max_length=20,null=True)
    floorid = models.IntegerField(null=True)
    rackid = models.IntegerField(null=True)
    hostid = models.IntegerField()
    activityid = models.IntegerField()
    power = models.FloatField()
    power_mode = models.CharField(max_length=25)
    stat1 = models.FloatField()
    stat2 = models.FloatField()
    stat3 = models.FloatField()
    time = models.IntegerField()

    def __str__(self):
        return str(self.activityid)


class CurrentDatacenter(models.Model):
    current = models.CharField(null=True, max_length=25)

class ConfiguredDataCenters(models.Model):
    sub_id = models.CharField(max_length=15, null=True)
    datacenterid = models.CharField(max_length=20)
    startTime = models.DateField()
    pue = models.FloatField()
    energy_cost = models.FloatField()
    carbon_conversion = models.FloatField()


class Count(models.Model):
    configured = models.IntegerField(null=True)










# class Hostactivity(models.Model):
#     sub_id = models.CharField(null=True,max_length=15)
#     datacenterid = models.CharField(max_length=20,null=True)
#     floorid = models.IntegerField(null=True)
#     rackid = models.IntegerField(null=True)
#     hostid = models.IntegerField()
#     activityid = models.IntegerField()
#     power = models.FloatField()
#     power_mode = models.CharField(max_length=25)
#     stat1 = models.FloatField()
#     stat2 = models.FloatField()
#     stat3 = models.FloatField()
#     time = models.IntegerField()

#     def __str__(self):
#         return str(self.activityid)
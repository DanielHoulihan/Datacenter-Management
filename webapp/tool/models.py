from django.db import models

class Application(models.Model):
    masterip = models.CharField(null=True, max_length=25)
    current = models.CharField(null=True, max_length=25)
    configured = models.IntegerField(null=True, default = 0)
    threshold_low = models.FloatField(null=True, max_length=25, default=15)
    threshold_medium = models.FloatField(null=True, max_length=25, default=30)
    
# Datacenter database model
class AvailableDatacenters(models.Model):
    masterip = models.CharField(null=True, max_length=25)
    datacenterid = models.CharField(max_length=20,null=True)
    datacentername = models.CharField(max_length=25, null=True)
    description = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.datacenterid)

# Floor (asset) database model
class Floor(models.Model):
    masterip = models.CharField(null=True, max_length=25)
    sub_id = models.CharField(null=True,max_length=15)
    datacenterid = models.CharField(max_length=20,null=True)
    floorid = models.IntegerField()
    floorname = models.CharField(max_length=25, null=True)
    description = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return str(self.floorid)

# Rack (asset) database model
class Rack(models.Model):
    masterip = models.CharField(null=True, max_length=25)
    sub_id = models.CharField(null=True,max_length=15)
    datacenterid = models.CharField(max_length=20,null=True)
    floorid = models.IntegerField()
    rackid = models.IntegerField()
    rackname = models.CharField(max_length=25, null=True)
    description = models.CharField(max_length=100, null=True)
    pdu = models.IntegerField(null=True)
    
    def __str__(self):
        return str(self.rackid)

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
    
    # Power
    cpu_last_response = models.CharField(max_length=25, null=True)
    cpu_usage = models.FloatField(null=True)
    cpu_responses = models.IntegerField(null=True)
    total_cpu = models.FloatField(null=True)
    
    # Energy
    kWh_consumed = models.FloatField(null=True)
    power_responses = models.IntegerField(null=True)
    total_watt_hour = models.FloatField(null=True)
    power_last_response = models.IntegerField(null=True)
    
    # Metrics
    TCO = models.FloatField(null=True)
    carbon_footprint_3 = models.FloatField(null=True)
    ops_cons_3 = models.FloatField(null=True)
    op_cost_3 = models.FloatField(null=True)
    app_waste_cost_3 = models.FloatField(null=True)
    capital = models.IntegerField(null=True)
    
    def __str__(self):
        return str(self.hostid)
                
                
# # Stores the current datacenter 
# class CurrentDatacenter(models.Model):
#     masterip = models.CharField(null=True, max_length=25)
#     current = models.CharField(null=True, max_length=25)

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
    
# # Configured count database model
# class Count(models.Model):
#     configured = models.IntegerField(null=True)

# # Stores selected master
# class MasterIP(models.Model):
#     master = models.CharField(null=True, max_length=25)

# # Stores Threshold for host CPU % usage
# class Threshold(models.Model):
#     low = models.FloatField(null=True, max_length=25)
#     medium = models.FloatField(null=True, max_length=25)

# Stores budget Information
class Budget(models.Model):
    masterip = models.CharField(max_length=20,null=True)
    sub_id = models.CharField(max_length=20,null=True)
    time = models.IntegerField(null=True)
    energy_dict = models.TextField(null=True)
    carbon_graph1 = models.ImageField(null=True)
    carbon_graph2 = models.ImageField(null=True)
    energy_graph1 = models.ImageField(null=True)
    energy_graph2 = models.ImageField(null=True)
    cost_graph1 = models.ImageField(null=True)
    cost_graph2 = models.ImageField(null=True)
    total_usage = models.FloatField(null=True)
    usage_percentage = models.FloatField(null=True)
    

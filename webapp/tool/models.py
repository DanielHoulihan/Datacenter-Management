from django.db import models

class Report(models.Model):
    reportId = models.CharField(max_length=75, blank=True, null=True)
    createDate = models.CharField(max_length=75, blank=True, null=True)
    message = models.CharField(max_length=75, blank=True, null=True)
    hosts = models.IntegerField(null=True)
    racks = models.IntegerField(null=True)
    data_center_name = models.CharField(max_length=100,null=True)
    pue = models.FloatField(null=True)
    startTime = models.CharField(max_length=20,null=True)
    endTime = models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.reportId
        
class HostReport(models.Model):
    reportId = models.ForeignKey(Report, on_delete=models.CASCADE)
    hostId = models.CharField(max_length=10)
    hostName = models.CharField(max_length=75)
    IPAddress = models.CharField(max_length=50)
    cpu_usage = models.FloatField()
    energyConsumption = models.FloatField(null=True)
    operationalCost = models.FloatField(null=True)
    apparentWastageCost = models.FloatField(null=True)
    carbonFootprint = models.FloatField(null=True)

    def __str__(self):
        return str(self.hostId)


class Threshold(models.Model):
    low = models.IntegerField()
    medium = models.IntegerField()
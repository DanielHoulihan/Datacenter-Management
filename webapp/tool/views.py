from django.shortcuts import  render
from tool.models import Report, HostReport, Threshold
import requests
from datetime import datetime
from django.views.decorators.csrf import csrf_protect


def get_reports(request):
    url = "http://localhost:3002/reports" 
    response = requests.get(url)
    data = response.json()

    for i in data:
        Report.objects.get_or_create(
            reportId = i['id'],
            createDate = i['createDate'],
            message = i['message'],   
            hosts = len(i['hostReports']),
            racks = len(i['rackReports']),
            data_center_name = i['reportParameter']['datacenterName'],
            pue = i['reportParameter']['pue'],
            startTime = datetime.utcfromtimestamp(i['reportParameter']['startTime']).strftime('%Y-%m-%d'),
            endTime = datetime.utcfromtimestamp(i['reportParameter']['endTime']).strftime('%Y-%m-%d'),
        )
        all_reports = Report.objects.all().order_by('-reportId')          

    return render (request, 'reports/report.html', { "all_reports": all_reports} )

@csrf_protect
def report_detail(request, id):

    if request.method == 'POST':
        low = request.POST['low']
        medium = request.POST['medium']
        Threshold.objects.update(low=low,medium=medium)

    get_reports(request)
    url = "http://localhost:3002/reports" 
    response = requests.get(url)
    data = response.json()

    for i in data:
        if i['id']==str(Report.objects.get(id = id)):
            for report in i['hostReports']:
                HostReport.objects.get_or_create(
                    reportId = Report.objects.get(id = id),
                    hostId = report['hostId'],
                    hostName = report['hostName'],
                    IPAddress = report['IPAddress'],
                    cpu_usage = round(report['averageCpuUsage'],2),
                    energyConsumption = round(report['energyConsumption'],2),
                    operationalCost = round(report['operationalCost'],2),
                    apparentWastageCost = round(report['apparentWastageCost'],2),
                    carbonFootprint = round(report['carbonFootprint'],2),
        )           
                host_reports_to_show = HostReport.objects.filter(reportId = 
                    Report.objects.get(id = id)).order_by('-reportId')

    if Threshold.objects.count()==0:
        Threshold.objects.create(low=15,medium=30)

    return render (request,'reports/report_detail.html',{'hosts': host_reports_to_show, "threshold": Threshold.objects.all().get()}
    )


def host_detail(request, id, Id2):
    report_detail(request, id)
    host = HostReport.objects.filter(reportId = Report.objects.get(id = id)).\
            get(hostId = HostReport.objects.get(id = Id2))
    return render (request,'reports/host_detail.html',{'hosts': host, "threshold": Threshold.objects.all().get()}
    )
    
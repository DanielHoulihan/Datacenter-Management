from django.shortcuts import  render
from tool import tco_services
from tool.models import ConfiguredDataCenters, Datacenter, Floor, Rack, Host, CurrentDatacenter, Count, MasterIP, HostEnergy, Threshold
from . import services
from . import forms
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
import time
from django.db.models import Avg, Max


def datacenters(request):

    services.get_datacenters()
    master = MasterIP.objects.all().values().get()["master"]

    if request.method == 'POST':
        form = forms.SelectCurrentForm(request.POST)
        if form.is_valid():
            current = form.cleaned_data['current_datacenter']
            if CurrentDatacenter.objects.count()==0:
                CurrentDatacenter.objects.create(masterip = master, current=current)
            else: CurrentDatacenter.objects.update(masterip = master, current=current)

    datacenters = Datacenter.objects.filter(masterip=master).all()
    configured = ConfiguredDataCenters.objects.filter(masterip=master).all()
    configured_count = configured.count()

    if CurrentDatacenter.objects.all().count()!=0 and CurrentDatacenter.objects.all().values().get()['masterip'] == master:
        current = CurrentDatacenter.objects.filter(masterip=master).all().values().get()['current']
        return render (request, 'home/home.html', { "datacenters": datacenters, "current": current, "configured":configured, "configured_count": configured_count, "master":master} )
    else: return render (request, 'home/home.html', { "datacenters": datacenters, "current": "Not selected", "configured":configured, "configured_count": configured_count, "master":master} )

def floors(request):
    master = MasterIP.objects.all().values().get()["master"]
    if CurrentDatacenter.objects.filter(masterip=master).all().count()==0:
        return render (request, 'pick_datacenter/pick_data_center.html', { "floors": "Pick a data center", "floor_count": 0} )
    current = CurrentDatacenter.objects.all().values().get()['current'].split('-')[0]
    services.get_floors(current)

    floors = Floor.objects.filter(datacenterid=current).filter(masterip=master).all()
    floor_count = floors.count()
    return render (request, 'assets/floors.html', { "floors": floors, "floor_count": floor_count} )


def racks(request, floorid):
    current = CurrentDatacenter.objects.all().values().get()['current'].split('-')[0]
    services.get_racks(current, floorid)
    racks = Rack.objects.filter(datacenterid=current).filter(floorid=floorid).filter(masterip=MasterIP.objects.all().values().get()["master"]).all()
    rack_count = racks.count()
    return render (request, 'assets/racks.html', { "racks": racks, "rack_count": rack_count} )


def hosts(request, floorid, rackid):
    if Threshold.objects.count()==0:
        Threshold.objects.create(low=15,medium=30)

    if request.method == 'POST':
        low = request.POST['low']
        medium = request.POST['medium']
        Threshold.objects.update(low=low,medium=medium)

    startTime = ConfiguredDataCenters.objects.all().filter(sub_id = CurrentDatacenter.objects.all().values().get()['current']).values().get()['startTime']
    startTime_unix = int(time.mktime(startTime.timetuple()))
    if ConfiguredDataCenters.objects.all().filter(sub_id = CurrentDatacenter.objects.all().values().get()['current']).values().get()['endTime']==None:
        endTime = str(int(time.time()))
    else:
        endTime = ConfiguredDataCenters.objects.all().filter(sub_id = CurrentDatacenter.objects.all().values().get()['current']).values().get()['endTime']
        endTime = int(time.mktime(endTime.timetuple()))

    master=MasterIP.objects.all().values().get()["master"]
    current = str(CurrentDatacenter.objects.all().values().get()['current'].split('-')[0])


    services.get_hosts(master, current, floorid, rackid, startTime_unix, endTime)
    hosts = Host.objects.filter(sub_id=str(CurrentDatacenter.objects.all().values().get()['current'])).filter(floorid=floorid).filter(masterip=master).filter(rackid=rackid).all()
    host_count = hosts.count()
    threshold = Threshold.objects.all().get()
    return render (request, 'assets/hosts.html', { "hosts": hosts, "host_count": host_count, "threshold": threshold} )
    
@csrf_protect
def configure(request):
    services.get_datacenters()
    master = MasterIP.objects.all().values().get()["master"]
    if request.method == 'POST':
        if 'to_delete' in request.POST:
            form = forms.DeleteConfigurationForm(request.POST)
            if form.is_valid():
                to_delete = form.cleaned_data['to_delete']
                ConfiguredDataCenters.objects.filter(sub_id=to_delete).delete()
                CurrentDatacenter.objects.filter(current=to_delete).delete()
        elif 'ip' in request.POST:
            ip = request.POST['ip']
            MasterIP.objects.update(master = ip)
            services.get_datacenters()
        elif 'to_configure' in request.POST:
            to_configure = request.POST['to_configure']
            start = request.POST['start']
            pue = request.POST['pue']
            energy_cost = request.POST['energy_cost']
            carbon_conversion = request.POST['carbon_conversion']
            if Count.objects.all().count()==0:
                Count.objects.create(configured=0)
            else: 
                Count.objects.update(configured = Count.objects.all().values().get()['configured']+1)
            if request.POST['endTime']: 
                ConfiguredDataCenters.objects.get_or_create(
                masterip = master,
                sub_id = str(to_configure)+"-"+str(Count.objects.all().values().get()['configured']+1),
                datacenterid = to_configure,
                startTime = start,
                endTime = request.POST['endTime'],
                pue = pue,
                energy_cost = energy_cost,
                carbon_conversion = carbon_conversion
            )
            else:
                ConfiguredDataCenters.objects.get_or_create(
                    masterip = master,
                    sub_id = str(to_configure)+"-"+str(Count.objects.all().values().get()['configured']+1),
                    datacenterid = to_configure,
                    startTime = start,
                    pue = pue,
                    energy_cost = energy_cost,
                    carbon_conversion = carbon_conversion
                )

    master = MasterIP.objects.all().values().get()["master"]
    configured = ConfiguredDataCenters.objects.filter(masterip=master).all()
    datacenters = Datacenter.objects.filter(masterip=master).all()
    configured_count = ConfiguredDataCenters.objects.filter(masterip=master).all().count()
    return render (request, 'configure/configure.html', { "datacenters": datacenters, "configured_count": configured_count, "configured": configured, "master":master} )

def budget(request):
    return render (request, 'budget/budget.html', { "budget": "Budget will be here"} )




@csrf_protect
def tco(request):
    master = MasterIP.objects.all().values().get()["master"]
    if CurrentDatacenter.objects.filter(masterip=master).all().count()==0:
        return render (request, 'pick_datacenter/pick_data_center.html', { "floors": "Pick a data center", "floor_count": 0} )
    current = str(CurrentDatacenter.objects.all().values().get()['current'].split('-')[0])
    if request.method == 'POST':
        if 'capital' in request.POST:
            capital = request.POST['capital']
            rack = request.POST['rack']
            floor = request.POST['floor']
            host = request.POST['host']
            startTime = ConfiguredDataCenters.objects.all().filter(sub_id = CurrentDatacenter.objects.all().values().get()['current']).values().get()['startTime']
            startTime = str(int(time.mktime(startTime.timetuple())))
            if ConfiguredDataCenters.objects.all().filter(sub_id = CurrentDatacenter.objects.all().values().get()['current']).values().get()['endTime']==None:
                endTime = str(int(time.time()))
            else:
                endTime = ConfiguredDataCenters.objects.all().filter(sub_id = CurrentDatacenter.objects.all().values().get()['current']).values().get()['endTime']
                endTime = str(int(time.mktime(endTime.timetuple())))
            tco_services.get_energy_usage(master, current, floor, rack, host, startTime, endTime)


    current = str(CurrentDatacenter.objects.all().values().get()['current'].split('-')[0])
    tco_services.find_all_available_hosts(master, current)

    all_available = HostEnergy.objects.filter(datacenterid=current).filter(masterip=master).all()
    tco_count = all_available.count()

    return render (request, 'TCO/tco.html', { "tco": all_available, "tco_count": tco_count} )























# def host_activity(request, floorid, rackid, hostid):
#     startTime = ConfiguredDataCenters.objects.all().filter(sub_id = CurrentDatacenter.objects.all().values().get()['current']).values().get()['startTime']
#     current = CurrentDatacenter.objects.all().values().get()['current'].split('-')[0]

#     startTime_unix = int(time.mktime(startTime.timetuple()))
    
#     activities = Hostactivity.objects.filter(
#         masterip=MasterIP.objects.all().values().get()["master"]).filter(
#         sub_id = CurrentDatacenter.objects.all().values().get()['current']).filter(
#         datacenterid=current).filter(
#             floorid=floorid).filter(
#                 rackid=rackid).filter(
#                     hostid=hostid).all()

#     if activities.count()==0:
#         services.get_host_detail(current, floorid, rackid, hostid, startTime_unix)
#     else: 
#         services.get_host_detail(current, floorid, rackid, hostid, activities.aggregate(Max('time')).get('time__max'))
#     activities_count = activities.count()
#     average = activities.aggregate(Avg('stat1'), Avg('stat2'), Avg('stat3'))# or 0.00
#     return render (request, 'reports/host_activity.html', { "average": average, "activities_count": activities_count} )
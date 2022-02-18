from django.shortcuts import  render
from tool.models import ConfiguredDataCenters, Datacenter, Floor, Rack, Host, Hostactivity, CurrentDatacenter, Count
from . import services
from . import forms
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
import time


def datacenters(request):
    services.get_datacenters()
    if request.method == 'POST':
        current = request.POST['current']
        if CurrentDatacenter.objects.count()==0:
            CurrentDatacenter.objects.create(current=current)
        else: CurrentDatacenter.objects.update(current=current)

    datacenters = Datacenter.objects.all()
    configured = ConfiguredDataCenters.objects.all()
    configured_count = ConfiguredDataCenters.objects.all().count()
    if CurrentDatacenter.objects.count()!=0:
        current = CurrentDatacenter.objects.all().values().get()['current']
        return render (request, 'reports/home.html', { "datacenters": datacenters, "current": current, "configured":configured, "configured_count": configured_count} )
    else: return render (request, 'reports/home.html', { "datacenters": datacenters, "current": "Not selected", "configured":configured, "configured_count": configured_count} )

def floors(request):
    if CurrentDatacenter.objects.all().count()==0:
        return render (request, 'reports/pick_data_center.html', { "floors": "Pick a data center", "floor_count": 0} )
    current = CurrentDatacenter.objects.all().values().get()['current'].split('-')[0]
    print(current)
    services.get_floors(current)

    floors = Floor.objects.filter(datacenterid=current).all()
    floor_count = Floor.objects.filter(datacenterid=current).all().count()
    return render (request, 'reports/floors.html', { "floors": floors, "floor_count": floor_count} )


def racks(request, floorid):
    print(CurrentDatacenter.objects.all())
    current = CurrentDatacenter.objects.all().values().get()['current'].split('-')[0]
    services.get_racks(current, floorid)
    
    racks = Rack.objects.filter(datacenterid=current).filter(floorid=floorid).all()
    rack_count = racks.count()
    return render (request, 'reports/racks.html', { "racks": racks, "rack_count": rack_count} )


def hosts(request, floorid, rackid):
    current = str(CurrentDatacenter.objects.all().values().get()['current'].split('-')[0])
    services.get_hosts(current, floorid, rackid)

    hosts = Host.objects.filter(datacenterid=current).filter(floorid=floorid).filter(rackid=rackid).all()
    host_count = hosts.count()
    return render (request, 'reports/hosts.html', { "hosts": hosts, "host_count": host_count} )
    


def host_activity(request, floorid, rackid, hostid):
    startTime = ConfiguredDataCenters.objects.all().filter(sub_id = CurrentDatacenter.objects.all().values().get()['current']).values().get()['startTime']
    current = CurrentDatacenter.objects.all().values().get()['current'].split('-')[0]

    startTime_unix = time.mktime(startTime.timetuple())
    startTime_unix = int(startTime_unix)
    print("starttime: " + str(startTime_unix))
    services.get_host_detail(current, floorid, rackid, hostid, startTime_unix)

    activities = Hostactivity.objects.filter(
        sub_id = CurrentDatacenter.objects.all().values().get()['current']).filter(
        datacenterid=current).filter(
            floorid=floorid).filter(
                rackid=rackid).filter(
                    hostid=hostid).all()
    activities_count = activities.count()

    return render (request, 'reports/host_activity.html', { "activities": activities, "activities_count": activities_count} )


@csrf_protect
def configure(request):
    services.get_datacenters()
    if request.method == 'POST':
        print(request.POST)
        if 'Delete' in request.POST:
            to_delete = request.POST['Delete']
            ConfiguredDataCenters.objects.filter(sub_id=to_delete).delete()
            CurrentDatacenter.objects.filter(current=to_delete).delete()
        else:
            to_configure = request.POST['to_configure']
            start = request.POST['start']
            pue = request.POST['pue']
            energy_cost = request.POST['energy_cost']
            carbon_conversion = request.POST['carbon_conversion']
            if Count.objects.all().count()==0:
                Count.objects.create(configured=0)
            else: 
                Count.objects.update(configured = Count.objects.all().values().get()['configured']+1)
            ConfiguredDataCenters.objects.get_or_create(
                sub_id = str(to_configure)+"-"+str(Count.objects.all().values().get()['configured']+1),
                datacenterid = to_configure,
                startTime = start,
                pue = pue,
                energy_cost = energy_cost,
                carbon_conversion = carbon_conversion
            )


    configured = ConfiguredDataCenters.objects.all()
    datacenters = Datacenter.objects.all()
    configured_count = ConfiguredDataCenters.objects.all().count()
    return render (request, 'reports/configure.html', { "datacenters": datacenters, "configured_count": configured_count, "configured": configured} )


def budget(request):
    return render (request, 'reports/budget.html', { "budget": "Budget will be here"} )

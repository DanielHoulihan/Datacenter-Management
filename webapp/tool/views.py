from django.shortcuts import  render
from tool import tco_services
from tool.models import ConfiguredDataCenters, Datacenter, Floor, Rack, Host, CurrentDatacenter, Count, MasterIP, HostEnergy, Threshold
from . import asset_services, services
from . import forms
from django.views.decorators.csrf import csrf_protect
import time


def datacenters(request):
    asset_services.get_datacenters()
    master = services.get_master()

    if request.method == 'POST':
        form = forms.SelectCurrentForm(request.POST)
        if form.is_valid():
            current = form.cleaned_data['current_datacenter']
            if CurrentDatacenter.objects.count()==0:
                CurrentDatacenter.objects.create(masterip = master, current=current)
            else: CurrentDatacenter.objects.update(masterip = master, current=current)

    datacenters = Datacenter.objects.filter(masterip=master).all()
    configured = services.get_configured()
    configured_count = configured.count()
    
    return render (request, 'home/home.html', { "datacenters": datacenters, "current": services.get_current_for_html(), "configured":configured, "configured_count": configured_count, "master":master, "page":"home"} )

def floors(request):
    master = services.get_master()
    if CurrentDatacenter.objects.filter(masterip=master).all().count()==0:
        return render (request, 'pick_datacenter/pick_data_center.html', { "floors": "Pick a data center", "floor_count": 0, "master": services.get_master(), "current": services.get_current_for_html(), "configured": services.get_configured(), "page":"assets"} )
    current = services.get_current_datacenter()
    asset_services.get_floors(current)

    floors = Floor.objects.filter(datacenterid=current).filter(masterip=master).all()
    floor_count = floors.count()
    return render (request, 'assets/floors.html', { "floors": floors, "floor_count": floor_count, "master":master, "current": services.get_current_for_html(), "configured": services.get_configured(), "page":"assets"} )


def racks(request, floorid):
    current = services.get_current_datacenter()
    asset_services.get_racks(current, floorid)
    racks = Rack.objects.filter(datacenterid=current).filter(floorid=floorid).filter(masterip=services.get_master()).all()
    rack_count = racks.count()
    return render (request, 'assets/racks.html', { "racks": racks, "rack_count": rack_count, "master":services.get_master(), "current": services.get_current_for_html(), "configured": services.get_configured(), "page":"assets"} )


def hosts(request, floorid, rackid):
    if Threshold.objects.count()==0:
        Threshold.objects.create(low=15,medium=30)

    if request.method == 'POST':
        low = request.POST['low']
        medium = request.POST['medium']
        Threshold.objects.update(low=low,medium=medium)

    startTime = ConfiguredDataCenters.objects.all().filter(sub_id = services.get_current_sub_id()).values().get()['startTime']
    startTime_unix = int(time.mktime(startTime.timetuple()))
    if ConfiguredDataCenters.objects.all().filter(sub_id = services.get_current_sub_id()).values().get()['endTime']==None:
        endTime = str(int(time.time()))
    else:
        endTime = ConfiguredDataCenters.objects.all().filter(sub_id = services.get_current_sub_id()).values().get()['endTime']
        endTime = int(time.mktime(endTime.timetuple()))

    master=services.get_master()
    current = str(services.get_current_datacenter())


    asset_services.get_hosts(master, current, floorid, rackid, startTime_unix, endTime)
    hosts = Host.objects.filter(sub_id=str(services.get_current_sub_id())).filter(floorid=floorid).filter(masterip=master).filter(rackid=rackid).all()
    host_count = hosts.count()
    threshold = Threshold.objects.all().get()
    return render (request, 'assets/hosts.html', { "hosts": hosts, "host_count": host_count, "threshold": threshold, "master":services.get_master(), "current": services.get_current_for_html(), "configured": services.get_configured(), "page":"assets"} )
    
@csrf_protect
def configure(request):
    asset_services.get_datacenters()
    master = services.get_master()
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
            asset_services.get_datacenters()
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

    master = services.get_master()
    configured = ConfiguredDataCenters.objects.filter(masterip=master).all()
    datacenters = Datacenter.objects.filter(masterip=master).all()
    configured_count = ConfiguredDataCenters.objects.filter(masterip=master).all().count()
    return render (request, 'configure/configure.html', { "datacenters": datacenters, "configured_count": configured_count, "configured": configured, "master":master, "current": services.get_current_for_html(), "page":"configure"} )

def budget(request):
    return render (request, 'budget/budget.html', { "budget": "Budget will be here", "master": services.get_master(), "current": services.get_current_for_html(), "configured": services.get_configured(), "page":"budget"} )




@csrf_protect
def tco(request):
    master = services.get_master()
    if CurrentDatacenter.objects.filter(masterip=master).all().count()==0:
        return render (request, 'pick_datacenter/pick_data_center.html', { "floors": "Pick a data center", "master": services.get_master(), "current": services.get_current_for_html(), "configured": services.get_configured()} )
    current = str(services.get_current_datacenter())
    if request.method == 'POST':
        if 'capital' in request.POST:
            capital = request.POST['capital']
            rack = request.POST['rack']
            floor = request.POST['floor']
            host = request.POST['host']
            startTime = ConfiguredDataCenters.objects.all().filter(sub_id = services.get_current_sub_id()).values().get()['startTime']
            startTime = str(int(time.mktime(startTime.timetuple())))
            if ConfiguredDataCenters.objects.all().filter(sub_id = services.get_current_sub_id()).values().get()['endTime']==None:
                endTime = str(int(time.time()))
            else:
                endTime = ConfiguredDataCenters.objects.all().filter(sub_id = services.get_current_sub_id()).values().get()['endTime']
                endTime = str(int(time.mktime(endTime.timetuple())))
            
            tco_services.get_energy_usage(master, current, floor, rack, host, startTime, endTime, capital)


    current_sub = services.get_current_sub_id()
    tco_services.find_all_available_hosts(master, current)

    all_available = HostEnergy.objects.filter(sub_id=current_sub).filter(masterip=master).all()
    tco_count = all_available.count()

    return render (request, 'TCO/tco.html', { "tco": all_available, "tco_count": tco_count, "master": master, "current": services.get_current_for_html(), "configured": services.get_configured(), "page":"tco"} )
























from django.shortcuts import  render
from tool.models import Datacenter, Floor, Rack, Host, Hostactivity, CurrentDatacenter
from . import services
import requests
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
import time


def get_datacenters(request):

    url = "http://192.168.56.103:8080/papillonserver/rest/datacenters" 
    response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    data = response.json()
    
    if request.method == 'POST':
        current = request.POST['current']
        CurrentDatacenter.objects.update(current=current)

    if CurrentDatacenter.objects.count()==0:
        CurrentDatacenter.objects.create(current = 268)

    if data!=None: 
        if isinstance(data['datacenter'], list):
            for i in data['datacenter']:
                Datacenter.objects.get_or_create(
                    datacenterid = i['id'],
                    datacentername = i['name'],
                    description = i['description'],
                    startTime = 1644537600,
                )
        else:
            Datacenter.objects.get_or_create(
                datacenterid = data['datacenter']['id'],
                datacentername = data['datacenter']['name'],
                description = data['datacenter']['description'],
                startTime = 1644537600,
            )

    datacenters = Datacenter.objects.all()
    current = CurrentDatacenter.objects.all().get()
    return render (request, 'reports/home.html', { "datacenters": datacenters, "current": current} )

# @csrf_protect
def floors(request):
    get_datacenters(request)

    current = str(CurrentDatacenter.objects.all().values().get()['current'])
    url = "http://192.168.56.103:8080/papillonserver/rest/datacenters/"+current+"/floors"
    response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    data = response.json()
    
    if data!=None: 
        if isinstance(data['floor'], list):
            for i in data['floor']:
                Datacenter.objects.get_or_create(
                    datacenterid = i['datacenterId'],
                    floorid = i['id'],
                    floorname = i['name'],
                    description = i['description']
                )
        else:
            Floor.objects.get_or_create(
                datacenterid = data['floor']['datacenterId'],
                floorid = data['floor']['id'],
                floorname = data['floor']['name'],
                description = data['floor']['description']
            )


    floors = Floor.objects.filter(datacenterid=current).all()
    floor_count = Floor.objects.filter(datacenterid=current).all().count()
    return render (request, 'reports/floors.html', { "floors": floors, "floor_count": floor_count} )


def racks(request, floorid):
    floors(request)
    current = str(CurrentDatacenter.objects.all().values().get()['current'])
    url = "http://192.168.56.103:8080/papillonserver/rest/datacenters/"+current+"/floors/"+floorid+"/racks"
    response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    data = response.json()
    
    if data!=None: 
        if isinstance(data['rack'], list):
            for i in data['rack']:
                Rack.objects.get_or_create(
                    floorid = i['floorId'],
                    rackid = i['id'],
                    rackname = i['name'],
                    description = i['description'],
                    pdu = i['pdu'],
                )
        else:
            Rack.objects.get_or_create(
                floorid = data['rack']['floorId'],
                rackid = data['rack']['id'],
                rackname = data['rack']['name'],
                description = data['rack']['description'],
                pdu = data['rack']['pdu']
            )


    racks = Rack.objects.all()
    rack_count = Rack.objects.all().count()
    return render (request, 'reports/racks.html', { "racks": racks, "rack_count": rack_count} )


def hosts(request, floorid, rackid):
    racks(request, floorid)
    current = str(CurrentDatacenter.objects.all().values().get()['current'])
    url = "http://192.168.56.103:8080/papillonserver/rest/datacenters/"+current+"/floors/"+floorid+"/racks/"+rackid+"/hosts"
    response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    data = response.json()
    
    if data!=None: 
        if isinstance(data['host'], list):
            for i in data['host']:
                Host.objects.get_or_create(
                    rackid = i['rackId'],
                    hostid = i['id'],
                    hostname = i['name'],
                    hostdescription = i['description'],
                    hostType = i['hostType'],
                    processors = i['processorCount'],
                    ipaddress = i['IPAddress']
                )
        else:
            Host.objects.get_or_create(
                rackid = data['host']['rackId'],
                hostid = data['host']['id'],
                hostname = data['host']['name'],
                hostdescription = data['host']['description'],
                hostType = data['host']['hostType'],
                processors = data['host']['processorCount'],
                ipaddress = data['host']['IPAddress']
            )


    hosts = Host.objects.all()
    host_count = Host.objects.all().count()
    return render (request, 'reports/hosts.html', { "hosts": hosts, "host_count": host_count} )
    


def host_activity(request, floorid, rackid, hostid):
    racks(request, floorid)
    current = str(CurrentDatacenter.objects.all().values().get()['current'])
    url = "http://192.168.56.103:8080/papillonserver/rest/datacenters/"+current+"/floors/"+floorid+"/racks/"+rackid+"/hosts/"+hostid+"/activity?starttime=1644537600&endtime=1645046167"
    response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    data = response.json()
    
    if data!=None: 
        if isinstance(data['activity'], list):
            for i in data['activity']:
                Hostactivity.objects.get_or_create(
                    hostid = i['hostId'],
                    activityid = i['id'],
                    power = i['power'],
                    power_mode = i['powerMode'],
                    stat1 = i['stat1'],
                    stat2 = i['stat2'],
                    stat3 = i['stat3'],
                    time = i['timeStamp'],
                )
        else:
            Hostactivity.objects.get_or_create(
                hostid = data['activity']['hostId'],
                activityid = data['activity']['id'],
                power = data['activity']['power'],
                power_mode = data['activity']['powerMode'],
                stat1 = data['activity']['stat1'],
                stat2 = data['activity']['stat2'],
                stat3 = data['activity']['stat3'],
                time = data['activity']['timeStamp']
            )


    activities = Hostactivity.objects.all()
    activities_count = Hostactivity.objects.all().count()
    return render (request, 'reports/host_activity.html', { "activities": activities, "activities_count": activities_count} )
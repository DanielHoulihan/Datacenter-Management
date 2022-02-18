from tool.models import Datacenter, Floor, CurrentDatacenter, Host, Hostactivity, Rack
import requests

def get_datacenters():
    url = "http://192.168.56.103:8080/papillonserver/rest/datacenters" 
    response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    data = response.json()

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



def get_floors(datacenter):
    get_datacenters()
    url = "http://192.168.56.103:8080/papillonserver/rest/datacenters/"+datacenter+"/floors"
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


def get_racks(datacenter, floorid):
    get_floors(datacenter)
    url = "http://192.168.56.103:8080/papillonserver/rest/datacenters/"+datacenter+"/floors/"+floorid+"/racks"
    response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    data = response.json()

    if data!=None: 
        if isinstance(data['rack'], list):
            for i in data['rack']:
                Rack.objects.get_or_create(
                    datacenterid = datacenter,
                    floorid = i['floorId'],
                    rackid = i['id'],
                    rackname = i['name'],
                    description = i['description'],
                    pdu = i['pdu'],
                )
        else:
            Rack.objects.get_or_create(
                datacenterid = datacenter,
                floorid = data['rack']['floorId'],
                rackid = data['rack']['id'],
                rackname = data['rack']['name'],
                description = data['rack']['description'],
                pdu = data['rack']['pdu']
            )


def get_hosts(datacenter, floorid, rackid):
    get_racks(datacenter, floorid)
    url = "http://192.168.56.103:8080/papillonserver/rest/datacenters/"+datacenter+"/floors/"+floorid+"/racks/"+rackid+"/hosts"
    response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    data = response.json()
    
    if data!=None: 
        if isinstance(data['host'], list):
            for i in data['host']:
                Host.objects.get_or_create(
                    datacenterid = datacenter,
                    floorid = floorid,
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
                datacenterid = datacenter,
                floorid = floorid,
                rackid = data['host']['rackId'],
                hostid = data['host']['id'],
                hostname = data['host']['name'],
                hostdescription = data['host']['description'],
                hostType = data['host']['hostType'],
                processors = data['host']['processorCount'],
                ipaddress = data['host']['IPAddress']
            )

def get_host_detail(datacenter, floorid, rackid, hostid, startTime):
    get_hosts(datacenter, floorid, rackid)
    url = "http://192.168.56.103:8080/papillonserver/rest/datacenters/"+datacenter+"/floors/"+floorid+"/racks/"+rackid+"/hosts/"+hostid+"/activity?starttime="+str(startTime)+"&endtime=1645111761"
    response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    data = response.json()

    if data!=None: 
        if isinstance(data['activity'], list):
            for i in data['activity']:
                Hostactivity.objects.get_or_create(
                    sub_id = CurrentDatacenter.objects.all().values().get()['current'],
                    datacenterid = datacenter,
                    floorid = floorid,
                    rackid = rackid,
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
                sub_id = CurrentDatacenter.objects.all().values().get()['current'],
                datacenterid = datacenter,
                floorid = floorid,
                rackid = rackid,
                hostid = data['activity']['hostId'],
                activityid = data['activity']['id'],
                power = data['activity']['power'],
                power_mode = data['activity']['powerMode'],
                stat1 = data['activity']['stat1'],
                stat2 = data['activity']['stat2'],
                stat3 = data['activity']['stat3'],
                time = data['activity']['timeStamp']
            )
from tool.models import Datacenter, Floor, CurrentDatacenter, Host, MasterIP, Rack, ConfiguredDataCenters
import requests
import time
from . import services

def get_datacenters():
    if MasterIP.objects.count()==0:
        MasterIP.objects.create(master="localhost")
    master = services.get_master()
    url = "http://"+master+":8080/papillonserver/rest/datacenters" 
    try:
        response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    except Exception:
        return 
    data = response.json()
    if data!=None: 
        if isinstance(data['datacenter'], list):
            for i in data['datacenter']:
                Datacenter.objects.get_or_create(
                    masterip=master,
                    datacenterid = i['id'],
                    datacentername = i['name'],
                    description = i['description'],
                )
        else:
            Datacenter.objects.get_or_create(
                masterip = master,
                datacenterid = data['datacenter']['id'],
                datacentername = data['datacenter']['name'],
                description = data['datacenter']['description'],
            )


def get_floors(datacenter):
    get_datacenters()
    master = services.get_master()
    url = "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/floors"
    response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    data = response.json()
    if data!=None: 
        if isinstance(data['floor'], list):
            for i in data['floor']:
                Floor.objects.get_or_create(
                    masterip = master,
                    datacenterid = i['datacenterId'],
                    floorid = i['id'],
                    floorname = i['name'],
                    description = i['description']
                )
        else:
            Floor.objects.get_or_create(
                masterip = master,
                datacenterid = data['floor']['datacenterId'],
                floorid = data['floor']['id'],
                floorname = data['floor']['name'],
                description = data['floor']['description']
            )


def get_racks(datacenter, floorid):
    get_floors(datacenter)
    master = services.get_master()
    url = "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/floors/"+floorid+"/racks"
    response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    data = response.json()
    if data!=None: 
        if isinstance(data['rack'], list):
            for i in data['rack']:
                Rack.objects.get_or_create(
                    masterip = master,
                    datacenterid = datacenter,
                    floorid = i['floorId'],
                    rackid = i['id'],
                    rackname = i['name'],
                    description = i['description'],
                    pdu = i['pdu'],
                )
        else:
            Rack.objects.get_or_create(
                masterip = master,
                datacenterid = datacenter,
                floorid = data['rack']['floorId'],
                rackid = data['rack']['id'],
                rackname = data['rack']['name'],
                description = data['rack']['description'],
                pdu = data['rack']['pdu']
            )


def get_hosts(master, datacenter, floorid, rackid, startTime, endTime):
    start = time.time()
    get_racks(datacenter, floorid)
    current = services.get_current_sub_id()
    url = "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/floors/"+floorid+"/racks/"+rackid+"/hosts/"
    response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    data = response.json()

    if data!=None: 
        if not isinstance(data['host'], list):
            return
        else:
            for i in data['host']:
                new_url = url + i['id'] +"/activity?starttime="+str(startTime)+"&endtime="+str(endTime)
                response = requests.get(new_url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
                data2 = response.json()
                cpu_total = 0
                cpu_count = 0
                if data2==None:
                    Host.objects.get_or_create(
                        masterip = master,
                        sub_id = services.get_current_sub_id(),
                        datacenterid = datacenter,
                        floorid = floorid,
                        rackid = i['rackId'],
                        hostid = i['id'],
                        hostname = i['name'],
                        hostdescription = i['description'],
                        hostType = i['hostType'],
                        processors = i['processorCount'],
                        ipaddress = i['IPAddress'],
                    )
                    continue
                if not isinstance(data2['activity'], list):
                    cpu_total = float(data2['activity']['stat1'])
                    cpu_count = 1
                else:
                    for activity in data2['activity']:
                        cpu_total += float(activity['stat1'])
                        cpu_count += 1 
                avg_cpu = cpu_total/cpu_count
                host = Host.objects.filter(masterip=master).filter(sub_id = current).filter(floorid=floorid).filter(rackid=rackid).filter(hostid=i['id'])
                if host.count()==0:
                    Host.objects.get_or_create(
                        masterip = master,
                        sub_id = services.get_current_sub_id(),
                        datacenterid = datacenter,
                        floorid = floorid,
                        rackid = i['rackId'],
                        hostid = i['id'],
                        hostname = i['name'],
                        hostdescription = i['description'],
                        hostType = i['hostType'],
                        processors = i['processorCount'],
                        ipaddress = i['IPAddress'],
                        lastTime = data2['activity'][-1:][0]['timeStamp'],
                        cpu_usage = avg_cpu,
                        responses = cpu_count,
                        total_cpu = cpu_total
                    )
                host.update(cpu_usage=avg_cpu, responses=cpu_count, total_cpu = cpu_total)


    end = time.time()
    print("Time taken to get CPU % (s) -> " + str(end-start))
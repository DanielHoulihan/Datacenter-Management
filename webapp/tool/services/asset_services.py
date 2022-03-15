from . import model_services
from tool.models import Datacenter, Floor, CurrentDatacenter, Host, MasterIP, Rack, ConfiguredDataCenters
import requests
import time
from . import services

def get_datacenters():
    services.check_master()
    master = services.get_master()
    url = "http://"+master+":8080/papillonserver/rest/datacenters" 
    try:
        response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    except Exception: return 
    data = response.json()
    if data!=None: 
        if isinstance(data['datacenter'], list):
            for i in data['datacenter']:
                model_services.create_datacenter(master,i['id'],i['name'],i['description'])
        else:
            model_services.create_datacenter(master,data['datacenter']['id'],data['datacenter']['name'],
            data['datacenter']['description'])


def get_floors(datacenter):
    get_datacenters()
    master = services.get_master()
    url = "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/floors"
    response = services.get_reponse(url)
    data = response.json()
    if data!=None: 
        if isinstance(data['floor'], list):
            for i in data['floor']:
                model_services.create_floor(master,i['datacenterId'],i['id'],i['name'],i['description'])
        else:
            model_services.create_floor(master,data['floor']['datacenterId'],data['floor']['id'],
            data['floor']['name'],data['floor']['description'])


def get_racks(datacenter, floorid):
    get_floors(datacenter)
    master = services.get_master()
    url = "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/floors/"+floorid+"/racks"
    response = services.get_reponse(url)
    data = response.json()
    if data!=None: 
        if isinstance(data['rack'], list):
            for i in data['rack']:
                model_services.create_rack(master,datacenter,i['floorId'],i['id'],i['name'],i['description'], i['pdu'])
        else:
            model_services.create_rack(master,datacenter,data['rack']['floorId'],data['rack']['id'],
            data['rack']['name'],data['rack']['description'],data['rack']['pdu'])


def get_hosts(master, datacenter, floorid, rackid, startTime, endTime):
    get_racks(datacenter, floorid)
    current = services.get_current_sub_id()
    url = "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/floors/"+floorid+"/racks/"+rackid+"/hosts/"
    response = services.get_reponse(url)
    data = response.json()
    if data!=None: 
        if not isinstance(data['host'], list):
            get_host_energy(data['host'], url, startTime,endTime,master,datacenter,floorid,current,rackid)
        else:
            for i in data['host']:
                get_host_energy(i, url, startTime,endTime,master,datacenter,floorid,current,rackid)



def get_host_energy(prefix, url, startTime,endTime,master,datacenter,floorid,current,rackid):
    new_url = url + prefix['id'] +"/activity?starttime="+str(startTime)+"&endtime="+str(endTime)
    response = services.get_reponse(new_url)
    data2 = response.json()
    cpu_total = 0
    cpu_count = 0
    if data2==None:
        model_services.create_empty_host(master,services.get_current_sub_id(),datacenter,floorid,prefix['rackId'],
        prefix['id'],prefix['name'],prefix['description'],prefix['hostType'],prefix['processorCount'],prefix['IPAddress'])
        return
    if not isinstance(data2['activity'], list):
        cpu_total = float(data2['activity']['stat1'])
        cpu_count = 1
    else:
        for activity in data2['activity']:
            cpu_total += float(activity['stat1'])
            cpu_count += 1 
    avg_cpu = cpu_total/cpu_count
    host = Host.objects.filter(masterip=master).filter(sub_id = current).filter(floorid=floorid).filter(rackid=rackid).filter(hostid=prefix['id'])
    if host.count()==0:
        model_services.create_host(master,services.get_current_sub_id(),datacenter,floorid,prefix['rackId'],
        prefix['id'],prefix['name'],prefix['description'],prefix['hostType'],prefix['processorCount'],prefix['IPAddress'],
        data2['activity'][-1:][0]['timeStamp'],avg_cpu,cpu_count,cpu_total)
    else:
        host.update(cpu_usage=avg_cpu, responses=cpu_count, total_cpu = cpu_total)



from . import model_services
from tool.models import Host
import requests
from . import services

def get_datacenters():
    """ Find all datacenters found on master IP """

    services.check_master()
    master = services.get_master()
    url = services.datacenter_url(master)
    try:
        response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    except Exception: return 
    data = response.json()
    if data==None: return
    if isinstance(data['datacenter'], list):
        for i in data['datacenter']:
            model_services.create_datacenter(master,i['id'],i['name'],i['description'])
    else:
        model_services.create_datacenter(master,data['datacenter']['id'],data['datacenter']['name'],
        data['datacenter']['description'])


def get_floors(datacenter):
    """ Create floor objects from floors in specified datacenter 

    Args:
        datacenter (String): Datacenter ID 
    """

    get_datacenters()
    master = services.get_master()
    url=services.floor_url(master,datacenter)
    response = services.get_reponse(url)
    data = response.json()
    if data==None: return
    if isinstance(data['floor'], list):
        for i in data['floor']:
            model_services.create_floor(master,i['datacenterId'],i['id'],i['name'],i['description'])
    else:
        model_services.create_floor(master,data['floor']['datacenterId'],data['floor']['id'],
        data['floor']['name'],data['floor']['description'])


def get_racks(datacenter, floorid):
    """ Create rack objects from racks in specified datacenter and floor

    Args:
        datacenter (String): Datacenter ID
        floorid (String): Floor ID
    """

    get_floors(datacenter)
    master = services.get_master()
    url = services.rack_url(master, datacenter, floorid)
    response = services.get_reponse(url)
    data = response.json()
    if data==None: return
    if isinstance(data['rack'], list):
        for i in data['rack']:
            model_services.create_rack(master,datacenter,i['floorId'],i['id'],i['name'],i['description'], i['pdu'])
    else:
        model_services.create_rack(master,datacenter,data['rack']['floorId'],data['rack']['id'],
        data['rack']['name'],data['rack']['description'],data['rack']['pdu'])


def get_hosts(master, datacenter, floorid, rackid, startTime, endTime):
    """ Create host objects for specified datacenter, floor, rack and populate Host objects with 
        CPU usage metrics

    Args:
        master (String): IP address of master
        datacenter (String): Current datacenter ID
        floorid (String): Selected floor ID
        rackid (String): Selected rack ID
        hostid (String): Selected Host ID
        startTime (String): Start Time of period
        endTime (String): End time of period
    """

    get_racks(datacenter, floorid)
    current = services.get_current_sub_id()
    url=services.host_url(master,datacenter,floorid,rackid)
    response = services.get_reponse(url)
    data = response.json()
    if data==None: return 
    if not isinstance(data['host'], list):
        get_host_energy(data['host'],startTime,endTime,master,datacenter,floorid,current,rackid)
    else:
        for i in data['host']:
            get_host_energy(i,startTime,endTime,master,datacenter,floorid,current,rackid)



def get_host_energy(prefix, startTime,endTime,master,datacenter,floorid,current,rackid):
    """ Create Host objects and populate with CPU usage metrics

    Args:
        prefix (String): Incremental prefix
        url (String): URL to get respoinse from
        startTime (String): Start Time of period
        endTime (String): End Time of period
        master (String): IP address of master
        datacenter (String): current datacenter
        floorid (String): Selected floor ID
        current (String): sub_id of current datacenter
        rackid (String): Selected Rack ID
    """

    host = Host.objects.filter(masterip=master).filter(sub_id = current).filter(floorid=floorid).filter(rackid=rackid).filter(hostid=prefix['id'])
    if host.exists():
        new_url = services.cpu_usage_url(master,datacenter,floorid,rackid,prefix['id'],str(int(host.values().get()['lastTime'])+1),endTime)
        response = services.get_reponse(new_url)
        data2 = response.json()
        cpu_total = 0
        cpu_count = 0
        if data2==None:return
        if isinstance(data2['activity'], list): 
            for activity in data2['activity']:
                cpu_total += float(activity['stat1'])
                cpu_count += 1 
        else:
            updated_cpu_total = host.values().get()['total_cpu'] + float(data2['activity']['stat1'])
            updated_responses = host.values().get()['responses'] + 1
            updated_avg_cpu = updated_cpu_total/updated_responses
            host.update(cpu_usage=updated_avg_cpu, responses=updated_responses, total_cpu=updated_cpu_total, lastTime=data2['activity']['timeStamp'])
            return

        updated_responses = host.values().get()['responses'] + cpu_count
        updated_cpu_total = host.values().get()['total_cpu'] + cpu_total
        updated_avg_cpu = updated_cpu_total/updated_responses
        host.update(cpu_usage=updated_avg_cpu, responses=updated_responses, total_cpu=updated_cpu_total, lastTime=data2['activity'][-1:][0]['timeStamp'])

    new_url = services.cpu_usage_url(master,datacenter,floorid,rackid,prefix['id'],startTime,endTime)
    response = services.get_reponse(new_url)
    data2 = response.json()
    if data2==None:return
    cpu_total = 0
    cpu_count = 0
    if isinstance(data2['activity'], list): 
        for activity in data2['activity']:
            cpu_total += float(activity['stat1'])
            cpu_count += 1 
    else:
        cpu_total = float(data2['activity']['stat1'])
        cpu_count = 1
        
    avg_cpu = cpu_total/cpu_count
    model_services.create_host(master,services.get_current_sub_id(),datacenter,floorid,prefix['rackId'],
    prefix['id'],prefix['name'],prefix['description'],prefix['hostType'],prefix['processorCount'],prefix['IPAddress'],
    data2['activity'][-1:][0]['timeStamp'],avg_cpu,cpu_count,cpu_total)



from . import model_services
from tool.models import Host, AvailableDatacenters
import requests
from . import services

def get_available_datacenters():
    """ Find all datacenters found on master IP """

    services.check_master()
    master = services.get_master()
    url = services.datacenter_url(master)
    try:
        response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"},timeout=5)
    except Exception: return ConnectionRefusedError
    data = response.json()
    if data==None: return
    if isinstance(data['datacenter'], list):
        for i in data['datacenter']:
            model_services.create_available_datacenter(master,i['id'],i['name'],i['description'])
    else:
        model_services.create_available_datacenter(master,data['datacenter']['id'],data['datacenter']['name'],
        data['datacenter']['description'])

def get_hosts_energy(master, sub_id):
    startTime, endTime = services.get_start_end()
    for host in Host.objects.filter(sub_id=sub_id).filter(masterip=master).all().values():
        get_host_energy(host['hostid'],startTime,endTime,host['masterip'],host['datacenterid'],host['floorid'],host['sub_id'],host['rackid'])
        

def update_hosts_energy(master,sub_id):
    startTime, endTime = services.get_start_end()
    for host in Host.objects.filter(sub_id=sub_id).filter(masterip=master).all().values():
        update_host_energy(host['hostid'],startTime,endTime,host['masterip'],host['datacenterid'],host['floorid'],host['sub_id'],host['rackid'])
        
            
def update_host_energy(hostid,startTime,endTime,master,datacenter,floorid,sub_id,rackid):
    host = Host.objects.filter(masterip=master).filter(sub_id = sub_id).filter(floorid=floorid).filter(rackid=rackid).filter(hostid=hostid)

    if host.values().get()['cpu_last_response']!=None:
        startTime = str(int(host.values().get()['cpu_last_response'])+1)
    else:
        get_host_energy(hostid,startTime,endTime,master,datacenter,floorid,sub_id,rackid)
        return
    
    new_url = services.cpu_usage_url(master,datacenter,str(floorid),str(rackid),str(hostid),startTime,endTime)
    response = services.get_response(new_url)
    data2 = response.json()
    cpu_total = 0
    cpu_count = 0
    if data2==None:return
    if isinstance(data2['activity'], list): 
        for activity in data2['activity']:
            cpu_total += float(activity['stat1'])
            cpu_count += 1 
        updated_responses = host.values().get()['cpu_responses'] + cpu_count
        updated_cpu_total = host.values().get()['total_cpu'] + cpu_total
        updated_avg_cpu = updated_cpu_total/updated_responses
        host.update(cpu_usage=updated_avg_cpu, cpu_responses=updated_responses, total_cpu=updated_cpu_total, cpu_last_response=data2['activity'][-1:][0]['timeStamp'])
    else:
        updated_responses = host.values().get()['cpu_responses'] + 1 
        updated_cpu_total = host.values().get()['total_cpu'] + float(data2['activity']['stat1'])
        updated_avg_cpu = updated_cpu_total/updated_responses
        host.update(cpu_usage=updated_avg_cpu, cpu_responses=updated_responses, total_cpu=updated_cpu_total, cpu_last_response=data2['activity']['timeStamp'])

def get_host_energy(hostid,startTime,endTime,master,datacenter,floorid,current,rackid):

    host = Host.objects.filter(masterip=master).filter(sub_id = current).filter(floorid=floorid).filter(rackid=rackid).filter(hostid=hostid)
    new_url = services.cpu_usage_url(master,datacenter,str(floorid),str(rackid),str(hostid),startTime,endTime)
    response = services.get_response(new_url)
    data2 = response.json()
    if data2==None:return
    cpu_total = 0
    cpu_count = 0
    if isinstance(data2['activity'], list): 
        for activity in data2['activity']:
            cpu_total += float(activity['stat1'])
            cpu_count += 1 
        avg_cpu = cpu_total/cpu_count
        host.update(cpu_usage=avg_cpu, cpu_responses=cpu_count, total_cpu=cpu_total, cpu_last_response=data2['activity'][-1:][0]['timeStamp'])
    else:
        cpu_total = float(data2['activity']['stat1'])
        cpu_count = 1
        avg_cpu = cpu_total/cpu_count
        host.update(cpu_usage=avg_cpu, cpu_responses=cpu_count, total_cpu=cpu_total, cpu_last_response=data2['activity']['timeStamp'])
    
def find_available_hosts(master, datacenter,sub_id):
    """ Finds all racks in the currently selected datacenter and specified floor

    Args:
        master (String): IP address of master
        current (String): Current datacenter ID
        floorid (String): Selected floor ID

    Returns:
        list[String]: list of all racks in specified datacenter and floor
    """

    url = "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/allhosts/"
    response = services.get_response(url)
    data = response.json()
    if data==None:return
    if isinstance(data['hostExtended'], list): 
        for host in data['hostExtended']:
            # model_services.create_datacenter(master,sub_id,host['datacenterId'],host['datacenterName'],host['datacenterDescription'])
            
            model_services.create_floor(master,sub_id,host['datacenterId'],host['floorId'],host['floorName'],host['floorDescription'])
            
            model_services.create_rack(master,sub_id,host['datacenterId'],host['floorId'],host['rackId'],host['rackName'],host['rackDescription'])
            
            model_services.create_empty_host(master,sub_id,host['datacenterId'],host['floorId'],host['rackId'],host['hostId'],
                                                host['hostName'],host['hostDescription'],host['hostType'],
                                                host['processorCount'],host['IPAddress'])
            




from . import model_services
from tool.models import Host, ConfiguredDataCenters
import requests
from . import services
import time
def get_available_datacenters():
    """ Finds all available datacenters on the master IP address. 

    Returns:
        ConnectionRefusedError: if there are no datacenters available an Error is thrown
    """
    
    services.check_master()
    master = services.get_master()
    url = services.datacenter_url(master)
    try:
        response = requests.get(url,
                                headers={'Content-Type': 'application/json', 'Accept': "application/json"},
                                timeout=5
                                )
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
    """ Gets all available hosts in the datacenter and individually gets their energy usage 

    Args:
        master (String): IP Address of master server
        sub_id (String): sub_id of the active datacenter

    Returns:
        Exception: If no datacenters are configured it will throw an error
    """
    
    try: 
        startTime, endTime = services.get_start_end()
    except: return ConfiguredDataCenters.DoesNotExist
    for host in Host.objects.filter(sub_id=sub_id).filter(masterip=master).all().values():
        get_host_energy(host['hostid'],startTime,endTime,host['masterip'],host['datacenterid'],
                        host['floorid'],host['sub_id'],host['rackid'])
        

def update_hosts_energy(master,sub_id):
    """ Gets all available hosts in the datacenter and individually gets their energy usage - 
    updates instead of create

    Args:
        master (String): IP Address of master server
        sub_id (String): sub_id of the active datacenter

    Returns:
        Exception: If no datacenters are configured it will throw an error
    """
    
    try: 
        startTime, endTime = services.get_start_end()
    except: return ConfiguredDataCenters.DoesNotExist
    for host in Host.objects.filter(sub_id=sub_id).filter(masterip=master).all().values():
        update_host_energy(host['hostid'],startTime,endTime,host['masterip'],
                           host['datacenterid'],host['floorid'],host['sub_id'],host['rackid'])
        
            
def update_host_energy(hostid,startTime,endTime,master,datacenter,floorid,sub_id,rackid):
    """ Finds the last time host energy was updated and sets that as the start time for 
        a new API call. Results are appended to the existing object

    Args:
        hostid (String): ID of selected host
        startTime (String): UNIX Date (epoch)
        endTime (String): UNIX Date (epoch)
        master (String): IP Address of master
        datacenter (String): Datacenter ID
        floorid (String): Floor ID
        sub_id (String): Sub_id of datacenter (instance)
        rackid (String): Rack ID
    """
    
    host = get_host(master,sub_id,floorid,rackid,hostid)
    
    if get_last_cpu_response(host)!=None:
        startTime = str(int(host.values().get()['cpu_last_response'])+1)
    else:
        get_host_energy(hostid,startTime,endTime,master,datacenter,floorid,sub_id,rackid)
        return
    
    s = time.process_time()
    new_url = services.cpu_usage_url(master,datacenter,str(floorid),str(rackid),str(hostid),startTime,endTime)
    response = services.get_response(new_url)
    data2 = response.json()
    # print(time.process_time() - s)
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
        host.update(cpu_usage=updated_avg_cpu, cpu_responses=updated_responses, 
                    total_cpu=updated_cpu_total, cpu_last_response=data2['activity'][-1:][0]['timeStamp'])
    else:
        updated_responses = host.values().get()['cpu_responses'] + 1 
        updated_cpu_total = host.values().get()['total_cpu'] + float(data2['activity']['stat1'])
        updated_avg_cpu = updated_cpu_total/updated_responses
        host.update(cpu_usage=updated_avg_cpu, cpu_responses=updated_responses, 
                    total_cpu=updated_cpu_total, cpu_last_response=data2['activity']['timeStamp'])

def get_host_energy(hostid,startTime,endTime,master,datacenter,floorid,current,rackid):
    """ Calling Papillon API with the start and end times that were specified by the user 
        when configuring their datacenter. Energy of the specified host is calculated and 
        stored in a Host model

    Args:
        hostid (String): ID of selected host
        startTime (String): UNIX Date (epoch)
        endTime (String): UNIX Date (epoch)
        master (String): IP Address of master
        datacenter (String): Datacenter ID
        floorid (String): Floor ID
        sub_id (String): Sub_id of datacenter (instance)
        rackid (String): Rack ID
    """
    
    host = get_host(master,current,floorid,rackid,hostid)
    s = time.process_time()
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
        host.update(cpu_usage=avg_cpu, cpu_responses=cpu_count, total_cpu=cpu_total, 
                    cpu_last_response=data2['activity'][-1:][0]['timeStamp'])
    else:
        cpu_total = float(data2['activity']['stat1'])
        cpu_count = 1
        avg_cpu = cpu_total/cpu_count
        host.update(cpu_usage=avg_cpu, cpu_responses=cpu_count, total_cpu=cpu_total, 
                    cpu_last_response=data2['activity']['timeStamp'])
    
def find_available_hosts(master, datacenter,sub_id):
    """ Using the url extension 'allhosts' we can find all hosts in the datacenter, including
        information about the parent rack/ floor/ datacenter. This information is stored in
        respective models.

    Args:
        master (String): Master IP address
        datacenter (String): Datacenter ID
        sub_id (String): selected instance of your datacenter

    Returns:
        exception: If the endpoint cannot be reached an exception is thrown
    """

    url = "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/allhosts/"
    response = services.get_response(url)
    try:
        data = response.json()
    except: return ConnectionRefusedError
    if data==None:return
    if isinstance(data['hostExtended'], list): 
        for host in data['hostExtended']:
            
            model_services.create_floor(master,sub_id,host['datacenterId'],host['floorId']
                                        ,host['floorName'],host['floorDescription'])
            
            model_services.create_rack(master,sub_id,host['datacenterId'],host['floorId'],
                                       host['rackId'],host['rackName'],host['rackDescription'])
            
            model_services.create_empty_host(master,sub_id,host['datacenterId'],host['floorId'],host['rackId'],
                                             host['hostId'],host['hostName'],host['hostDescription'],
                                             host['hostType'],host['processorCount'],host['IPAddress'])
            

def get_host(master,sub_id,floorid,rackid,hostid):
    """ Using the identifiers for a host, this function returns that host object from the 
        database

    Args:
        master (String): Master IP address
        sub_id (String): Instance of datacenter
        floorid (String): Floor ID where host is
        rackid (String): Rack ID where host is
        hostid (String): Host ID

    Returns:
        exception: If no host in the specified location exists, an exception is thrown
    """
    
    try:
        return Host.objects.filter(masterip=master).filter(sub_id = sub_id).filter(
            floorid=floorid).filter(rackid=rackid).filter(hostid=hostid)
    except: return Host.DoesNotExist


def get_last_cpu_response(host):
    """ Using a host instance, the last time a CPU response was recorded is retrieved in this 
        function

    Args:
        host (String): Host object

    Returns:
        exception : If host object does not exist (ie. None object)
    """
    
    try:
        return host.values().get()['cpu_last_response']
    except: return Host.DoesNotExist
    
    
    
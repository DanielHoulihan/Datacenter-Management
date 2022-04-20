from tool.models import Host, ConfiguredDataCenters
from . import services, model_services
import time
def get_hosts_power(master, sub_id):
    """  call get_host_power for all the Host objects in the selected datacenter

    Args:
        master (String): IP Address of master server
        sub_id (String): Selected datacenter instance

    Returns:
        exception: Object does not exist
    """
    
    try: 
        startTime, endTime = services.get_start_end()
    except: return ConfiguredDataCenters.DoesNotExist
    for host in Host.objects.filter(sub_id=sub_id).filter(masterip=master).all().values():
        get_host_power(host['masterip'],host['sub_id'],host['datacenterid'],host['floorid'],
                       host['rackid'],host['hostid'],startTime,endTime)
        
def update_hosts_power(master, sub_id):
    """  call update_host_power for all the Host objects in the selected datacenter

    Args:
        master (String): IP Address of master server
        sub_id (String): Selected datacenter instance

    Returns:
        exception: Object does not exist
    """
    
    try: 
        startTime, endTime = services.get_start_end()
    except: return ConfiguredDataCenters.DoesNotExist
    for host in Host.objects.filter(sub_id=sub_id).filter(masterip=master).all().values():
        update_host_power(host['masterip'],host['sub_id'],host['datacenterid'],
                          host['floorid'],host['rackid'],host['hostid'],startTime,endTime)     
        
def get_host_power(master, sub_id, datacenter, floorid, rackid, hostid, startTime, endTime):
    """ Generate a url to reach the Papillon API endpoint and find the hosts power information. 
        Use these to generate metrics and update the host.

    Args:
        master (String): IP Address of master 
        sub_id (String): _description_
        datacenter (String): _description_
        floorid (String): _description_
        rackid (String): _description_
        hostid (String): _description_
        startTime (String): _description_
        endTime (String): _description_
    """
        
    host = Host.objects.filter(masterip=master).filter(sub_id = sub_id).filter(
        floorid=floorid).filter(rackid=rackid).filter(hostid=hostid)
    s = time.process_time()
    url = services.power_url(master, datacenter, str(floorid), str(rackid), str(hostid), startTime, endTime)
    response = services.get_response(url)
    data = response.json()
    # print(time.process_time() - s)
    if data != None: 
        total_watts = 0
        minutes = 0
        if isinstance(data['power'], list):
            lastTime = data['power'][-1]['timeStamp']
            for power in data['power']:
                total_watts += float(power['power'])
                minutes+=1
        else:
            lastTime = data['power']['timeStamp']
            minutes = 1 
            total_watts = float(data['power']['power'])

        hours = minutes/60
        kWh = total_watts/hours/1000
        ops_cons_3 =24*7*kWh*52*3
        pue = services.get_pue()
        carbon_conversion = services.get_carbon_conversion()
        energy_cost = services.get_energy_cost()
        op_cost_3 = ops_cons_3*pue*energy_cost
        carbon_footprint_3=ops_cons_3*carbon_conversion
        kWh_consumed = total_watts/1000
        
        app_waste_cost_3 = op_cost_3 * (1-host.values().get()['cpu_usage']/100)
        
        host.update(carbon_footprint_3=carbon_footprint_3,
                power_responses=minutes,kWh_consumed=kWh_consumed,ops_cons_3=ops_cons_3,
                op_cost_3=op_cost_3,power_last_response=lastTime,total_watt_hour=total_watts,
                app_waste_cost_3 = app_waste_cost_3
        )

def update_host_power(master, sub_id, datacenter, floorid, rackid, hostid, startTime, endTime):
    """ If a host exists with a last time host power was updated, the host is updated with a new start time

    Args:
        master (String): IP Address of master
        sub_id (String): Datcenter instance
        datacenter (String): Datacenter ID
        floorid (Integer): Floor ID
        rackid (Integer): Rack ID
        hostid (Integer): Host ID
        startTime (String): UNIX start time as a string 
        endTime (String): UNIX end time as a string 

    Returns:
        exception: if no Host object exists we throw an exception.
    """
    
    host = Host.objects.filter(masterip=master).filter(sub_id = sub_id).filter(
        floorid=floorid).filter(rackid=rackid).filter(hostid=hostid)
    if not host.exists(): return Host.DoesNotExist
    if host.values().get()['power_last_response']!=None:
        startTime = str(int(host.values().get()['power_last_response'])+1)
    else: 
        get_host_power(master, sub_id, datacenter, floorid, rackid, hostid, startTime, endTime)
        return
    s = time.process_time()
    url = services.power_url(master, datacenter, str(floorid), str(rackid), str(hostid), startTime, endTime)
    response = services.get_response(url)
    data = response.json()
    # print(time.process_time() - s)
    if data != None: 
        total_watts = 0
        minutes = 0
        if isinstance(data['power'], list):
            lastTime = data['power'][-1]['timeStamp']
            for power in data['power']:
                total_watts += float(power['power'])
                minutes+=1
        else:
            lastTime = data['power']['timeStamp']
            minutes = 1 
            total_watts = float(data['power']['power']) 
                
        updated_minutes = minutes + host.values().get()['power_responses']
        updated_watts = total_watts + host.values().get()['total_watt_hour']
        hours = updated_minutes/60
        avg_Wh = updated_watts/hours/1000
        ops_cons_3 = calculate_ops_cons_3(avg_Wh)
        pue = services.get_pue()
        carbon_conversion = services.get_carbon_conversion()
        energy_cost = services.get_energy_cost()
        op_cost_3 = calculate_op_cost_3(ops_cons_3, pue, energy_cost)
        carbon_footprint_3=calculate_carbon_footprint_3(ops_cons_3, carbon_conversion)
        kWh_consumed = updated_watts/1000
        
        if host.values().get()['capital']!=None:
            tco_3=int(host.values().get()['capital'])+(energy_cost*ops_cons_3)
            
            host.update(capital=int(host.values().get()['capital']),TCO=tco_3,
                        carbon_footprint_3=carbon_footprint_3,power_responses=updated_minutes,
                        kWh_consumed=kWh_consumed,ops_cons_3=ops_cons_3,op_cost_3=op_cost_3,
                        power_last_response=lastTime,total_watt_hour=updated_watts
            )
        else:
            host.update(carbon_footprint_3=carbon_footprint_3,
                    power_responses=updated_minutes,kWh_consumed=kWh_consumed,ops_cons_3=ops_cons_3,
                    op_cost_3=op_cost_3,power_last_response=lastTime,total_watt_hour=updated_watts
            )
    
    
def calculate_tco(master, sub_id, floor, rack, host, capital):
    """ Calculate Total Cost of Ownership of specified host. 

    Args:
        master (String): IP Address of master server
        sub_id (String): Datacenter instance selected
        floor (Integer): Floor ID
        rack (Integer): Rack ID
        host (Integer): Host ID
        capital (Integer): Capital cost of server (specified by user)

    Returns:
        exception: If no Host objects exist
    """
    
    host = Host.objects.filter(masterip=master).filter(sub_id = sub_id).filter(
        floorid=floor).filter(rackid=rack).filter(hostid=host)
    if not host.exists(): return Host.DoesNotExist
    ops_cons_3 = host.values().get()['ops_cons_3']
    energy_cost = services.get_energy_cost()
    try:
        tco_3 = int(capital)+(energy_cost*ops_cons_3)
        host.update(TCO=tco_3,capital=capital)
    except: return
    
    
def calculate_ops_cons_3(kWh):
    """ Cqlculates Operational Consumption over a 3 year period (extrapolated)

    Args:
        kWh (Float): Average kWh consumed by the host

    Returns:
        Float: Operational Consumption for 3 years
    """
    
    return  24*7*kWh*52*3

def calculate_op_cost_3(ops_cons_3, pue, energy_cost):
    """ Calculates Operational Cost for a 3 year period (extrapolated)

    Args:
        ops_cons_3 (Float): Operational Consumption for 3 years
        pue (Float): Power Usage Effectiveness
        energy_cost (Float): Energy Cost for your datacenter

    Returns:
        Float: Operational Cost for 3 years
    """
    
    return ops_cons_3*pue*energy_cost
    
def calculate_carbon_footprint_3(ops_cons_3,carbon_conversion):
    """ Calculates Carbon Foorptint of datacenter for a 3 year period

    Args:
        ops_cons_3 (Float): Operational Consumption for 3 years
        carbon_conversion (Float): Carbon conversion (kgCo2 / kWh)

    Returns:
        Float: kgCo2 produced by host 
    """
    
    return ops_cons_3*carbon_conversion




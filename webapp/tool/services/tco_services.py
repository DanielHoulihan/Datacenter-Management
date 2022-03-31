from tool.models import Host
from . import services, model_services

def get_hosts_power(master, sub_id):

    startTime, endTime = services.get_start_end()
    for host in Host.objects.filter(sub_id=sub_id).filter(masterip=master).all().values():
        get_host_power(host['masterip'],host['sub_id'],host['datacenterid'],host['floorid'],host['rackid'],host['hostid'],startTime,endTime)
        
def update_hosts_power(master, sub_id):

    startTime, endTime = services.get_start_end()
    for host in Host.objects.filter(sub_id=sub_id).filter(masterip=master).all().values():
        update_host_power(host['masterip'],host['sub_id'],host['datacenterid'],host['floorid'],host['rackid'],host['hostid'],startTime,endTime)     
        
def get_host_power(master, sub_id, datacenter, floorid, rackid, hostid, startTime, endTime):

    host = Host.objects.filter(masterip=master).filter(sub_id = sub_id).filter(floorid=floorid).filter(rackid=rackid).filter(hostid=hostid)
    url = services.power_url(master, datacenter, str(floorid), str(rackid), str(hostid), startTime, endTime)
    response = services.get_response(url)
    data = response.json()
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
        # tco_3=int(capital)+(energy_cost*ops_cons_3)
        kWh_consumed = total_watts/1000
        
        app_waste_cost_3 = op_cost_3 * (1-host.values().get()['cpu_usage']/100)
        
        host.update(carbon_footprint_3=carbon_footprint_3,
                power_responses=minutes,kWh_consumed=kWh_consumed,ops_cons_3=ops_cons_3,
                op_cost_3=op_cost_3,power_last_response=lastTime,total_watt_hour=total_watts,
                app_waste_cost_3 = app_waste_cost_3
        )

def update_host_power(master, sub_id, datacenter, floorid, rackid, hostid, startTime, endTime):
    host = Host.objects.filter(masterip=master).filter(sub_id = sub_id).filter(floorid=floorid).filter(rackid=rackid).filter(hostid=hostid)

    if host.values().get()['power_last_response']!=None:
        startTime = str(int(host.values().get()['power_last_response'])+1)
    else: 
        get_host_power(master, sub_id, datacenter, floorid, rackid, hostid, startTime, endTime)
        return
 
    url = services.power_url(master, datacenter, str(floorid), str(rackid), str(hostid), startTime, endTime)
    response = services.get_response(url)
    data = response.json()
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
        kWh = updated_watts/hours/1000
        ops_cons_3 =24*7*kWh*52*3
        pue = services.get_pue()
        carbon_conversion = services.get_carbon_conversion()
        energy_cost = services.get_energy_cost()
        op_cost_3 = ops_cons_3*pue*energy_cost
        carbon_footprint_3=ops_cons_3*carbon_conversion
        kWh_consumed = updated_watts/1000
        
        if host.values().get()['capital']!=None:
            tco_3=int(host.values().get()['capital'])+(energy_cost*ops_cons_3)
            
            host.update(capital=int(host.values().get()['capital']),TCO=tco_3,carbon_footprint_3=carbon_footprint_3,
                    power_responses=updated_minutes,kWh_consumed=kWh_consumed,ops_cons_3=ops_cons_3,
                    op_cost_3=op_cost_3,power_last_response=lastTime,total_watt_hour=updated_watts
            )
        else:
            host.update(carbon_footprint_3=carbon_footprint_3,
                    power_responses=updated_minutes,kWh_consumed=kWh_consumed,ops_cons_3=ops_cons_3,
                    op_cost_3=op_cost_3,power_last_response=lastTime,total_watt_hour=updated_watts
            )
    
    
def calculate_tco(master, sub_id, floor, rack, host, capital):
    host = Host.objects.filter(masterip=master).filter(sub_id = sub_id).filter(floorid=floor).filter(rackid=rack).filter(hostid=host)
    ops_cons_3 = host.values().get()['ops_cons_3']
    energy_cost = services.get_energy_cost()
    try:
        tco_3 = int(capital)+(energy_cost*ops_cons_3)
        host.update(TCO=tco_3,capital=capital)
    except: return
    
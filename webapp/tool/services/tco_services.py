from tool.models import HostEnergy
from . import services

def find_available_floors(master, current):
    """ Finds all floors in the currently selected datacenter 

    Args:
        master (String): IP address of master 
        current (String): Current datacenter ID

    Returns:
        list[String]: list of all floors in specified datacenter
    """    

    url = services.create_url(master, current)
    response = services.get_reponse(url)
    data = response.json()
    floors = []
    if data!=None: 
        if isinstance(data['floor'], list):
            for i in data['floor']:
                floors.append(i['id'])  
        else:
            floors.append(data['floor']['id'])
    return floors


def find_available_racks(master, current, floorid):
    """ Finds all racks in the currently selected datacenter and specified floor

    Args:
        master (String): IP address of master
        current (String): Current datacenter ID
        floorid (String): Selected floor ID

    Returns:
        list[String]: list of all racks in specified datacenter and floor
    """

    url = services.create_url(master, current, floorid)
    response = services.get_reponse(url)
    data = response.json()
    racks = []
    if data!=None: 
        if isinstance(data['rack'], list):
            for i in data['rack']:
                racks.append(i['id'])  
        else:
            racks.append(data['rack']['id'])
            
    return racks

            
def find_all_available_hosts(master, current):
    """ Finds all floors, racks, hosts in selected datacenter

    Args:
        master (String): IP address of master
        current (String): Current datacenter ID
    """

    for floor in find_available_floors(master, current):
        for rack in find_available_racks(master, current, floor):
            get_hosts_tco(master, current, floor, rack)



def get_hosts_tco(master, datacenter, floorid, rackid):
    """ Creates HostEnergy objects in specified rack

    Args:
        master (String): IP address of master
        current (String): Current datacenter ID
        floorid (String): Selected floor ID
        rackid (String): Selected rack ID
    """

    current = services.get_current_sub_id()
    url = services.create_url(master, datacenter, floorid, rackid)
    response = services.get_reponse(url)
    data = response.json()
    if data!=None: 
        if isinstance(data['host'], list):
            for i in data['host']:
                HostEnergy.objects.get_or_create(
                    masterip = master,
                    sub_id = current,
                    datacenterid = datacenter,
                    floorid = floorid,
                    rackid = i['rackId'],
                    hostid = i['id'],
                    ipaddress = i['IPAddress']
                )
        else:
            HostEnergy.objects.get_or_create(
                masterip = master,
                sub_id = current,
                datacenterid = datacenter,
                floorid = floorid,
                rackid = data['host']['rackId'],
                hostid = data['host']['id'],
                ipaddress = data['host']['IPAddress']
            )


def get_energy_usage(master, datacenter, floorid, rackid, hostid, startTime, endTime, capital):
    """ Calculates TCO for specified host and uipdates existing HostEnergy Object

    Args:
        master (String): IP address of master
        current (String): Current datacenter ID
        floorid (String): Selected floor ID
        rackid (String): Selected rack ID
        hostid (String): Selected Host ID
        startTime (String): Start Time of period
        endTime (String): End time of period
        capital (Integer): Capital cost of selected host
    """
    current = services.get_current_sub_id()
    url = services.create_url(master, datacenter, floorid, rackid, hostid, startTime, endTime)
    response = services.get_reponse(url)
    data = response.json()
    minutes=0
    total_watts=0
    if data != None:

        total_watts = 0
        minutes = 0
        for power in data['power']:
            total_watts += float(power['power'])
            minutes+=1

        hours = minutes/60
        watt_hour = total_watts/hours
        kWh = total_watts/hours/1000
        ops_cons_3 =24*7*kWh*52*3
        pue = services.get_pue()
        carbon_conversion = services.get_carbon_conversion()
        energy_cost = services.get_energy_cost()
        op_cost_3 = ops_cons_3*pue*energy_cost
        carbon_footprint_3=ops_cons_3*carbon_conversion
        tco_3=int(capital)+(energy_cost*ops_cons_3)
        kWh_consumed = total_watts/1000

        host = HostEnergy.objects.filter(masterip=master).filter(sub_id = current).filter(floorid=floorid).filter(rackid=rackid).filter(hostid=hostid)
        host.update(TCO=tco_3,total_watt_hour=total_watts, minutes = minutes, hours = hours, avg_kWh=kWh, avg_watt_hour = watt_hour, capital=capital, ops_cons_3=ops_cons_3, carbon_footprint_3=carbon_footprint_3, op_cost_3=op_cost_3, kWh_consumed=kWh_consumed)


import requests
import time
from . import asset_services
from tool.models import ConfiguredDataCenters, HostEnergy, CurrentDatacenter
from . import services

def find_available_floors(master, current):
    url = "http://"+master+":8080/papillonserver/rest/datacenters/"+current+"/floors/"
    response = services.get_reponse(url)
    # response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
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
    url = "http://"+master+":8080/papillonserver/rest/datacenters/"+current+"/floors/"+floorid+"/racks"
    response = services.get_reponse(url)
    # response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
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
    for floor in find_available_floors(master, current):
        for rack in find_available_racks(master, current, floor):
            get_hosts_tco(master, current, floor, rack)


                

def get_hosts_tco(master, datacenter, floorid, rackid):
    current = services.get_current_sub_id()
    url = "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/floors/"+floorid+"/racks/"+rackid+"/hosts"
    response = services.get_reponse(url)
    # response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
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
    current = services.get_current_sub_id()
    url = "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/floors/"+floorid+"/racks/"+rackid+"/hosts/"+hostid+"/power?starttime="+startTime+"&endtime="+endTime
    response = services.get_reponse(url)
    # response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
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


from . import tco_services, services
from tool.models import ConfiguredDataCenters, HostEnergy, CurrentDatacenter
import requests
import time
from collections import defaultdict
import pandas as pd
from functools import reduce


def get_hosts(master, current_sub):

    startTime = ConfiguredDataCenters.objects.all().filter(sub_id = services.get_current_sub_id()).values().get()['startTime']
    startTime = str(int(time.mktime(startTime.timetuple())))
    if ConfiguredDataCenters.objects.all().filter(sub_id = services.get_current_sub_id()).values().get()['endTime']==None:
        endTime = str(int(time.time()))
    else:
        endTime = ConfiguredDataCenters.objects.all().filter(sub_id = services.get_current_sub_id()).values().get()['endTime']
        endTime = str(int(time.mktime(endTime.timetuple())))

    available_hosts = HostEnergy.objects.filter(masterip=master).filter(sub_id=current_sub).all().values()

    p=[services.unix_range(startTime,endTime)]

    for host in available_hosts:
        url = "http://"+host['masterip']+":8080/papillonserver/rest/datacenters/"+host['datacenterid']+"/floors/"+str(host['floorid'])+"/racks/"+str(host['rackid'])+"/hosts/"+str(host['hostid'])+"/power?starttime="+startTime+"&endtime="+endTime
        response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
        data = response.json()
        start=int(startTime)

        
        print(host['hostid'])
        energy = defaultdict(list)
        temp = 0
        if data!=None:
            for power in data['power']:
                if int(power['timeStamp']) >= start:
                    if int(power['timeStamp']) >= start+86400:
                        start+=86400
                        temp+=float(power['power'])
                        continue
                    energy[start].append(float(power['power']))

                    
            energy[list(energy.keys())[0]].append(temp)
            summed = {k: sum(v) for (k, v) in energy.items()}
            df = pd.DataFrame(summed.items(), columns=['day', host['hostid']])
            p.append(df)

    hosts = reduce(lambda x, y: pd.merge(x, y, on = 'day', how='left'), p)
    hosts['day'] = pd.to_datetime(hosts['day'],unit='s')
    return hosts


    # current = services.get_current_sub_id()
    # url = "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/floors/"+floorid+"/racks/"+rackid+"/hosts/"+hostid+"/power?starttime="+startTime+"&endtime="+endTime
    # response = requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    # data = response.json()
    # minutes=0
    # total_watts=0
    # if data != None:

    #     total_watts = 0
    #     minutes = 0
    #     for power in data['power']:
    #         total_watts += float(power['power'])
    #         minutes+=1

    #     hours = minutes/60
    #     watt_hour = total_watts/hours
    #     kWh = total_watts/hours/1000
    #     ops_cons_3 =24*7*kWh*52*3
    #     pue = services.get_pue()
    #     carbon_conversion = services.get_carbon_conversion()
    #     energy_cost = services.get_energy_cost()
    #     op_cost_3 = ops_cons_3*pue*energy_cost
    #     carbon_footprint_3=ops_cons_3*carbon_conversion
    #     tco_3=int(capital)+(energy_cost*ops_cons_3)

    #     host = HostEnergy.objects.filter(masterip=master).filter(sub_id = current).filter(floorid=floorid).filter(rackid=rackid).filter(hostid=hostid)
    #     host.update(TCO=tco_3,total_watts=total_watts, minutes = minutes, hours = hours, kWh=kWh, watt_hour = watt_hour, capital=capital, ops_cons_3=ops_cons_3, carbon_footprint_3=carbon_footprint_3, op_cost_3=op_cost_3)    



# 86400
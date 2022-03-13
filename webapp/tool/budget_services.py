from . import tco_services, services
from tool.models import ConfiguredDataCenters, HostEnergy, CurrentDatacenter
import requests
import time
from collections import defaultdict
import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt
import mpld3

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
        minutes=0
        if data!=None:
            for power in data['power']:
                if int(power['timeStamp']) >= start:
                    if int(power['timeStamp']) >= start+86400:
                        start+=86400
                        temp+=float(power['power'])
                        minutes+=1
                        continue
                    energy[start].append(float(power['power']))
                    minutes+=1

                    
            energy[list(energy.keys())[0]].append(temp)
            summed = {k: sum(v) for (k, v) in energy.items()}
            df = pd.DataFrame(summed.items(), columns=['day', host['hostid']])
            df[host['hostid']] = df[host['hostid']]/1000
            p.append(df)

    hosts = reduce(lambda x, y: pd.merge(x, y, on = 'day', how='left'), p)
    hosts['day'] = pd.to_datetime(hosts['day'],unit='s')
    hosts = hosts.fillna(0)
    hosts = hosts[hosts['day']<=pd.to_datetime(int(time.time()),unit='s')]
    for col in hosts.columns[1:]:
        hosts[col] = hosts[col].cumsum()
    hosts['Total'] = hosts[hosts.columns[1:]].sum(axis=1)
    return hosts[hosts.columns[:-1]], hosts[[hosts.columns[0], hosts.columns[-1]]]


import matplotlib.dates as mdates

def plot_usage(table):
    plt.switch_backend('Agg') 
    startTime, endTime = services.get_start_end()
    plt.figure(figsize=(5,4))
    ax = plt.axes()
    
    plt.xlim([pd.to_datetime(startTime,unit='s'), pd.to_datetime(endTime,unit='s')])
    for column in table.columns[1:]:
        plt.plot(table['day'], table[column], label=column)
    plt.legend()
    plt.ylabel('kWh', fontsize=16)
    plt.xlabel('Date', fontsize=18)
    fig2 = plt.gcf()
    g2 = mpld3.fig_to_html(fig2)
    return g2


def carbon_usage(table):
    carbon = services.get_carbon_conversion()
    for col in table.columns[1:]:
        table[col] = table[col]*carbon
    return table

def cost_estimate(table):
    cost = services.get_energy_cost()
    for col in table.columns[1:]:
        table[col] = table[col]*cost
    return table

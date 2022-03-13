from . import tco_services, services
from tool.models import ConfiguredDataCenters, HostEnergy, CurrentDatacenter
import requests
import time
from collections import defaultdict
import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt
import mpld3
import base64
import io
import matplotlib.dates as mdates 



plt.switch_backend('Agg') 

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


def plot_usage(table):
    startTime, endTime = services.get_start_end()
    startTime=int(startTime)-10000
    fig, ax = plt.subplots(figsize=(6,3))
    for column in table.columns[1:]:
        ax.plot(table['day'], table[column], label=column, markerfacecolor='blue')
    plt.xlim([pd.to_datetime(startTime,unit='s'), pd.to_datetime(endTime,unit='s')])  
    # plt.axhline(y=20, c='r')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    x = (pd.to_datetime(endTime,unit='s') - pd.to_datetime(startTime,unit='s')).days/4
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=int(x)))
    buf = io.BytesIO()
    fig.savefig(buf)
    return base64.b64encode(buf.getvalue()).decode()


    # startTime, endTime = services.get_start_end()
    # startTime=int(startTime)-10000
    # plt.figure(figsize=(5,4))    
    # plt.xlim([pd.to_datetime(startTime,unit='s'), pd.to_datetime(endTime,unit='s')])   
    # for column in table.columns[1:]:
    #     plt.plot(table['day'], table[column], label=column)
    # plt.legend(loc='upper left')
    # plt.ylabel('kWh', fontsize=16)
    # plt.xlabel('Date', fontsize=18)
    # plt.gca().set_ylim(ymin=0)
    # fig = plt.gcf()

    # buf = io.BytesIO()
    # fig.savefig(buf,format='png')
    # string = base64.b64encode(buf.read())
    # uri=urllib.parse.quote(string)
    # return uri
    # g = mpld3.fig_to_html(fig)
    # return g

def plot_carbon_total(table):
    startTime, endTime = services.get_start_end()
    startTime=int(startTime)-10000
    fig, ax = plt.subplots(figsize=(5,3))
    for column in table.columns[1:]:
        ax.plot(table['day'], table[column], label=column, markerfacecolor='blue')
    plt.xlim([pd.to_datetime(startTime,unit='s'), pd.to_datetime(endTime,unit='s')])  
    # plt.axhline(y=20, c='r')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    x = (pd.to_datetime(endTime,unit='s') - pd.to_datetime(startTime,unit='s')).days/4
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=int(x)))
    plt.axhline(y=services.get_budget(), c='r')
    buf = io.BytesIO()
    fig.savefig(buf)
    return base64.b64encode(buf.getvalue()).decode()

    # startTime, endTime = services.get_start_end()
    # startTime=int(startTime)-10000
    # table['Budget']=services.get_budget()
    # plt.figure(figsize=(5,4))    
    # plt.xlim([pd.to_datetime(startTime,unit='s'), pd.to_datetime(endTime,unit='s')])   
    # # plt.ylim(0,services.get_budget()) 
    # for column in table.columns[1:]:
    #     plt.plot(table['day'], table[column], label=column)
    # plt.legend(loc='upper left')
    # plt.ylabel('kWh', fontsize=16)
    # plt.xlabel('Date', fontsize=18)
    # plt.gca().set_ylim(ymin=0)  
    # fig2 = plt.gcf()
    # g = mpld3.fig_to_html(fig2)
    # return g


def carbon_usage(table):
    temp = table.copy()
    carbon = services.get_carbon_conversion()
    for col in temp.columns[1:]:
        temp[col] = temp[col]*carbon
    return temp

def cost_estimate(table):
    temp = table.copy()
    cost = services.get_energy_cost()
    for col in temp.columns[1:]:
        temp[col] = temp[col]*cost
    return temp

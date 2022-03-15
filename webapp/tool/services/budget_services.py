from . import services
from tool.models import HostEnergy
import time
from collections import defaultdict
import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt
import base64
import io
import matplotlib.dates as mdates 



plt.switch_backend('Agg') 

def get_hosts(master, current_sub):

    startTime,endTime = services.get_start_end()
    available_hosts = HostEnergy.objects.filter(masterip=master).filter(sub_id=current_sub).all().values()
    df_list=[unix_range(startTime,endTime)]

    for host in available_hosts:
        url = "http://"+host['masterip']+":8080/papillonserver/rest/datacenters/"+host['datacenterid']+"/floors/"+str(host['floorid'])+"/racks/"+str(host['rackid'])+"/hosts/"+str(host['hostid'])+"/power?starttime="+startTime+"&endtime="+endTime
        response = services.get_reponse(url)
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
            df_list.append(df)

    hosts = reduce(lambda x, y: pd.merge(x, y, on = 'day', how='left'), df_list)
    hosts['day'] = pd.to_datetime(hosts['day'],unit='s')
    hosts = hosts.fillna(0)
    hosts = hosts[hosts['day']<=pd.to_datetime(int(time.time()),unit='s')]
    for col in hosts.columns[1:]:
        hosts[col] = hosts[col].cumsum()
    hosts['Total'] = hosts[hosts.columns[1:]].sum(axis=1)
    return hosts[hosts.columns[:-1]], hosts[[hosts.columns[0], hosts.columns[-1]]]


def plot_usage(table, ylabel):
    startTime, endTime = services.get_start_end()
    startTime=int(startTime)-10000
    fig, ax = plt.subplots(figsize=(6,5))
    for column in table.columns[1:]:
        ax.plot(table['day'], table[column], label=column, markerfacecolor='blue')
    plt.xlim([pd.to_datetime(startTime,unit='s'), pd.to_datetime(endTime,unit='s')])  
    plt.legend(loc='upper left')
    plt.axhline(y=0, linestyle='dashed')
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.rc('grid', linestyle="--", color='lightgrey')
    plt.grid(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    x = (pd.to_datetime(endTime,unit='s') - pd.to_datetime(startTime,unit='s')).days/4
    if x<1:
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    else: ax.xaxis.set_major_locator(mdates.DayLocator(interval=int(x)))
    buf = io.BytesIO()
    fig.savefig(buf)
    fig.clf()
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


def plot_carbon_total(table):
    startTime, endTime = services.get_start_end()
    startTime=int(startTime)-10000
    fig, ax = plt.subplots(figsize=(6,5))
    for column in table.columns[1:]:
        ax.plot(table['day'], table[column], label=column, markerfacecolor='blue')
    plt.xlim([pd.to_datetime(startTime,unit='s'), pd.to_datetime(endTime,unit='s')])  
    plt.rc('grid', linestyle="--", color='lightgrey')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    x = (pd.to_datetime(endTime,unit='s') - pd.to_datetime(startTime,unit='s')).days/4
    if x<1:
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    else: ax.xaxis.set_major_locator(mdates.DayLocator(interval=int(x)))
    plt.axhline(y=services.get_budget(), c='r')
    plt.axhline(y=0, linestyle='dashed')
    plt.legend(loc='upper left')
    plt.xlabel("Date")
    plt.ylabel("KgCo2")
    plt.grid(True)
    buf = io.BytesIO()
    fig.savefig(buf)
    fig.clf()
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()

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

def unix_range(startTime,endTime):
    start=int(startTime)
    range1 = int((int(endTime)-start)/86400)
    dates=[]
    for i in range(0,range1):
        dates.append(start)
        start+=86400
    base_df = pd.DataFrame(dates, columns=['day'])
    return base_df
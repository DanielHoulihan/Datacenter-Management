from . import services
from tool.models import Host, Budget, ConfiguredDataCenters
import time
from collections import defaultdict
import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt
import base64
import io
import matplotlib.dates as mdates 
import json
plt.switch_backend('Agg') 

def get_hosts_budget(master, sub_id):
    """ Determines whether a budget should be created or an existing one updated. Once this is 
        complete the graphs are produced using methods and updated in the budegt objects. 

    Args:
        master (String): IP Address of the master
        sub_id (String): Instance of datacenter
    """
    
    startTime,endTime = services.get_start_end()
    available_hosts = get_all_host_values(master,sub_id)
    budget = get_all_budgets(master,sub_id)
    if budget.exists():
        update_budget(budget, available_hosts, endTime)
    else:
        create_budget(startTime, endTime, available_hosts)
        
    budget = get_energy_dict(master, sub_id)
    
    decoded_data = json.loads(budget)
    df = pd.DataFrame(decoded_data)
    df = df.fillna(0)
    df['day'] = pd.to_datetime(df['day'],unit='s')
    for col in df.columns[1:]:
        df[col] = df[col].cumsum()
    hosts_df = df[df.columns[:-1]]
    total_df = df[[df.columns[0], df.columns[-1]]]
    budget = Budget.objects.filter(masterip=master).filter(sub_id=sub_id).all()
    
    total_usage = list(total_df['Total'])[-1] * ConfiguredDataCenters.objects.filter(
        masterip=master).filter(sub_id=sub_id).values().get()['carbon_conversion']
    if ConfiguredDataCenters.objects.filter(masterip=master).filter(
        sub_id=sub_id).values().get()['budget'] == None:
        budget.update(
            carbon_graph1 = plot_usage(carbon_usage(hosts_df),'kgC02'),
            carbon_graph2 = plot_usage(carbon_usage(total_df),'kgC02'),
            energy_graph1 = plot_usage(hosts_df,'kWh'),
            energy_graph2 = plot_usage(total_df,'kWh'),
            cost_graph1 = plot_usage(cost_estimate(hosts_df),'€'),
            cost_graph2 = plot_usage(cost_estimate(total_df),'€'),
            total_usage = total_usage
        )
    else: 
        budget.update(
            carbon_graph1 = plot_usage(carbon_usage(hosts_df),'kgC02'),
            carbon_graph2 = plot_carbon_total(carbon_usage(total_df)),
            energy_graph1 = plot_usage(hosts_df,'kWh'),
            energy_graph2 = plot_usage(total_df,'kWh'),
            cost_graph1 = plot_usage(cost_estimate(hosts_df),'€'),
            cost_graph2 = plot_usage(cost_estimate(total_df),'€'),
            total_usage = total_usage,
            usage_percentage = (total_usage/ConfiguredDataCenters.objects.filter(
                masterip=master).filter(sub_id=sub_id).values().get()['budget'])*100
        )
    

def update_budget(budget, available_hosts, endTime):
    """ Updates the Budget object passed in. The energy_dict is the only field updated. This is
        where the daily usage is stored along with the day identifier

    Args:
        budget (String): Budget object
        available_hosts (Queryset<Host>): A list of hosts from the existing models
                                          which are located in the current datacenter instance  
        endTime (String): UNIX end time specified by user (or live if not specified)
    """
    
    
    budgeted = budget.values().get()['energy_dict']
    decoded_data = json.loads(budgeted)
    startTime = str(int(decoded_data[-1]['day']))
    df_list=[unix_range(startTime,endTime)]
    for host in available_hosts:
        url = services.power_url(host['masterip'],host['datacenterid'],str(host['floorid']),
                                str(host['rackid']),str(host['hostid']),startTime,endTime)
        
        response = services.get_response(url)
        data = response.json()
        start=int(startTime)
        energy = defaultdict(list)
        if data!=None: 
            if isinstance(data['power'],list):
                for power in data['power']:
                    if int(power['timeStamp']) >= start:
                        if int(power['timeStamp']) >= start+86400:
                            start+=86400
                            energy[start].append(float(power['power']))
                            continue
                        energy[start].append(float(power['power']))

            summed = {k: sum(v) for (k, v) in energy.items()}
            df = pd.DataFrame(summed.items(), columns=['day', str(host['hostid'])])
            df[str(host['hostid'])] = df[str(host['hostid'])]/1000
            df_list.append(df)
            

    hosts = reduce(lambda x, y: pd.merge(x, y, on = 'day', how='left'), df_list)
    hosts = hosts.fillna(0)
    hosts = hosts[hosts['day']<=int(time.time())]
    hosts['Total'] = hosts[hosts.columns[1:]].sum(axis=1)
    df_dicts = list(hosts.T.to_dict().values())

    updated_dict = decoded_data[:-1] + df_dicts
    encoded_json = json.dumps(updated_dict)       
    budget.update(energy_dict=encoded_json)


def create_budget(startTime, endTime, available_hosts):
    """ Creates budget object since none exist for the specified datacenter

    Args:
        startTime (String): UNIX date in string format (specified by user)
        endTime (String): UNIX date in string format (specified by user)
        available_hosts (Queryset<Host>): _description_
    """
    
    df_list=[unix_range(startTime,endTime)]
    for host in available_hosts:
        url = services.power_url(host['masterip'],host['datacenterid'],str(host['floorid']),
                                    str(host['rackid']),str(host['hostid']),startTime,endTime)
        response = services.get_response(url)
        data = response.json()
        start=int(startTime)
        energy = defaultdict(list)
        if data!=None: 
            if isinstance(data['power'],list):
                for power in data['power']:
                    if int(power['timeStamp']) >= start:
                        if int(power['timeStamp']) >= start+86400:
                            start+=86400
                            energy[start].append(float(power['power']))
                            continue
                        energy[start].append(float(power['power']))

            summed = {k: sum(v) for (k, v) in energy.items()}
            df = pd.DataFrame(summed.items(), columns=['day', str(host['hostid'])])
            df[str(host['hostid'])] = df[str(host['hostid'])]/1000
            df_list.append(df)

    hosts = reduce(lambda x, y: pd.merge(x, y, on = 'day', how='left'), df_list)
    hosts = hosts.fillna(0)
    hosts = hosts[hosts['day']<=int(time.time())]
    hosts['Total'] = hosts[hosts.columns[1:]].sum(axis=1)

    df_dicts = list(hosts.T.to_dict().values())
    encoded_json = json.dumps(df_dicts)        

    Budget.objects.get_or_create(
        masterip=services.get_master(),
        sub_id=services.get_current_sub_id,
        energy_dict=encoded_json
    )
    
# def save_plot_usage(master, current_sub):
#     """_summary_

#     Args:
#         master (_type_): _description_
#         current_sub (_type_): _description_
#     """
#     budget = Budget.objects.filter(masterip=master).filter(
#         sub_id=current_sub).all().values().get()['energy_dict']
#     decoded_data = json.loads(budget)
#     df = pd.DataFrame(decoded_data)
#     df = df.fillna(0)
#     df['day'] = pd.to_datetime(df['day'],unit='s')
#     for col in df.columns[1:]:
#         df[col] = df[col].cumsum()
#     hosts_df = df[df.columns[:-1]]
#     total_df = df[[df.columns[0], df.columns[-1]]]
    
#     budget.update(
#         carbon_graph1 = plot_usage(carbon_usage(hosts_df),'kgC02'),
#         carbon_graph2 = plot_usage(carbon_usage(total_df),'kgC02'),
#         energy_graph1 = plot_usage(hosts_df,'kWh'),
#         energy_graph2 = plot_usage(total_df,'kWh'),
#         cost_graph1 = plot_usage(cost_estimate(hosts_df),'€'),
#         cost_graph2 = plot_usage(cost_estimate(total_df),'€')   
#     )
    

def plot_usage(table,ylabel):
    """ Plots the specified dataframe onto a line chart using matplotlib. This plot is encoded 
        and saved into a Budget object (in another function). Raw matplotlib graphs cannot be saved
        into a Django model.

    Args:
        table (Pandas DataFrame): DataFrame containing daily energy usage of datacenter
        ylabel (String): Label for y axis of graphic

    Returns:
        base64: encoded graph depicting specified table
    """
    
    startTime, endTime = services.get_start_end()
    startTime=int(startTime)-10000
    fig, ax = plt.subplots(figsize=(5.5,4.5))
    for column in table.columns[1:]:
        ax.plot(table['day'], table[column], label=column, markerfacecolor='blue')
        ax.annotate(xy=(list(table['day'])[-1],list(table[column])[-1]), text=round(list(table[column])[-1],2))
    plt.rc('grid', linestyle="--", color='lightgrey')
    plt.xlim([pd.to_datetime(startTime,unit='s'), pd.to_datetime(endTime,unit='s')])  
    plt.legend(loc='upper left')
    plt.axhline(y=0, linestyle='dashed')
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.grid(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    x = (pd.to_datetime(endTime,unit='s') - pd.to_datetime(startTime,unit='s')).days/4
    if x<=1:
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    else: 
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=int(x)))
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf)
    fig.clf()
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()



def plot_carbon_total(table):
    """ Includes budget line if specified by the user.

    Args:
        table (Pandas DataFrame): DataFrame containing daily energy usage of datacenter
        ylabel (String): Label for y axis of graphic

    Returns:
        base64: encoded graph depicting specified table
    """

    startTime, endTime = services.get_start_end()
    startTime=int(startTime)-10000
    fig, ax = plt.subplots(figsize=(5.5,4.5))
    for column in table.columns[1:]:
        ax.plot(table['day'], table[column], label=column, markerfacecolor='blue')
        ax.annotate(xy=(list(table['day'])[-1],list(table[column])[-1]), text=round(list(table[column])[-1],2))
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
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf)
    fig.clf()
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()

def carbon_usage(table):
    """ Convert energy usage into carbon usage

    Args:
        table (Pandas Dataframe): energy table to convert into carbon usage

    Returns:
        Pandas DataFrame: Converted table
    """
    
    try:
        temp = table.copy()
    except: return
    carbon = services.get_carbon_conversion()
    for col in temp.columns[1:]:
        temp[col] = temp[col]*carbon
    return temp

def cost_estimate(table):
    """ Convert energy usage into operational cost

    Args:
        table (Pandas Dataframe): energy table to convert into operational cost

    Returns:
        Pandas DataFrame: Converted table
    """

    try:
        temp = table.copy()
    except: return
    cost = services.get_energy_cost()
    for col in temp.columns[1:]:
        temp[col] = temp[col]*cost
    return temp

def unix_range(startTime,endTime):
    """ Create dataframe with index as unix date (step = 1 day)

    Args:
        startTime (String): start time of dataframe
        endTime (String): end time of dataframe

    Returns:
        Pandas DataFrame: Empty dataframe with UNIX date range as index
    """

    start = int(startTime)
    range1 = int((int(endTime)-start)/86400)
    dates=[]
    for i in range(0,range1+1):
        dates.append(start)
        start+=86400
    base_df = pd.DataFrame(dates, columns=['day'])
    return base_df


def get_all_budgets(master,sub_id):
    """ Find and return all budget objects in the current datacenter

    Args:
        master (String): _description_
        sub_id (String): _description_

    Returns:
        Exception: If no Budget objects exist in the database
    """
    
    try:
        return Budget.objects.filter(masterip=master).filter(sub_id=sub_id).all()
    except: return Budget.DoesNotExist


def get_all_host_values(master, sub_id):
    """ Returns all hosts values for selected datacenter 

    Args:
        master (String): _description_
        sub_id (String): _description_

    Returns:
        Exception: If no Host objects exist in the database
    """
    
    try:
        return Host.objects.filter(masterip=master).filter(sub_id=sub_id).all().values()
    except: return Host.DoesNotExist
    
    
def get_energy_dict(master, sub_id):
    """ Get the energydict of the specified datacenter. (dictionary of the daily energy usage)

    Args:
        master (String): IP Address of master
        sub_id (String): Datacenter instance selected

    Returns:
        Exception: If no Budget objects exist in the database
    """
    
    try:
        return Budget.objects.filter(masterip=master).filter(
            sub_id=sub_id).all().values().get()['energy_dict']
    except: return Budget.DoesNotExist
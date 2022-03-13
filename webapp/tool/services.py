from tool.models import CurrentDatacenter, MasterIP, ConfiguredDataCenters
import pandas as pd
import time
import matplotlib.pyplot as plt 
import mpld3

def get_current_sub_id():
    return str(CurrentDatacenter.objects.all().values().get()['current'])

def get_current_datacenter():
    return str(CurrentDatacenter.objects.all().values().get()['current'].split('-')[0])

def get_master():
    return MasterIP.objects.all().values().get()["master"]

def get_current_for_html():
    current = "-"
    if CurrentDatacenter.objects.filter(masterip=get_master()).all().count()!=0:
        current = get_current_sub_id()
    return current

def get_configured():
    return ConfiguredDataCenters.objects.filter(masterip=get_master()).all()

def get_pue():
    return ConfiguredDataCenters.objects.filter(masterip=get_master()).filter(sub_id=get_current_sub_id()).all().values().get()['pue']

def get_energy_cost():
    return ConfiguredDataCenters.objects.filter(masterip=get_master()).filter(sub_id=get_current_sub_id()).all().values().get()['energy_cost']

def get_carbon_conversion():
    return ConfiguredDataCenters.objects.filter(masterip=get_master()).filter(sub_id=get_current_sub_id()).all().values().get()['carbon_conversion']

def get_budget():
    return ConfiguredDataCenters.objects.filter(masterip=get_master()).filter(sub_id=get_current_sub_id()).all().values().get()['budget']


def unix_range(startTime,endTime):
    start=int(startTime)
    range1 = int((int(endTime)-start)/86400)
    dates=[]
    for i in range(0,range1):
        dates.append(start)
        start+=86400
    base_df = pd.DataFrame(dates, columns=['day'])
    return base_df


def get_start_end():
    startTime = ConfiguredDataCenters.objects.all().filter(sub_id = get_current_sub_id()).values().get()['startTime']
    startTime = str(int(time.mktime(startTime.timetuple())))
    if ConfiguredDataCenters.objects.all().filter(sub_id = get_current_sub_id()).values().get()['endTime']==None:
        endTime = str(int(time.time()))
    else:
        endTime = ConfiguredDataCenters.objects.all().filter(sub_id = get_current_sub_id()).values().get()['endTime']
        endTime = str(int(time.mktime(endTime.timetuple())))
    return startTime, endTime




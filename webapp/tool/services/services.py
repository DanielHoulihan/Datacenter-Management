from tool.models import CurrentDatacenter, MasterIP, ConfiguredDataCenters, Threshold, Count
import pandas as pd
import time
import requests
from django.shortcuts import render
import requests

def get_current_sub_id():
    try:
        return str(CurrentDatacenter.objects.all().values().get()['current'])
    except: return CurrentDatacenter.DoesNotExist

def get_current_datacenter():
    try:
        return str(CurrentDatacenter.objects.all().values().get()['current'].split('-')[0])
    except: return CurrentDatacenter.DoesNotExist

def get_master():
    try:
        return MasterIP.objects.all().values().get()["master"]
    except: return MasterIP.DoesNotExist

def get_current_for_html():
    try:
        current = str(CurrentDatacenter.objects.all().values().get()['current'])
    except:
        current='-'
    return current

def get_configured():
    try:
        return ConfiguredDataCenters.objects.filter(masterip=get_master()).all().get()
    except: return ConfiguredDataCenters.DoesNotExist

def get_pue():
    try: 
        return ConfiguredDataCenters.objects.filter(masterip=get_master()).filter(sub_id=get_current_sub_id()).all().values().get()['pue']
    except: return ConfiguredDataCenters.DoesNotExist

def get_energy_cost():
    try:
        return ConfiguredDataCenters.objects.filter(masterip=get_master()).filter(sub_id=get_current_sub_id()).all().values().get()['energy_cost']
    except: return ConfiguredDataCenters.DoesNotExist

def get_carbon_conversion():
    try:
        return ConfiguredDataCenters.objects.filter(masterip=get_master()).filter(sub_id=get_current_sub_id()).all().values().get()['carbon_conversion']
    except: return ConfiguredDataCenters.DoesNotExist

def get_budget():
    try:
        return ConfiguredDataCenters.objects.filter(masterip=get_master()).filter(sub_id=get_current_sub_id()).all().values().get()['budget']
    except: return ConfiguredDataCenters.DoesNotExist

def get_start_end():
    try:
        startTime = ConfiguredDataCenters.objects.all().filter(sub_id = get_current_sub_id()).values().get()['startTime']
        startTime = str(int(time.mktime(startTime.timetuple())))
        if ConfiguredDataCenters.objects.all().filter(sub_id = get_current_sub_id()).values().get()['endTime']==None:
            endTime = str(int(time.time()))
        else:
            endTime = ConfiguredDataCenters.objects.all().filter(sub_id = get_current_sub_id()).values().get()['endTime']
            endTime = str(int(time.mktime(endTime.timetuple())))
        return startTime, endTime
    except: return ConfiguredDataCenters.DoesNotExist

def get_reponse(url):
    try:
        return requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    except: return ConnectionError

def check_master():
    if MasterIP.objects.count()==0:
        MasterIP.objects.create(master="localhost")

def prompt_configuration(request,page):
    context = {"page":page,"master": get_master(), "current": get_current_for_html()}
    return render(request, 'pick_datacenter/pick_data_center.html', context) 


def create_or_update_current(master,current):
    if CurrentDatacenter.objects.count()==0:
        CurrentDatacenter.objects.create(masterip = master, current=current)
    else: CurrentDatacenter.objects.update(masterip = master, current=current)

def set_threshold():
    if Threshold.objects.count()==0:
        Threshold.objects.create(low=15,medium=30)

def increment_count():
    if Count.objects.all().count()==0:
        Count.objects.create(configured=0)
    else: 
        Count.objects.update(configured = Count.objects.all().values().get()['configured']+1)
from tool.models import CurrentDatacenter, MasterIP, ConfiguredDataCenters
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
    return requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})

def check_master():
    if MasterIP.objects.count()==0:
        MasterIP.objects.create(master="localhost")

def prompt_configuration(request,page):
    context = {"page":page,"master": get_master(), "current": get_current_for_html()}
    return render(request, 'pick_datacenter/pick_data_center.html', context) 
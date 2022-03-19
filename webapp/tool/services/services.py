from tool.models import CurrentDatacenter, MasterIP, ConfiguredDataCenters, Threshold, Count
import time
import requests
from django.shortcuts import render
import requests

def get_current_sub_id():
    """ Find the sub_id of the current datacenter """

    try:
        return str(CurrentDatacenter.objects.all().values().get()['current'])
    except: return CurrentDatacenter.DoesNotExist

def get_current_datacenter():
    """ Find the id of the current datacenter """

    try:
        return str(CurrentDatacenter.objects.all().values().get()['current'].split('-')[0])
    except: return CurrentDatacenter.DoesNotExist

def get_master():
    """ Find the IP address of the selected master """

    try:
        return MasterIP.objects.all().values().get()["master"]
    except: return MasterIP.DoesNotExist

def get_current_for_html():
    """ Find the sub_id of the current datacenter for html use """

    try:
        current = str(CurrentDatacenter.objects.all().values().get()['current'])
    except:
        current='-'
    return current

def get_configured():
    """ Find all configured datacenters on selected IP """

    try:
        return ConfiguredDataCenters.objects.filter(masterip=get_master()).all().get()
    except: return ConfiguredDataCenters.DoesNotExist

def get_pue():
    """ Find the PUE of the specified datacenter """

    try: 
        return ConfiguredDataCenters.objects.filter(masterip=get_master()).filter(sub_id=get_current_sub_id()).all().values().get()['pue']
    except: return ConfiguredDataCenters.DoesNotExist

def get_energy_cost():
    """ Find the energy cost of the specified datacenter """

    try:
        return ConfiguredDataCenters.objects.filter(masterip=get_master()).filter(sub_id=get_current_sub_id()).all().values().get()['energy_cost']
    except: return ConfiguredDataCenters.DoesNotExist

def get_carbon_conversion():
    """ Find the carbon conversion of the specified datacenter """

    try:
        return ConfiguredDataCenters.objects.filter(masterip=get_master()).filter(sub_id=get_current_sub_id()).all().values().get()['carbon_conversion']
    except: return ConfiguredDataCenters.DoesNotExist

def get_budget():
    """ Find the budget of the specified datacenter """

    try:
        return ConfiguredDataCenters.objects.filter(masterip=get_master()).filter(sub_id=get_current_sub_id()).all().values().get()['budget']
    except: return ConfiguredDataCenters.DoesNotExist

def get_start_end():
    """ Generate UNIX times for start and end of currently selected datacenter """

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
    """ Add headers to URL to get response in json (default is XML) """

    try:
        return requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    except: return ConnectionError

def check_master():
    """ Create default master """

    if MasterIP.objects.count()==0:
        MasterIP.objects.create(master="localhost")

def prompt_configuration(request,page):
    """ redirect to pick_datacenter.html if needed """

    context = {"page":page,"master": get_master(), "current": get_current_for_html()}
    return render(request, 'pick_datacenter/pick_data_center.html', context) 


def create_or_update_current(master,current):
    """ Selecting current """

    if CurrentDatacenter.objects.count()==0:
        CurrentDatacenter.objects.create(masterip = master, current=current)
    else: CurrentDatacenter.objects.update(masterip = master, current=current)

def set_threshold():
    """ Set default threshold """

    if Threshold.objects.count()==0:
        Threshold.objects.create(low=15,medium=30)

def increment_count():
    """ Increment count in certain conditions """

    if Count.objects.all().count()==0:
        Count.objects.create(configured=0)
    else: 
        Count.objects.update(configured = Count.objects.all().values().get()['configured']+1)

def get_lower_threshold():
    """ Find the lower threshold for assets % """

    try:
        return Threshold.objects.all().values().get()['low']
    except: return Threshold.DoesNotExist

def get_upper_threshold():
    """ Find the upper threshold for assets % """

    try:
        return Threshold.objects.all().values().get()['low']
    except: return Threshold.DoesNotExist

def create_url(master, datacenter=None, floor=None, rack=None, host=None, start=None, end=None):
    """ Create URL given arguments (Python overloading) """

    if datacenter is None:
        return "http://"+master+":8080/papillonserver/rest/datacenters/"
    if floor is None:
        return "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/floors/"
    if rack is None:
        return "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/floors/"+floor+"/racks/"
    if host is None:
        return "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/floors/"+floor+"/racks/"+rack+"/hosts/"
    else: 
        return "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/floors/"+floor+"/racks/"+rack+"/hosts/"+host+"/power?starttime="+start+"&endtime="+end
    

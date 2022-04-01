from tool.models import Application, ConfiguredDataCenters
import time
import requests
from django.shortcuts import render
import requests

def get_current_sub_id():
    """ Find the sub_id of the current datacenter """

    try:
        return str(Application.objects.all().values().get()['current'])
    except: return Application.DoesNotExist    

def get_current_datacenter():
    """ Find the id of the current datacenter """

    try:
        return str(Application.objects.all().values().get()['current'].split('-')[0])
    except: return Application.DoesNotExist

def get_master():
    """ Find the IP address of the selected master """

    try:
        return Application.objects.all().values().get()["masterip"]
    except: return Application.DoesNotExist

def get_current_for_html():
    """ Find the sub_id of the current datacenter for html use """

    try:
        current = str(Application.objects.filter(masterip=get_master()).all().values().get()['current'])
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

def get_response(url):
    """ Add headers to URL to get response in json (default is XML) """

    try:
        return requests.get(url,headers={'Content-Type': 'application/json', 'Accept': "application/json"})
    except: return ConnectionError

def check_master():
    """ Create default master """

    if Application.objects.count()==0:
        Application.objects.create(masterip="localhost")

def prompt_configuration(request,page):
    """ redirect to pick_datacenter.html if needed """

    context = {"page":page,"master": get_master(), "current": get_current_for_html()}
    return render(request, 'pick_datacenter/pick_data_center.html', context) 


def create_or_update_current(master,current):
    """ Selecting current """

    if Application.objects.count()==0:
        Application.objects.create(masterip = master, current=current)
    else: Application.objects.update(masterip = master, current=current)



def increment_count():
    """ Increment count in certain conditions """

    if Application.objects.count()==0:
        Application.objects.create(configured=0)
    else: 
        Application.objects.update(configured = Application.objects.all().values().get()['configured']+1)
        

def get_lower_threshold():
    """ Find the lower threshold for assets % """

    try:
        return Application.objects.all().values().get()['threshold_low']
    except: return Application.DoesNotExist

def get_upper_threshold():
    """ Find the upper threshold for assets % """

    try:
        return Application.objects.all().values().get()['threshold_medium']
    except: return Application.DoesNotExist
 
def datacenter_url(master):
    return "http://"+master+":8080/papillonserver/rest/datacenters/"

def power_url(master, datacenter,floor,rack,host,start,end):
    return "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/floors/"+floor+"/racks/"+rack+"/hosts/"+host+"/power?starttime="+start+"&endtime="+end

def cpu_usage_url(master, datacenter,floor,rack,host,start,end):
    return "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/floors/"+floor+"/racks/"+rack+"/hosts/"+host+"/activity?starttime="+start+"&endtime="+end

def all_power_url(master, datacenter, start, end):
    return "http://"+master+":8080/papillonserver/rest/datacenters/"+datacenter+"/allhosts/power?starttime="+start+"&endtime="+end
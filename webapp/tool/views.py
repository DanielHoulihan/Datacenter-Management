#!/usr/bin/env python

from django.shortcuts import render
from tool.models import ConfiguredDataCenters, Floor, Rack, Host, Budget, AvailableDatacenters, Application
from .services import services, asset_services, budget_services, tco_services, model_services, Co2_signal_services
from . import forms
from django.views.decorators.csrf import csrf_protect
from datetime import datetime 

__author__ = "Daniel Houlihan"
__studentnumber__ = "18339866"
__version__ = "1.0.1"
__maintainer__ = "Daniel Houlihan"
__email__ = "daniel.houlihan@ucdconnect.ie"
__status__ = "Production"

def assets(request):
    """ Assets Tab
    Finds the available assets in the chosen datacenter. 
    POST method allows user to change the treshold of the CPU usages.
    """    

    context = {}
    master = services.get_master()
    
    if request.method == 'POST':
        form = forms.ChangeThresholdForm(request.POST)
        if form.is_valid():
            low,medium=form.cleaned_data
            Application.objects.update(threshold_low=low,threshold_medium=medium)
        context["error"] = form

    if Application.objects.filter(masterip=master).values().all().get()['current']==None:
        return services.prompt_configuration(request,"assets")

    sub_id = services.get_current_sub_id()
    context['master'] = master
    context['floors'] = Floor.objects.filter(sub_id=sub_id).filter(masterip=master).all()
    context['floor_count'] = Floor.objects.filter(sub_id=sub_id).filter(masterip=master).all().count()
    context['rack_count'] = Rack.objects.filter(sub_id=sub_id).filter(masterip=master).all().count()
    context["host_count"] = Host.objects.filter(sub_id=services.get_current_sub_id()).filter(
        masterip=master).all().count()
    context['current'] = services.get_current_for_html()
    context["threshold"] = Application.objects.all().get()
    context['racks'] = Rack.objects.filter(sub_id=sub_id).filter(masterip=services.get_master()).all()
    context["hosts"] = Host.objects.filter(sub_id=services.get_current_sub_id()).filter(
        masterip=master).all()
    context['page'] = 'assets'
    
    return render (request, 'assets/assets.html', context )


@csrf_protect
def configure(request):
    """ Home Tab
    From AvailableDatacenters, ConfiguredDatacenters collects the relevent information
    and sends to the HTML templates for the Home tab.
    
    POST methods:
    'to_delete' - remove selected datacenter from database
    'ip' - change the ip address of te master
    'to_configure' - setting up a new configured datacenter
    'current_datacenter' - select a current datacenter from the configured
    'update' - updates the selected datacenter
    """
    
    context = {}
        
    master = services.get_master()
    services.check_master()
    if request.method == 'POST':
        if 'to_delete' in request.POST:
            form = forms.DeleteConfigurationForm(request.POST)
            if form.is_valid():
                to_delete = form.cleaned_data['to_delete']
                ConfiguredDataCenters.objects.filter(sub_id=to_delete).filter(masterip=master).delete()
                Application.objects.filter(current=to_delete).filter(masterip=master).update(current=None)
                Host.objects.filter(sub_id=to_delete).filter(masterip=master).delete()

    if request.method == 'POST':            
        if 'ip' in request.POST:
            form = forms.ChangeIPForm(request.POST)
            if form.is_valid():
                ip = form.cleaned_data
                Application.objects.update(masterip=ip, current=None)
                asset_services.get_available_datacenters()
                

    if request.method == 'POST':
        if 'to_configure' in request.POST:
            form = forms.ConfigureNewDatacenterForm(request.POST)
            if form.is_valid():
                to_configure, start, end, pue, energy_cost, carbon_conversion, budget = form.cleaned_data
                services.increment_count()
                instance = str(to_configure)+"-"+str(Application.objects.all().values().get()['configured'])

                model_services.create_configured(master,
                instance,to_configure,start,end,pue,energy_cost,carbon_conversion,budget)

                services.create_or_update_current(master,instance)
                asset_services.find_available_hosts(master, to_configure, instance)
                asset_services.get_hosts_energy(master, instance)
                tco_services.get_hosts_power(master, instance)
                budget_services.get_hosts_budget(master, instance)

            context['error'] = form

    if request.method == 'POST':
        if 'current_datacenter' in request.POST:
            form = forms.SelectCurrentForm(request.POST)
            if form.is_valid():
                current = form.cleaned_data['current_datacenter']
                services.create_or_update_current(master,current)
            context['error'] = form

    if request.method == 'POST':
        if 'update' in request.POST:
            if services.get_current_datacenter()!=Application.DoesNotExist:
                form = forms.UpdateDatacenterForm(request.POST)
                if form.is_valid():
                    to_update = form.cleaned_data['update']
                    asset_services.find_available_hosts(master, services.get_current_datacenter(), to_update)
                    asset_services.update_hosts_energy(master,to_update)
                    budget_services.get_hosts_budget(master,to_update)
                    tco_services.update_hosts_power(master,to_update)


    sub_id = services.get_current_sub_id()

    try:
        last_update = Host.objects.filter(masterip=master).filter(
            sub_id=sub_id).all().values()[0]['cpu_last_response']
        last_update = datetime.fromtimestamp(int(last_update)).strftime("%Y-%m-%d %H:%M")
    except: last_update='Never'
    
    try:
        carbon_intenisty, fuel_mix = Co2_signal_services.get_carbon_intensity()
        context['labels'] = ['Fossil Fuels', 'Renewables']
        context['data'] = [fuel_mix,100-fuel_mix]
        context['colors'] = ["#fd5e53","#32de84"]   
        context['carbon_intensity'] = carbon_intenisty
    except:
        context['labels'] = ['Fossil Fuels', 'Renewables']
        context['data'] = [100,0]
        context['colors'] = ["#fd5e53","#32de84"]   
        context['carbon_intensity'] = "API limit reached"
        
  
    status = asset_services.get_available_datacenters()
    master = services.get_master()
    context['last_update'] = last_update
    context['datacenters'] = AvailableDatacenters.objects.filter(masterip=master).all()
    context['datacenters_count'] = AvailableDatacenters.objects.filter(masterip=master).all().count()
    context['configured_count'] = ConfiguredDataCenters.objects.filter(masterip=master).all().count()
    context['configured'] = ConfiguredDataCenters.objects.filter(masterip=master).all()
    context['master'] = services.get_master()
    context['current'] = services.get_current_for_html()
    context['page'] = "home"
    
    context['online'] = "false"
    # status = asset_services.get_available_datacenters()
    if status!=ConnectionRefusedError:
        context['online'] = 'true'
    return render (request, 'configure/configure.html', context)

            
@csrf_protect
def tco(request):
    """ TCO Tab
    From Host objects collects the relavent TCO information to show in TCO tab.
    POST method allows for user to specify the capital cost of a host.
    """

    context = {}
    master = services.get_master()

    if Application.objects.filter(masterip=master).values().all().get()['current']==None:
        return services.prompt_configuration(request,"tco")

    sub_id = services.get_current_sub_id()
    if request.method == 'POST':
        form = forms.CalculateTCOForm(request.POST)
        if form.is_valid():
            capital,rack,floor,host = form.cleaned_data
            tco_services.calculate_tco(master, sub_id, floor, rack, host, capital)
        context['error'] = form

    context['tco'] = Host.objects.filter(sub_id=sub_id).filter(masterip=master).all()
    context['tco_count'] = Host.objects.filter(sub_id=sub_id).filter(masterip=master).all().count()
    context['master'] = master
    context['current'] = services.get_current_for_html()
    context['page'] = 'tco'
    return render (request, 'TCO/tco.html', context )


def budget(request):
    """ Budget Tab
    Collects graphs from Budget objects to show in web application budget tab.
    """
    
    context = {}
    master = services.get_master()
    current_sub = services.get_current_sub_id()

    if Application.objects.filter(masterip=master).values().all().get()['current']==None:
        return services.prompt_configuration(request,"budget")
    
    budget = Budget.objects.filter(masterip=master).filter(sub_id=current_sub).all().values().get()
    
    context['page'] = 'budget'
    context['master'] = master
    context['current'] = services.get_current_for_html()    
    context['g1'] = budget['carbon_graph1']
    context['g2'] = budget['carbon_graph2']
    context['g3'] = budget['energy_graph1']
    context['g4'] = budget['energy_graph2']
    context['g5'] = budget['cost_graph1']
    context['g6'] = budget['cost_graph2']
    context['usage_percentage'] = budget['usage_percentage']

    return render(request, 'budget/budget.html', context)




#!/usr/bin/env python

from django.shortcuts import render, redirect
from django.urls import reverse
from tool.models import ConfiguredDataCenters, Datacenter, Floor, Rack, Host, CurrentDatacenter, Count, MasterIP, Threshold, Budget, AvailableDatacenters
from .services import services, asset_services, budget_services, tco_services, model_services
from . import forms
from django.views.decorators.csrf import csrf_protect
import json
from datetime import datetime 
import pandas as pd
import time

__author__ = "Daniel Houlihan"
__studentnumber__ = "18339866"
__version__ = "1.0.1"
__maintainer__ = "Daniel Houlihan"
__email__ = "daniel.houlihan@ucdconnect.ie"
__status__ = "Production"

def assets(request):
    """ Assets Tab
    Finds the available floors in the chosen datacenter (assets) 
    """    

    context = {}
    master = services.get_master()
    
    services.set_threshold()

    if request.method == 'POST':
        form = forms.ChangeThresholdForm(request.POST)
        if form.is_valid():
            low,medium=form.cleaned_data
            Threshold.objects.update(low=low,medium=medium)
        context["error"] = form

    if CurrentDatacenter.objects.filter(masterip=master).all().count()==0:
        return services.prompt_configuration(request,"assets")

    sub_id = services.get_current_sub_id()
    context['master'] = master
    context['floors'] = Floor.objects.filter(sub_id=sub_id).filter(masterip=master).all()
    context['floor_count'] = Floor.objects.filter(sub_id=sub_id).filter(masterip=master).all().count()
    context['rack_count'] = Rack.objects.filter(sub_id=sub_id).filter(masterip=master).all().count()
    context["host_count"] = Host.objects.filter(sub_id=services.get_current_sub_id()).filter(masterip=master).all().count()
    context['current'] = services.get_current_for_html()
    context["threshold"] = Threshold.objects.all().get()
    context['racks'] = Rack.objects.filter(sub_id=sub_id).filter(masterip=services.get_master()).all()
    context["hosts"] = Host.objects.filter(sub_id=services.get_current_sub_id()).filter(masterip=master).all()
    context['page'] = 'assets'
    
    return render (request, 'assets/assets.html', context )


@csrf_protect
def configure(request):
    """ Home Tab
    # 'to_delete' - remove selected datacenter from database
    # 'ip' - change the ip address of te master
    # 'to_configure' - setting up a new configured datacenter
    # 'current_datacenter' - select a current datacenter from the configured
    """
    
    context = {}
    asset_services.get_available_datacenters()
    master = services.get_master()
    services.check_master()
    if request.method == 'POST':
        if 'to_delete' in request.POST:
            form = forms.DeleteConfigurationForm(request.POST)
            if form.is_valid():
                to_delete = form.cleaned_data['to_delete']
                ConfiguredDataCenters.objects.filter(sub_id=to_delete).filter(masterip=master).delete()
                CurrentDatacenter.objects.filter(current=to_delete).filter(masterip=master).delete()
                Host.objects.filter(sub_id=to_delete).filter(masterip=master).delete()

    if request.method == 'POST':            
        if 'ip' in request.POST:
            form = forms.ChangeIPForm(request.POST)
            if form.is_valid():
                ip = form.cleaned_data
                MasterIP.objects.update(master = ip)
                asset_services.get_available_datacenters() 

    if request.method == 'POST':
        if 'to_configure' in request.POST:
            form = forms.ConfigureNewDatacenterForm(request.POST)
            if form.is_valid():
                to_configure, start, end, pue, energy_cost, carbon_conversion, budget = form.cleaned_data
                services.increment_count()
                instance = str(to_configure)+"-"+str(Count.objects.all().values().get()['configured']+1)
                if end and not budget: 
                    model_services.create_configured_end_no_budget(master,
                    instance,to_configure,start,end,pue,energy_cost,carbon_conversion)

                if end and budget: 
                    model_services.create_configured_end_budget(master,
                    instance,to_configure,start,end,pue,energy_cost,carbon_conversion,budget)

                if not end and budget: 
                    model_services.create_configured_no_end_budget(master,
                    instance,to_configure,start,pue,energy_cost,carbon_conversion,budget)

                else:
                    model_services.create_configured_no_end_no_budget(master,
                    instance,to_configure,start,pue,energy_cost,carbon_conversion)
                    
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
            form = forms.UpdateDatacenterForm(request.POST)
            if form.is_valid():
                to_update = form.cleaned_data['update']
                asset_services.find_available_hosts(master, services.get_current_datacenter(), to_update)
                asset_services.update_hosts_energy(master,to_update)
                budget_services.get_hosts_budget(master,to_update)
                tco_services.update_hosts_power(master,to_update)


    sub_id = services.get_current_sub_id()
    try:
        last_update = Host.objects.filter(masterip=master).filter(sub_id=sub_id).all().values()[0]['cpu_last_response']
        last_update = datetime.fromtimestamp(int(last_update)).strftime("%Y-%m-%d %H:%M")
    except: last_update='Never'
    master = services.get_master()
    context['last_update'] = last_update
    context['datacenters'] = AvailableDatacenters.objects.filter(masterip=master).all()
    context['datacenters_count'] = AvailableDatacenters.objects.filter(masterip=master).all().count()
    context['configured_count'] = ConfiguredDataCenters.objects.filter(masterip=master).all().count()
    context['configured'] = ConfiguredDataCenters.objects.filter(masterip=master).all()
    context['master'] = services.get_master()
    context['current'] = services.get_current_for_html()
    context['page'] = "home"
    
    return render (request, 'configure/configure.html', context)

            
@csrf_protect
def tco(request):
    """ TCO Tab
    # Calculates TCO of selected host - sends to template
    """

    context = {}
    master = services.get_master()

    if CurrentDatacenter.objects.filter(masterip=master).all().count()==0:
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
    Generate graphs for carbon usage, energy usage, costs
    """
    context = {}
    master = services.get_master()
    current_sub = services.get_current_sub_id()

    if CurrentDatacenter.objects.filter(masterip=master).all().count()==0:
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




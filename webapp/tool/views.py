#!/usr/bin/env python

from django.shortcuts import render
from tool.models import ConfiguredDataCenters, Datacenter, Floor, Rack, Host, CurrentDatacenter, Count, MasterIP, HostEnergy, Threshold
from .services import services, asset_services, budget_services, tco_services, model_services
from . import forms
from django.views.decorators.csrf import csrf_protect

__author__ = "Daniel Houlihan"
__studentnumber__ = "18339866"
__version__ = "1.0.1"
__maintainer__ = "Daniel Houlihan"
__email__ = "daniel.houlihan@ucdconnect.ie"
__status__ = "Production"

def floors(request):
    """ Assets Tab
    Finds the available floors in the chosen datacenter (assets) 
    """    

    context = {}
    master = services.get_master()

    if CurrentDatacenter.objects.filter(masterip=master).all().count()==0:
        return services.prompt_configuration(request,"assets")

    current = services.get_current_datacenter()
    asset_services.get_floors(services.get_current_datacenter())

    context['floors'] = Floor.objects.filter(datacenterid=current).filter(masterip=master).all()
    context['floor_count'] = Floor.objects.filter(datacenterid=current).filter(masterip=master).all().count()
    context['master'] = master
    context['current'] = services.get_current_for_html()
    context['page'] = 'assets'
    return render (request, 'assets/floors.html', context )


def racks(request, floorid):
    """ Assets/Racks Tab
    Finds the available racks in the chosen datacenter (assets) and sends to template
    """

    context = {}
    current = services.get_current_datacenter()

    asset_services.get_racks(current, floorid)

    context['racks'] = Rack.objects.filter(datacenterid=current).filter(floorid=floorid).filter(masterip=services.get_master()).all()
    context['rack_count'] = Rack.objects.filter(datacenterid=current).filter(floorid=floorid).filter(masterip=services.get_master()).all().count()
    context['master'] = services.get_master()
    context['current'] = services.get_current_for_html()
    context['page'] = "assets"
    return render (request, 'assets/racks.html', context )


def hosts(request, floorid, rackid):
    """ Assets/Racks/Hosts Tab 
    Finds the available hosts in the chosen datacenter (assets) and sends to template
    """

    context = {}
    services.set_threshold()

    if request.method == 'POST':
        form = forms.ChangeThresholdForm(request.POST)
        if form.is_valid():
            low,medium=form.cleaned_data
            Threshold.objects.update(low=low,medium=medium)
        context["error"] = form

    startTime, endTime = services.get_start_end()
    master=services.get_master()
    current = services.get_current_datacenter()
    asset_services.get_hosts(master, current, floorid, rackid, startTime, endTime)

    context["hosts"] = Host.objects.filter(sub_id=services.get_current_sub_id()).filter(floorid=floorid).filter(masterip=master).filter(rackid=rackid).all()
    context["host_count"] = Host.objects.filter(sub_id=services.get_current_sub_id()).filter(floorid=floorid).filter(masterip=master).filter(rackid=rackid).all().count()
    context["threshold"] = Threshold.objects.all().get()
    context["master"] = services.get_master()
    context["current"] = services.get_current_for_html()
    context["page"] = "assets"
    return render (request, 'assets/hosts.html', context )
    

@csrf_protect
def configure(request):
    """ Home Tab
    # 'to_delete' - remove selected datacenter from database
    # 'ip' - change the ip address of te master
    # 'to_configure' - setting up a new configured datacenter
    # 'current_datacenter' - select a current datacenter from the configured
    """

    context = {}
    asset_services.get_datacenters()
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
                HostEnergy.objects.filter(sub_id=to_delete).filter(masterip=master).delete()

    if request.method == 'POST':            
        if 'ip' in request.POST:
            form = forms.ChangeIPForm(request.POST)
            if form.is_valid():
                ip = form.cleaned_data
                MasterIP.objects.update(master = ip)
                asset_services.get_datacenters()

    if request.method == 'POST':
        if 'to_configure' in request.POST:
            form = forms.ConfigureNewDatacenterForm(request.POST)
            if form.is_valid():
                to_configure, start, end, pue, energy_cost, carbon_conversion, budget = form.cleaned_data
                services.increment_count()
                if end and not budget: 
                    model_services.create_configured_end_no_budget(master,
                    str(to_configure)+"-"+str(Count.objects.all().values().get()['configured']+1),
                    to_configure,start,end,pue,energy_cost,carbon_conversion)

                if end and budget: 
                    model_services.create_configured_end_budget(master,
                    str(to_configure)+"-"+str(Count.objects.all().values().get()['configured']+1),
                    to_configure,start,end,pue,energy_cost,carbon_conversion,budget)

                if not end and budget: 
                    model_services.create_configured_no_end_budget(master,
                    str(to_configure)+"-"+str(Count.objects.all().values().get()['configured']+1),
                    to_configure,start,pue,energy_cost,carbon_conversion,budget)

                else:
                    model_services.create_configured_no_end_no_budget(master,
                    str(to_configure)+"-"+str(Count.objects.all().values().get()['configured']+1),
                    to_configure,start,pue,energy_cost,carbon_conversion)
            context['error'] = form

    if request.method == 'POST':
        if 'current_datacenter' in request.POST:
            form = forms.SelectCurrentForm(request.POST)
            if form.is_valid():
                current = form.cleaned_data['current_datacenter']
                services.create_or_update_current(master,current)
            context['error'] = form

    master = services.get_master()
    context['datacenters'] = Datacenter.objects.filter(masterip=master).all()
    context['datacenters_count'] = Datacenter.objects.filter(masterip=master).all().count()
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

    current = services.get_current_datacenter()
    if request.method == 'POST':
        form = forms.CalculateTCOForm(request.POST)
        if form.is_valid():
            capital,rack,floor,host = form.cleaned_data
            startTime,endTime = services.get_start_end()            
            tco_services.get_energy_usage(master, current, floor, rack, host, startTime, endTime, capital)
        context['error'] = form

    current_sub = services.get_current_sub_id()
    tco_services.find_all_available_hosts(master, current)

    context['tco'] = HostEnergy.objects.filter(sub_id=current_sub).filter(masterip=master).all()
    context['tco_count'] = HostEnergy.objects.filter(sub_id=current_sub).filter(masterip=master).all().count()
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
    current = services.get_current_datacenter()

    if CurrentDatacenter.objects.filter(masterip=master).all().count()==0:
        return services.prompt_configuration(request,"budget")

    tco_services.find_all_available_hosts(master, current)
    df, total = budget_services.get_hosts(master,current_sub)

    if request.method == 'POST':            
        if 'ip' in request.POST:
            form = forms.ChangeIPForm(request.POST)
            if form.is_valid():
                ip = form.cleaned_data
                MasterIP.objects.update(master = ip)
                asset_services.get_datacenters()
                
    context['page'] = 'budget'
    context['master'] = master
    context['current'] = services.get_current_for_html()
    if ConfiguredDataCenters.objects.filter(masterip=master).filter(sub_id=current_sub).values().get()['budget'] == None:
        context['g1'] = budget_services.plot_usage(budget_services.carbon_usage(total), ylabel="KgCo2")
    else: context['g1'] = budget_services.plot_carbon_total(budget_services.carbon_usage(total))
    context['g2'] = budget_services.plot_usage(budget_services.carbon_usage(df), ylabel="KgCo2")
    context['g3'] = budget_services.plot_usage(total, ylabel="kWh")
    context['g4'] = budget_services.plot_usage(df, ylabel="kWh")
    context['g5'] = budget_services.plot_usage(budget_services.cost_estimate(total), ylabel="Euro")
    context['g6'] = budget_services.plot_usage(budget_services.cost_estimate(df), ylabel="Euro")

    return render(request, 'budget/budget.html', context)
 


 # production example - https://github.com/gothinkster/django-realworld-example-app
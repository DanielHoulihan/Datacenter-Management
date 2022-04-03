from tool.models import Floor, Host, Rack, ConfiguredDataCenters, AvailableDatacenters

""" 
Filling models for cleaner, more readable code
"""

def create_available_datacenter(master,id,name,description):
    AvailableDatacenters.objects.get_or_create(
        masterip=master,
        datacenterid = id,
        datacentername = name,
        description = description,
    )

def create_floor(master,sub_id,datacenter,floor,name,description):
    Floor.objects.get_or_create(
        masterip = master,
        sub_id = sub_id,
        datacenterid = datacenter,
        floorid = floor,
        floorname = name,
        description = description
    )

def create_rack(master,sub_id,datacenter,floor,rack,name,description):
    Rack.objects.get_or_create(
        masterip = master,
        sub_id = sub_id,
        datacenterid = datacenter,
        floorid = floor,
        rackid = rack,
        rackname = name,
        description = description,
    )

def create_empty_host(master,sub_id,datacenter,floorid,rack,id,name,
        description,type,processors,ip):
    Host.objects.get_or_create(
        masterip = master,
        sub_id = sub_id,
        datacenterid = datacenter,
        floorid = floorid,
        rackid = rack,
        hostid = id,
        hostname = name,
        hostdescription = description,
        hostType = type,
        processors = processors,
        ipaddress = ip
    )


def create_configured(master,sub_id,datacenter,start,end,pue,
        energy_cost,carbon_conversion,budget):
    ConfiguredDataCenters.objects.get_or_create(
        masterip = master,
        sub_id = sub_id,
        datacenterid = datacenter,
        startTime = start,
        endTime = end,
        pue = pue,
        energy_cost = energy_cost,
        carbon_conversion = carbon_conversion,
        budget = budget
    )
    
    
    
# def create_configured_end_no_budget(master,sub_id,datacenter,start,end,
#         pue,energy_cost,carbon_conversion):
#     ConfiguredDataCenters.objects.get_or_create(
#         masterip = master,
#         sub_id = sub_id,
#         datacenterid = datacenter,
#         startTime = start,
#         endTime = end,
#         pue = pue,
#         energy_cost = energy_cost,
#         carbon_conversion = carbon_conversion
#     )



# def create_configured_no_end_budget(master,sub_id,datacenter,start,pue,
#         energy_cost,carbon_conversion,budget):
#     ConfiguredDataCenters.objects.get_or_create(
#         masterip = master,
#         sub_id = sub_id,
#         datacenterid = datacenter,
#         startTime = start,
#         pue = pue,
#         energy_cost = energy_cost,
#         carbon_conversion = carbon_conversion,
#         budget = budget
#     )

# def create_configured_no_end_no_budget(master,sub_id,datacenter,start,
#         pue,energy_cost,carbon_conversion):
#     ConfiguredDataCenters.objects.get_or_create(
#         masterip = master,
#         sub_id = sub_id,
#         datacenterid = datacenter,
#         startTime = start,
#         pue = pue,
#         energy_cost = energy_cost,
#         carbon_conversion = carbon_conversion,
#     )
    

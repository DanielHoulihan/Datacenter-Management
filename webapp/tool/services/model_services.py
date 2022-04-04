from tool.models import Floor, Host, Rack, ConfiguredDataCenters, AvailableDatacenters

""" 
Filling models for cleaner, more readable code
"""

def create_available_datacenter(master,id,name,description):
    """ Filling AvailableDatacenters object in database

    Args:
        master (String): IP Address of master
        id (String): Datacenter ID
        name (String): Datacenter name
        description (String): Datacenter description
    """
    
    AvailableDatacenters.objects.get_or_create(
        masterip=master,
        datacenterid = id,
        datacentername = name,
        description = description,
    )

def create_floor(master,sub_id,datacenter,floor,name,description):
    """ Filling Floor objects in database

    Args:
        master (String): IP Address of master
        sub_id (String): Instance of datacenter
        datacenter (String): Datacenter ID
        floor (Integer): Floor ID
        name (String): Floor name
        description (String): Floor description
    """
    
    Floor.objects.get_or_create(
        masterip = master,
        sub_id = sub_id,
        datacenterid = datacenter,
        floorid = floor,
        floorname = name,
        description = description
    )

def create_rack(master,sub_id,datacenter,floor,rack,name,description):
    """ Filling Floor objects in database

    Args:
        master (String): IP Address of master
        sub_id (String): Instance of datacenter
        datacenter (String): Datacenter ID
        floor (Integer): Floor ID
        rack (Integer): Rack ID
        name (String): Rack name
        description (String): Rack description
    """
    
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
    """ Filling empty Host object in database 

    Args:
        master (String): IP Address of master
        sub_id (String): Instance of datacenter
        datacenter (String): Datacenter ID
        floor (Integer): Floor ID
        rack (Integer): Rack ID
        id (Integer): Host ID
        name (String): Host name
        description (String): Host description
        type (String): Type of host
        processors (String): # of processors in host
        ip (String): IP Address of host
    """
    
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
    """ Filling ConfiguredDatacenters objects in database

    Args:
        master (String): IP Address of master
        sub_id (String): Instance of datacenter
        datacenter (String): Datacenter ID
        start (Datetime): Start time of audit period
        end (Datetime): End time of audit period
        pue (Float): Power Usage Effectiveness of datacenter
        energy_cost (Float): Energy cost ( in euro )
        carbon_conversion (Float): Carbon conversion (kgCo2 / kWh produced)
        budget (Integer): Carbon budget of period (kgCo2)
    """
    
    
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
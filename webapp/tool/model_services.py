from tool.models import Datacenter, Floor, CurrentDatacenter, Host, MasterIP, Rack, ConfiguredDataCenters
import requests
import time
from . import services

def create_datacenter(master,id,name,description):
    Datacenter.objects.get_or_create(
        masterip=master,
        datacenterid = id,
        datacentername = name,
        description = description,
    )

def create_floor(master,datacenter,floor,rack,description):
    Floor.objects.get_or_create(
        masterip = master,
        datacenterid = datacenter,
        floorid = floor,
        floorname = rack,
        description = description
    )

def create_rack(master,datacenter,floor,rack,name,description,pdu):
    Rack.objects.get_or_create(
        masterip = master,
        datacenterid = datacenter,
        floorid = floor,
        rackid = rack,
        rackname = name,
        description = description,
        pdu = pdu
    )

def create_empty_host(master,sub_id,datacenter,floorid,rack,id,name,description,type,processors,ip):
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

def create_host(master,sub_id,datacenter,floorid,rack,id,name,description,type,processors,ip,last,avg_cpu,cpu_count,cpu_total):
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
        ipaddress = ip,
        lastTime = last,
        cpu_usage = avg_cpu,
        responses = cpu_count,
        total_cpu = cpu_total
    )

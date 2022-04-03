from django.test import TestCase
from pkg_resources import AvailableDistributions
from tool.services import model_services
from tool.models import AvailableDatacenters, Floor, Rack, Host, ConfiguredDataCenters
import datetime

class ServicesTestEmpty(TestCase):
    
    def test_create_available_dataceneter(self):
        model_services.create_available_datacenter(
            "test1",
            "test2",
            "test3",
            "test4"
        )
        
        master = AvailableDatacenters.objects.all().values().get()['masterip']
        datacenter = AvailableDatacenters.objects.all().values().get()['datacenterid']
        name = AvailableDatacenters.objects.all().values().get()['datacentername']
        description = AvailableDatacenters.objects.all().values().get()['description']
        
        self.assertEquals(master,"test1")
        self.assertEquals(datacenter,"test2")
        self.assertEquals(name,"test3")
        self.assertEquals(description,"test4")
        
        
    def test_create_floor(self):
        model_services.create_floor(
            "test1",
            "test2",
            "test3",
            4,
            "test5",
            "test6"
        )
        
        master = Floor.objects.all().values().get()['masterip']
        sub_id = Floor.objects.all().values().get()['sub_id']
        datacenter = Floor.objects.all().values().get()['datacenterid']
        floor = Floor.objects.all().values().get()['floorid']
        name = Floor.objects.all().values().get()['floorname']
        description = Floor.objects.all().values().get()['description']

        self.assertEquals(master,"test1")
        self.assertEquals(sub_id,"test2")
        self.assertEquals(datacenter,"test3")
        self.assertEquals(floor,4)
        self.assertEquals(name,"test5")
        self.assertEquals(description,"test6")



    def test_create_rack(self):
        model_services.create_rack(
            "test1",
            "test2",
            "test3",
            4,
            5,
            "test6",
            "test7"
        )
        
        master = Rack.objects.all().values().get()['masterip']
        sub_id = Rack.objects.all().values().get()['sub_id']
        datacenter = Rack.objects.all().values().get()['datacenterid']
        floor = Rack.objects.all().values().get()['floorid']
        rack = Rack.objects.all().values().get()['rackid']
        name = Rack.objects.all().values().get()['rackname']
        description = Rack.objects.all().values().get()['description']

        self.assertEquals(master,"test1")
        self.assertEquals(sub_id,"test2")
        self.assertEquals(datacenter,"test3")
        self.assertEquals(floor,4)
        self.assertEquals(rack,5)
        self.assertEquals(name,"test6")
        self.assertEquals(description,"test7")
        
    def test_create_empty_host(self):
        model_services.create_empty_host(
            "test1",
            "test2",
            "test3",
            4,
            5,
            6,
            "test7",
            "test8",
            "test9",
            10,
            "test11"
        )
        
        master = Host.objects.all().values().get()['masterip']
        sub_id = Host.objects.all().values().get()['sub_id']
        datacenter = Host.objects.all().values().get()['datacenterid']
        floor = Host.objects.all().values().get()['floorid']
        rack = Host.objects.all().values().get()['rackid']
        host = Host.objects.all().values().get()['hostid']
        name = Host.objects.all().values().get()['hostname']
        description = Host.objects.all().values().get()['hostdescription']
        type = Host.objects.all().values().get()['hostType']
        processors = Host.objects.all().values().get()['processors']
        ipaddress = Host.objects.all().values().get()['ipaddress']
        
        self.assertEquals(master,"test1")
        self.assertEquals(sub_id,"test2")
        self.assertEquals(datacenter,"test3")
        self.assertEquals(floor,4)
        self.assertEquals(rack,5)
        self.assertEquals(host,6)
        self.assertEquals(name,"test7")
        self.assertEquals(description,"test8")
        self.assertEquals(type,"test9")
        self.assertEquals(processors,10)
        self.assertEquals(ipaddress,"test11")
        
        
        
    def test_create_configured(self):
        model_services.create_configured(
            "test1",
            "test2",
            "test3",
            datetime.date(2021, 10, 19),
            datetime.date(2021, 10, 20),
            6,
            7,
            8,
            9
        )
        
        master = ConfiguredDataCenters.objects.all().values().get()['masterip']
        sub_id = ConfiguredDataCenters.objects.all().values().get()['sub_id']
        datacenter = ConfiguredDataCenters.objects.all().values().get()['datacenterid']
        start = ConfiguredDataCenters.objects.all().values().get()['startTime']
        end = ConfiguredDataCenters.objects.all().values().get()['endTime']
        pue = ConfiguredDataCenters.objects.all().values().get()['pue']
        energy = ConfiguredDataCenters.objects.all().values().get()['energy_cost']
        carbon = ConfiguredDataCenters.objects.all().values().get()['carbon_conversion']
        budget = ConfiguredDataCenters.objects.all().values().get()['budget']
        
        self.assertEquals(master,"test1")
        self.assertEquals(sub_id,"test2")
        self.assertEquals(datacenter,"test3")
        self.assertEquals(start,datetime.date(2021, 10, 19))
        self.assertEquals(end,datetime.date(2021, 10, 20))
        self.assertEquals(pue,6)
        self.assertEquals(energy,7)
        self.assertEquals(carbon,8)
        self.assertEquals(budget,9)
   
from django.test import TestCase
from tool.services import asset_services
from tool.models import ConfiguredDataCenters, Host

class AssetsTestEmpty(TestCase):
        
    def test_get_available_datacenters(self):
        exception = asset_services.get_available_datacenters()
        self.assertEquals(exception,ConnectionRefusedError)
        
    def test_get_hosts_energy(self):
        exception = asset_services.get_hosts_energy("master", "sub_id")
        self.assertEquals(exception,ConfiguredDataCenters.DoesNotExist)
        
    def test_update_hosts_energy(self):
        exception = asset_services.update_hosts_energy("master", "sub_id")
        self.assertEquals(exception,ConfiguredDataCenters.DoesNotExist)
        
    def test_get_host(self):
        exception = asset_services.get_host("master","sub_id","floorid","rackid",'hostid')
        self.assertEquals(exception, Host.DoesNotExist)

    def test_get_last_cpu_reponse(self):
        host = None
        exception = asset_services.get_last_cpu_response(host)
        self.assertEquals(exception,Host.DoesNotExist)
        
    def test_find_available_hosts(self):
        exception = asset_services.find_available_hosts("master", "datacenter","sub_id")
        self.assertEquals(exception,ConnectionRefusedError)
        
        
        
class AssetsTest(TestCase):
    
    def setUp(self):
        Host.objects.create(
            masterip="master",
            sub_id = "sub_id",
            datacenterid = "datacenter",
            floorid = 1,
            rackid = 2,
            hostid = 3,
            processors=5
        )
        
    def test_get_host(self):
        host = asset_services.get_host("master","sub_id",1,2,3)
        self.assertTrue(host.exists())
        
    def test_get_available_datacenters(self):
        exception = asset_services.get_available_datacenters()
        self.assertEquals(exception,ConnectionRefusedError)
        
    def test_get_hosts_energy(self):
        exception = asset_services.get_hosts_energy("master", "sub_id")
        self.assertEquals(exception,ConfiguredDataCenters.DoesNotExist)
        
    def test_update_hosts_energy(self):
        exception = asset_services.update_hosts_energy("master", "sub_id")
        self.assertEquals(exception,ConfiguredDataCenters.DoesNotExist)
        
    def test_get_last_cpu_reponse(self):
        host = None
        exception = asset_services.get_last_cpu_response(host)
        self.assertEquals(exception,Host.DoesNotExist)
        
    def test_find_available_hosts(self):
        exception = asset_services.find_available_hosts("master", "datacenter","sub_id")
        self.assertEquals(exception,ConnectionRefusedError)
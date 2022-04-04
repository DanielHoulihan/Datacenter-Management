from django.test import TestCase
from tool.services import tco_services, services
from tool.models import Host, ConfiguredDataCenters, Application
import datetime

class TCOServicesTestEmpty(TestCase):


    def test_calculate_tco_empty(self):
        exception = tco_services.calculate_tco("master", "sub_id", 3, 2, 1, 100)
        self.assertEquals(exception,Host.DoesNotExist)
        
    def test_update_host_power_empty(self):
        exception = tco_services.update_host_power("master", "sub_id", "datacenter", 5, 4, 3, 1, 2)
        self.assertEquals(exception,Host.DoesNotExist)
        
    def test_get_hosts_power_empty(self):
        exception = tco_services.get_hosts_power("master", "sub_id")
        self.assertEquals(exception, ConfiguredDataCenters.DoesNotExist)
        
    def test_update_hosts_power_empty(self):
        exception = tco_services.update_hosts_power("master", "sub_id")
        self.assertEquals(exception, ConfiguredDataCenters.DoesNotExist)
        
        
class TCOServicesTest(TestCase):
    
    def setUp(self):
        
        ConfiguredDataCenters.objects.create(
            masterip = "master",
            sub_id = "sub_id",
            energy_cost=0.5,
            startTime = datetime.date(2021, 10, 19),
            endTime = datetime.date(2021, 10, 29),
            pue=1.5,
            carbon_conversion=0.4,
            
        )
        Host.objects.create(
            masterip = "master",
            sub_id = "sub_id",
            floorid = 1,
            rackid = 2,
            hostid = 3,
            ops_cons_3=100,
            processors=2
        )
        Application.objects.create(
            masterip="master",
            current="sub_id"
        )
        
    def test_calculate_tco(self):
        
        tco_services.calculate_tco("master", "sub_id",1,2,3,500)
        
        tco = Host.objects.all().values().get()['TCO']
        capital =  Host.objects.all().values().get()['capital']
        
        self.assertEquals(tco,550.0)
        self.assertEquals(capital,500)
        

    def test_calculate_ops_cons_3(self):
        ops_cons_3 = tco_services.calculate_ops_cons_3(100)
        self.assertEquals(ops_cons_3, 2620800)
        
    def test_calculate_op_cost_3(self):
        ops_cons_3 = tco_services.calculate_ops_cons_3(10)
        pue = services.get_pue()
        energy_cost = services.get_energy_cost()
        
        op_cost_3 = tco_services.calculate_op_cost_3(ops_cons_3, pue, energy_cost)
        
        self.assertEquals(op_cost_3, 196560)
        
    def test_calculate_carbon_footprint_3(self):
        ops_cons_3 = tco_services.calculate_ops_cons_3(10)
        carbon_conversion = services.get_carbon_conversion()
        
        cf_3 = tco_services.calculate_carbon_footprint_3(ops_cons_3, carbon_conversion)
        
        self.assertEquals(cf_3, 104832)
        
import datetime
from django.test import TestCase
from tool.services import services
from django.core.exceptions import ObjectDoesNotExist
from tool.models import ConfiguredDataCenters, Application


class ServicesTestEmpty(TestCase):

    # Test current datacenter for html woth no datacenter selected
    def test_get_current_for_html(self):
        test = services.get_current_for_html()
        self.assertEqual(test,"-")

    def test_get_current_sub_id(self):
        test = services.get_current_sub_id()
        self.assertEqual(Application.DoesNotExist,test)

    def test_get_current_datacenter(self):
        test = services.get_current_datacenter()
        self.assertEqual(Application.DoesNotExist,test)

    def test_get_master(self):
        test = services.get_master()
        self.assertEqual(Application.DoesNotExist,test)

    def test_get_configured(self):
        test = services.get_configured()
        self.assertEqual(ConfiguredDataCenters.DoesNotExist,test)

    def test_get_pue(self):
        test = services.get_pue()
        self.assertEqual(ConfiguredDataCenters.DoesNotExist,test)

    def test_get_energy_cost(self):
        test = services.get_energy_cost()
        self.assertEqual(ConfiguredDataCenters.DoesNotExist,test)

    def test_get_carbon_conversion(self):
        test = services.get_carbon_conversion()
        self.assertEqual(ConfiguredDataCenters.DoesNotExist,test)

    def test_get_budget(self):
        test = services.get_budget()
        self.assertEqual(ConfiguredDataCenters.DoesNotExist,test)

    def test_get_start_end(self):
        test = services.get_start_end()
        self.assertEqual(ConfiguredDataCenters.DoesNotExist, test)

    def test_get_response(self):
        url="http://arbitrary_address"
        test = services.get_response(url)
        self.assertEqual(ConnectionError, test)

    def test_get_lower_threshold(self):
        lower = services.get_lower_threshold()
        self.assertEqual(lower, Application.DoesNotExist)

    def test_get_upper_threshold(self):
        upper = services.get_upper_threshold()
        self.assertEqual(upper, Application.DoesNotExist)
        
    def test_get_empty_threshold(self):
        self.assertEqual(services.get_lower_threshold(),Application.DoesNotExist)
        self.assertEqual(services.get_upper_threshold(),Application.DoesNotExist)

    def test_increment_count(self):
        services.increment_count()
        services.increment_count()
        self.assertEqual(Application.objects.all().values().get()['configured'], 1)
    
    def test_create_or_update_current(self):
        master = "master IP"
        current = "current datacenter"
        services.create_or_update_current(master, current)
        
    def test_check_master(self):
        services.check_master()
        self.assertEqual(Application.objects.all().values().get()['masterip'], "localhost")
        
    def test_datacenter_url(self):
        url = services.datacenter_url("localhost")
        self.assertEqual(url, "http://localhost:8080/papillonserver/rest/datacenters/")

    def test_power_url(self):
        url = services.power_url("localhost", "datacenter", "floor", "rack", "host", "12", "13")
        self.assertEqual(url, "http://localhost:8080/papillonserver/rest/datacenters/datacenter/floors/floor/racks/rack/hosts/host/power?starttime=12&endtime=13")
    
    def test_cpu_usage_url(self):
        url = services.cpu_usage_url("localhost", "datacenter", "floor", "rack", "host", "12", "13")
        self.assertEqual(url, "http://localhost:8080/papillonserver/rest/datacenters/datacenter/floors/floor/racks/rack/hosts/host/activity?starttime=12&endtime=13")
        
    def test_all_power_url(self):
        url = services.all_power_url("localhost", "datacenter", "start", "end")
        self.assertEqual(url, "http://localhost:8080/papillonserver/rest/datacenters/datacenter/allhosts/power?starttime=start&endtime=end")
        
        


class ServicesTest(TestCase):

    def setUp(self):
        ConfiguredDataCenters.objects.create(
            masterip="master",
            sub_id='sub_id-1',
            datacenterid='sub_id',
            startTime=datetime.date(2021, 10, 19),
            endTime=datetime.date(2021, 10, 21),
            pue=1.5,
            energy_cost=0.3,
            carbon_conversion=0.8,
            budget=20
            )
        Application.objects.create(
            masterip="master",
            current="sub_id-1",
            configured=6,
            threshold_low=50,
            threshold_medium=70
        )

    def test_get_current_for_html(self):
        test = services.get_current_for_html()
        self.assertEqual(test,"sub_id-1")

    def test_get_current_sub_id(self):
        test = services.get_current_sub_id()
        self.assertEqual("sub_id-1",test)

    def test_get_current_datacenter(self):
        test = services.get_current_datacenter()
        self.assertEqual("sub_id",test)

    def test_get_master(self):
        test = services.get_master()
        self.assertEqual("master",test)

    def test_get_configured(self):
        test = services.get_configured()
        self.assertEqual(ConfiguredDataCenters.objects.all().get(),test)

    def test_get_pue(self):
        test = services.get_pue()
        self.assertEqual(1.5,test)

    def test_get_energy_cost(self):
        test = services.get_energy_cost()
        self.assertEqual(0.3,test)

    def test_get_carbon_conversion(self):
        test = services.get_carbon_conversion()
        self.assertEqual(0.8,test)

    def test_get_budget(self):
        test = services.get_budget()
        self.assertEqual(20,test)

    def test_get_start_end(self):
        start,end = services.get_start_end()
        self.assertEqual(start, '1634601600')
        self.assertEqual(end, '1634774400')

    def test_check_master(self):
        services.check_master()
        self.assertEqual(Application.objects.all().values().get()['masterip'], "master")
        
    def test_create_or_update_current(self):
        master = "master_test"
        current = "sub_id_test"
        services.create_or_update_current(master, current)
        self.assertEquals(Application.objects.all().values().get()['masterip'],"master_test")
        self.assertEquals(Application.objects.all().values().get()['current'],"sub_id_test")
        
    def test_increment_count(self):
        services.increment_count()
        self.assertEquals(Application.objects.all().values().get()['configured'],7)
        
    def test_get_lower_threshold(self):
        self.assertEqual(Application.objects.all().values().get()['threshold_low'],50)

    def test_get_upper_threshold(self):
        self.assertEqual(Application.objects.all().values().get()['threshold_medium'],70)

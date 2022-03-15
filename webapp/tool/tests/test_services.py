import datetime
from django.test import TestCase
from tool.services import services
from django.core.exceptions import ObjectDoesNotExist
from tool.models import CurrentDatacenter, MasterIP, ConfiguredDataCenters


class ServicesTestEmpty(TestCase):

    # Test current datacenter for html woth no datacenter selected
    def test_get_current_for_html(self):
        test = services.get_current_for_html()
        self.assertEqual(test,"-")

    def test_get_current_sub_id(self):
        test = services.get_current_sub_id()
        self.assertEqual(CurrentDatacenter.DoesNotExist,test)

    def test_get_current_datacenter(self):
        test = services.get_current_datacenter()
        self.assertEqual(CurrentDatacenter.DoesNotExist,test)

    def test_get_master(self):
        test = services.get_master()
        self.assertEqual(MasterIP.DoesNotExist,test)

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

    def test_get_reponse(self):
        url="http://arbitrary_address"
        test = services.get_reponse(url)
        self.assertEqual(ConnectionError, test)




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
        MasterIP.objects.create(
            master="master"
        )
        CurrentDatacenter.objects.create(
            masterip="master",
            current="sub_id-1"
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

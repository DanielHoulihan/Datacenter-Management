import datetime
from django.test import TestCase
from tool import asset_services
from django.core.exceptions import ObjectDoesNotExist
from tool.models import CurrentDatacenter, MasterIP, ConfiguredDataCenters

class AssetsTest(TestCase):

    def setUp(self):
        asset_services.get_datacenters()
        

    # def test_get_current_for_html(self):
    #     asset_services.get_datacenters()
    #     self.assertEqual(test,"sub_id-1")

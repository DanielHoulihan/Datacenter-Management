import datetime
from django.test import TestCase
from tool import services
from django.core.exceptions import ObjectDoesNotExist
from tool.models import CurrentDatacenter, MasterIP, ConfiguredDataCenters


class BudgetServicesTestEmpty(TestCase):

    def test_unix_date(self):
        test = services.unix_range(1647302400,1647565200)
        expected_dates = [1647302400, 1647388800, 1647475200]
        self.assertEqual(expected_dates,list(test['day']))



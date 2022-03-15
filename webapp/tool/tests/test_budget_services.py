from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from tool.models import CurrentDatacenter, MasterIP, ConfiguredDataCenters
from tool.services import budget_services


class BudgetServicesTestEmpty(TestCase):

    def test_unix_date(self):
        test = budget_services.unix_range(1647302400,1647565200)
        expected_dates = [1647302400, 1647388800, 1647475200]
        self.assertEqual(expected_dates,list(test['day']))



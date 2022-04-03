from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from tool.models import ConfiguredDataCenters, Application, Budget
from tool.services import budget_services, services
import pandas as pd
import datetime

class BudgetServicesTestEmpty(TestCase):

    def test_carbon_usage_empty(self):
        df = pd.DataFrame()
        new_table = budget_services.carbon_usage(df)
        self.assertEqual(True, new_table.equals(pd.DataFrame()))
        
    def test_carbon_usage_None(self):
        new_table = budget_services.carbon_usage(None)
        self.assertEqual(new_table,None)
        
    def test_cost_estimate_empty(self):
        df = pd.DataFrame()
        new_table = budget_services.cost_estimate(df)
        self.assertEqual(True, new_table.equals(pd.DataFrame()))
        
    def test_cost_estimate_None(self):
        new_table = budget_services.cost_estimate(None)
        self.assertEqual(new_table,None)
        
    def test_get_all_budgets_none(self):
        exception = budget_services.get_all_budgets("master", "current_sub")
        self.assertFalse(exception.exists())
        
    def test_get_energy_dict_none(self):
        exception = budget_services.get_energy_dict("master", "current_sub")
        self.assertEquals(exception, Budget.DoesNotExist)
        
        
class BudgetServicesTest(TestCase):
    
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
            current="sub_id-1"
        )
        
        Budget.objects.create(
            masterip="master",
            sub_id = "sub_id-1",
            energy_dict = "dictionary"
        )
        
    def test_unix_date(self):
        start, end = services.get_start_end()
        test = budget_services.unix_range(start,end)
        expected_dates = [1634601600, 1634688000, 1634774400]
        self.assertEqual(expected_dates,list(test['day']))

    def test_carbon_usage(self):
        df = pd.DataFrame({'day': [1634601600,1634688000], 'Total': [1000,2000]})
        new_table = budget_services.carbon_usage(df)
        self.assertEqual(True, new_table.equals(pd.DataFrame({'day': [1634601600,1634688000], 'Total': [800.0,1600.0]})))

    def test_cost_estimate(self):
        df = pd.DataFrame({'day': [1634601600,1634688000], 'Total': [1000,2000]})
        new_table = budget_services.cost_estimate(df)
        self.assertEqual(True, new_table.equals(pd.DataFrame({'day': [1634601600,1634688000], 'Total': [300.0,600.0]})))
               
    def test_get_all_host_values(self):
        exception = budget_services.get_all_host_values("master", "current_sub")
        self.assertFalse(exception.exists())
        
    def test_get_all_budgets(self):
        exception = budget_services.get_all_budgets("master", "sub_id-1")
        self.assertTrue(exception.exists())
        
    def test_get_energy_dict(self):
        dict = budget_services.get_energy_dict("master", "sub_id-1")
        self.assertEquals(dict, "dictionary")
from django.test import TestCase
from tool import forms
from datetime import datetime
class FormTest(TestCase):

    # selecting datacenter
    def test_select_current(self):
        form_data = {'current_datacenter': '287'}
        form = forms.SelectCurrentForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        
    # updating datacenter
    def test_update_datacenter(self):
        form_data = {'update': '288'}
        form = forms.UpdateDatacenterForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        
    # deleting datacenter
    def test_delete(self):
        form_data = {'to_delete': '287'}
        form = forms.DeleteConfigurationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_delete_not_string(self):
        form_data = {'to_delete': None}
        form = forms.DeleteConfigurationForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    # changing threshold
    def test_change_threshold_low_above_med(self):
        form_data = {'low': '10', 'medium': '5'}
        form = forms.ChangeThresholdForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_change_threshold_med_above_low(self):
        form_data = {'low': '5', 'medium': '10'}
        form = forms.ChangeThresholdForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_change_threshold_low_below_0(self):
        form_data = {'low': '-5', 'medium': '10'}
        form = forms.ChangeThresholdForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_change_threshold_med_below_0(self):
        form_data = {'low': '5', 'medium': '-10'}
        form = forms.ChangeThresholdForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_change_threshold_low_above_100(self):
        form_data = {'low': '105', 'medium': '106'}
        form = forms.ChangeThresholdForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_change_threshold_med_above_100(self):
        form_data = {'low': '10', 'medium': '106'}
        form = forms.ChangeThresholdForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_change_threshold_med_not_string(self):
        form_data = {'low': '10', 'medium': 106}
        form = forms.ChangeThresholdForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_change_threshold_low_not_string(self):
        form_data = {'low': 10, 'medium': '106'}
        form = forms.ChangeThresholdForm(data=form_data)
        self.assertFalse(form.is_valid())
        
        
    # IP change
    def test_change_ip(self):
        form_data = {'ip': "localhost"}
        form = forms.ChangeIPForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        
    # Configurating new datacenter    
    def test_configure_valid(self):
        form_data = {'to_configure':'287', 'start': datetime(2022,1,1), 'pue': 1, 'energy_cost':2, 'carbon_conversion':5, 'budget':10}
        form = forms.ConfigureNewDatacenterForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_configure_neg_pue(self):
        form_data = {'to_configure':'287', 'start': datetime(2022,1,1), 'pue': -1, 'energy_cost':2, 'carbon_conversion':5, 'budget':10}
        form = forms.ConfigureNewDatacenterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_configure_high_pue(self):
        form_data = {'to_configure':'287', 'start': datetime(2022,1,1), 'pue': 100000000000, 'energy_cost':2, 'carbon_conversion':5, 'budget':10}
        form = forms.ConfigureNewDatacenterForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_configure_neg_energy(self):
        form_data = {'to_configure':'287', 'start': datetime(2022,1,1), 'pue': 1, 'energy_cost':-2, 'carbon_conversion':5, 'budget':10}
        form = forms.ConfigureNewDatacenterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_configure_high_energy(self):
        form_data = {'to_configure':'287', 'start': datetime(2022,1,1), 'pue': 2, 'energy_cost':100000000000, 'carbon_conversion':5, 'budget':10}
        form = forms.ConfigureNewDatacenterForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_configure_neg_carbon(self):
        form_data = {'to_configure':'287', 'start': datetime(2022,1,1), 'pue': 1, 'energy_cost':2, 'carbon_conversion':-5, 'budget':10}
        form = forms.ConfigureNewDatacenterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_configure_high_carbon(self):
        form_data = {'to_configure':'287', 'start': datetime(2022,1,1), 'pue': 2, 'energy_cost':1, 'carbon_conversion':100000000000, 'budget':10}
        form = forms.ConfigureNewDatacenterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_configure_neg_budget(self):
        form_data = {'to_configure':'287', 'start': datetime(2022,1,1), 'pue': 1, 'energy_cost':2, 'carbon_conversion':5, 'budget':-10}
        form = forms.ConfigureNewDatacenterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_configure_high_budget(self):
        form_data = {'to_configure':'287', 'start': datetime(2022,1,1), 'pue': 2, 'energy_cost':1, 'carbon_conversion':1, 'budget':100000000000}
        form = forms.ConfigureNewDatacenterForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_configure_start_before_end(self):
        form_data = {'to_configure':'287', 'start': datetime(2022,1,1), 'end': datetime(2021,1,1), 'pue': 2, 'energy_cost':1, 'carbon_conversion':1, 'budget':100000000000}
        form = forms.ConfigureNewDatacenterForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    # TCO testing
    
    def test_tco_valid(self):
        form_data = {'capital':5000, 'rack': '5', 'floor':'5', 'host': '2'}
        form = forms.CalculateTCOForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_tco_neg_capital(self):
        form_data = {'capital':-5000, 'rack': '5', 'floor':'5', 'host': '2'}
        form = forms.CalculateTCOForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_tco_high_capital(self):
        form_data = {'capital':100000000000, 'rack': '5', 'floor':'5', 'host': '2'}
        form = forms.CalculateTCOForm(data=form_data)
        self.assertFalse(form.is_valid())
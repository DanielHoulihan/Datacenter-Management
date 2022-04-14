from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from tool.models import Application
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import Select

class TCOTest(LiveServerTestCase):
        
    def test_tco_submit(self):
        selenium = webdriver.Chrome(ChromeDriverManager().install())

        selenium.get('http://localhost:8000/tool/tco/')
        player_name = selenium.find_element_by_name('capital')
        submit = selenium.find_element_by_class_name('tco_calculate_button')
        player_name.send_keys('6969')

        submit.send_keys(Keys.RETURN)

        assert '6969' in selenium.page_source

    def test_tco_submit_neg(self):
        selenium = webdriver.Chrome(ChromeDriverManager().install())

        selenium.get('http://localhost:8000/tool/tco/')
        player_name = selenium.find_element_by_name('capital')
        submit = selenium.find_element_by_class_name('tco_calculate_button')
        player_name.send_keys('-696969')

        submit.send_keys(Keys.RETURN)

        assert not '-696969' in selenium.page_source

    def test_tco_submit_high(self):
        selenium = webdriver.Chrome(ChromeDriverManager().install())

        selenium.get('http://localhost:8000/tool/tco/')
        player_name = selenium.find_element_by_name('capital')
        submit = selenium.find_element_by_class_name('tco_calculate_button')
        player_name.send_keys('100000000000000')

        submit.send_keys(Keys.RETURN)

        assert not '100000000000000' in selenium.page_source

    def test_tco_submit_string(self):
        selenium = webdriver.Chrome(ChromeDriverManager().install())

        selenium.get('http://localhost:8000/tool/tco/')
        player_name = selenium.find_element_by_name('capital')
        submit = selenium.find_element_by_class_name('tco_calculate_button')
        player_name.send_keys('hello')

        submit.send_keys(Keys.RETURN)

        assert not 'hello' in selenium.page_source
        
        
class AssetTest(LiveServerTestCase):
        
    def test_asset_threshold_valid(self):
        selenium = webdriver.Chrome(ChromeDriverManager().install())

        selenium.get('http://localhost:8000/tool/assets/')
        player_name = selenium.find_element_by_name('low')
        layer_name = selenium.find_element_by_name('medium')
        submit = selenium.find_element_by_class_name('submit')
        player_name.send_keys('26')
        layer_name.send_keys('76')

        submit.send_keys(Keys.RETURN)
        
        assert '26' and '76' in selenium.page_source

    def test_asset_threshold_invalid(self):
        selenium = webdriver.Chrome(ChromeDriverManager().install())

        selenium.get('http://localhost:8000/tool/assets/')
        player_name = selenium.find_element_by_name('low')
        layer_name = selenium.find_element_by_name('medium')
        submit = selenium.find_element_by_class_name('submit')
        player_name.send_keys('96')
        layer_name.send_keys('69')

        submit.send_keys(Keys.RETURN)
        
        assert  'Upper Threshold must be greater than lower' in selenium.page_source
        
    def test_asset_threshold_low_neg(self):
        selenium = webdriver.Chrome(ChromeDriverManager().install())

        selenium.get('http://localhost:8000/tool/assets/')
        player_name = selenium.find_element_by_name('low')
        layer_name = selenium.find_element_by_name('medium')
        submit = selenium.find_element_by_class_name('submit')
        player_name.send_keys('-69')
        layer_name.send_keys('96')

        submit.send_keys(Keys.RETURN)
        
        assert 'Lower Threshold must be between 0 and 100' in selenium.page_source

    def test_asset_threshold_med_neg(self):
        selenium = webdriver.Chrome(ChromeDriverManager().install())

        selenium.get('http://localhost:8000/tool/assets/')
        player_name = selenium.find_element_by_name('low')
        layer_name = selenium.find_element_by_name('medium')
        submit = selenium.find_element_by_class_name('submit')
        player_name.send_keys('69')
        layer_name.send_keys('-96')

        submit.send_keys(Keys.RETURN)
        
        assert not 'Upper Threshold must be between 0 and 100' in selenium.page_source


    def test_asset_threshold_low_high(self):
        selenium = webdriver.Chrome(ChromeDriverManager().install())

        selenium.get('http://localhost:8000/tool/assets/')
        player_name = selenium.find_element_by_name('low')
        layer_name = selenium.find_element_by_name('medium')
        submit = selenium.find_element_by_class_name('submit')
        player_name.send_keys('101')
        layer_name.send_keys('105')

        submit.send_keys(Keys.RETURN)
        
        assert 'Lower Threshold must be between 0 and 100' in selenium.page_source

    def test_asset_threshold_med_high(self):
        selenium = webdriver.Chrome(ChromeDriverManager().install())

        selenium.get('http://localhost:8000/tool/assets/')
        player_name = selenium.find_element_by_name('low')
        layer_name = selenium.find_element_by_name('medium')
        submit = selenium.find_element_by_class_name('submit')
        player_name.send_keys('69')
        layer_name.send_keys('101')

        submit.send_keys(Keys.RETURN)
        
        assert 'Upper Threshold must be between 0 and 100' in selenium.page_source



# class ChangeMaster(LiveServerTestCase):
        
#     def test_asset_threshold_valid(self):
#         selenium = webdriver.Chrome(ChromeDriverManager().install())

#         selenium.get('http://localhost:8000/tool/')
#         player_name = selenium.find_element_by_name('ip')
#         submit = selenium.find_element_by_class_name('save')
#         player_name.send_keys('localhost')
#         submit.send_keys(Keys.RETURN)
        
#         assert 'localhost' in selenium.page_source
#         player_name = selenium.find_element_by_name('ip')
#         submit = selenium.find_element_by_class_name('save')
#         player_name.send_keys('192.168.56.102')
#         submit.send_keys(Keys.RETURN)
        
        
class UpdateDatacenter(LiveServerTestCase):
        
    def test_configure_datacenter(self):
        selenium = webdriver.Chrome(ChromeDriverManager().install())
        selenium.get('http://localhost:8000/tool/')
        submit = selenium.find_element_by_class_name('update-button')
        submit.send_keys(Keys.RETURN)

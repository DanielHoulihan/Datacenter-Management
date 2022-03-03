from django.test import TestCase
from tool import services

class ServicesTest(TestCase):

    def test_something_that_will_pass(self):
        test = services.get_current_for_html()
        self.assertEqual(test,"-")

from voting.models import Voting, Question, QuestionOption
from mixnet.models import Auth
from django.conf import settings
from pathlib import Path
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command


# Create your tests here.
from base.tests import BaseTestCase
import json
from django.utils import timezone
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from voting.models import Candidatura
from base.tests import BaseTestCase

class VisualizerTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        call_command("loaddata", "test_data_visualizer.json")

    def tearDown(self):
        super().tearDown()
        call_command("flush", interactive=False)

    # def test_access_bot_200(self):
    #     v = self.create_voting()
    #     data = {} 
    #     self.login()
    #     response = self.client.get('/visualizer/botResults/{}/'.format(v.pk), data, format= 'json')
    #     print("Hola")
    #     print(response.resolver_match.func.__name__)
    #     self.assertEquals(response.status_code, 200)


    def test_access_bot_no_admin_404(self):
        data = {} 
        self.login(user='franpe', password="complexpassword")
        response = self.client.get('/visualizer/botResults/{}/'.format(1), data, format= 'json')
        self.assertEquals(response.status_code, 404)

    def test_access_bot_400(self):
        data = {} 
        self.login()
        response = self.client.get('/visualizer/{}/'.format(-1), data, format= 'json')
        self.assertEquals(response.status_code, 404)
        
    def test_access_visualizer_200(self):
        data = {} 
        self.login()
        response = self.client.get('/visualizer/{}/'.format(1), data, format= 'json')
        self.assertEquals(response.status_code, 200)

    def test_access_visualizer_400(self):
        data = {} 
        self.login()
        response = self.client.get('/visualizer/{}/'.format(-1), data, format= 'json')
        self.assertEquals(response.status_code, 404)

    def test_access_aboutus_200(self):
        data = {} 
        self.login()
        response = self.client.get('/visualizer/aboutUs/', data, format= 'json')
        self.assertEquals(response.status_code, 200)

    def test_access_aboutus_404(self):
        data = {} 
        self.login()
        response = self.client.get('/visualizer/aboutUs/{}'.format(-1), data, format= 'json')
        self.assertEquals(response.status_code, 404)

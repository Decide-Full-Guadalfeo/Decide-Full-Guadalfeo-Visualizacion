from voting.models import Voting, Question, QuestionOption
from mixnet.models import Auth
from django.conf import settings
from pathlib import Path
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

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

    def tearDown(self):
        super().tearDown()

    def create_voting(self,opt_number=5):
        v = Voting(name="Test primaria 1 pregunta")
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        script_location = Path(__file__).absolute().parent
        file_location = script_location / 'API_vGeneral.json'
        with file_location.open() as json_file:
            json_file = json.load(json_file)

            # Sorting the results
            lista = []
            if (json_file['tipo'] == 'VG'):
                lista = [0,1,2,3,4,5,6]
            else:
                lista = [0,1,2,3,4,5]
            for i in lista:
                json_file['preguntas'][i]['opts'] = sorted(json_file['preguntas'][i]['opts'], key=lambda x : x['voto_M']+x['voto_F'], reverse=True)

        v.postproc=json_file

        return v

    # def test_access_bot_200(self):
    #     v = self.create_voting()
    #     data = {} 
    #     self.login()
    #     response = self.client.get('/visualizer/botResults/{}/'.format(v.pk), data, format= 'json')
    #     print("Hola")
    #     print(response.resolver_match.func.__name__)
    #     self.assertEquals(response.status_code, 200)


    def test_access_bot_no_admin_404(self):
        v = self.create_voting()
        data = {} 
        self.login(user='noadmin')
        response = self.client.get('/visualizer/botResults/{}/'.format(v.pk), data, format= 'json')
        self.assertEquals(response.status_code, 404)

    def test_access_bot_400(self):
        data = {} 
        self.login()
        response = self.client.get('/visualizer/{}/'.format(-1), data, format= 'json')
        self.assertEquals(response.status_code, 404)
        
    def test_access_visualizer_200(self):
        v = self.create_voting()
        data = {} 
        self.login()
        response = self.client.get('/visualizer/{}/'.format(v.pk), data, format= 'json')
        self.assertEquals(response.status_code, 200)

    def test_access_visualizer_400(self):
        data = {} 
        self.login()
        response = self.client.get('/visualizer/{}/'.format(-1), data, format= 'json')
        self.assertEquals(response.status_code, 404)

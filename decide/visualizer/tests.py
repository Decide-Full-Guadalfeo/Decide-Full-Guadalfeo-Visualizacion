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

    
        
class StatisticsPostprocTestCase(BaseTestCase):
    
    def setUp(self):
        super().setUp()
        call_command("loaddata", "test_data_visualizer.json")
        self.login()
        
    def tearDown(self):
        super().tearDown()
    
    def test_votacion_general(self):

    # Ejecutamos el tally y postproc de una votación general
        Voting.objects.get(id=6).tally_votes(self.token)

    # Estadísticas
        v = Voting.objects.get(id=6)
        assert v.postproc["estadisticas"] != None
        assert len(v.postproc["estadisticas"]["abstencion"]) == 6
        assert len(v.postproc["estadisticas"]["media_edad"]) == 6
        assert len(v.postproc["estadisticas"]["abstencion_f"]) == 6
        assert len(v.postproc["estadisticas"]["abstencion_m"]) == 6

    # Delegado de centro
        assert v.postproc["preguntas"][0]["titulo"] == "Votaci\u00f3n general 2: Elige al delegado al centro"
        assert len(v.postproc["preguntas"][0]["opts"]) == 1
        assert len(v.postproc["preguntas"][0]["opts"][0]["estadisticas"]) == 8
        assert v.postproc["preguntas"][0]["opts"][0]["estadisticas"]["votos_censo"] == 100.0

    # Primero
        assert v.postproc["preguntas"][1]["titulo"] == "Votaci\u00f3n general 2: Elige al delegado de primero"
        assert len(v.postproc["preguntas"][1]["opts"]) == 1
        assert len(v.postproc["preguntas"][1]["opts"][0]["estadisticas"]) == 3
        assert v.postproc["preguntas"][1]["opts"][0]["estadisticas"]["votos_censo"] == 100.0

    # Segundo
        assert v.postproc["preguntas"][2]["titulo"] == "Votaci\u00f3n general 2: Elige al delegado de segundo"
        assert int(len(v.postproc["preguntas"][2]["opts"])) == 1
        assert len(v.postproc["preguntas"][2]["opts"][0]["estadisticas"]) == 3
        assert v.postproc["preguntas"][2]["opts"][0]["estadisticas"]["votos_censo"] == 0

    # Tercero
        assert v.postproc["preguntas"][3]["titulo"] == "Votaci\u00f3n general 2: Elige al delegado de tercero"
        assert int(len(v.postproc["preguntas"][3]["opts"])) == 1
        assert len(v.postproc["preguntas"][3]["opts"][0]["estadisticas"]) == 3
        assert v.postproc["preguntas"][3]["opts"][0]["estadisticas"]["votos_censo"] == 0

    # Cuarto
        assert v.postproc["preguntas"][4]["titulo"] == "Votaci\u00f3n general 2: Elige al delegado de cuarto"
        assert int(len(v.postproc["preguntas"][4]["opts"])) == 1
        assert len(v.postproc["preguntas"][4]["opts"][0]["estadisticas"]) == 3
        assert v.postproc["preguntas"][4]["opts"][0]["estadisticas"]["votos_censo"] == 0
    
    # Master
        assert v.postproc["preguntas"][5]["titulo"] == "Votaci\u00f3n general 2: Elige al delegado del master"
        assert int(len(v.postproc["preguntas"][5]["opts"])) == 1
        assert len(v.postproc["preguntas"][5]["opts"][0]["estadisticas"]) == 3
        assert v.postproc["preguntas"][5]["opts"][0]["estadisticas"]["votos_censo"] == 0

    #Delegación de alumnos
        assert v.postproc["preguntas"][6]["titulo"] == "Votaci\u00f3n general 2: Elige a los miembros de delegaci\u00f3n de alumnos"
        assert int(len(v.postproc["preguntas"][6]["opts"])) == 5
        assert len(v.postproc["preguntas"][6]["opts"][0]["estadisticas"]) == 8
        assert v.postproc["preguntas"][6]["opts"][0]["estadisticas"]["votos_censo"] == 100.0

    def test_votacion_primaria(self):
        
    # Ejecutamos stop, tally y postproc de una votación primaria
        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(5), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')
        Voting.objects.get(id=5).tally_votes(self.token)


        v = Voting.objects.get(id=5)
        assert len(v.postproc["preguntas"]) == 6

    # Estadísticas
        assert v.postproc["estadisticas"] != None
        assert len(v.postproc["estadisticas"]["abstencion"]) == 6
        assert len(v.postproc["estadisticas"]["media_edad"]) == 6
        assert len(v.postproc["estadisticas"]["abstencion_f"]) == 6
        assert len(v.postproc["estadisticas"]["abstencion_m"]) == 6

    # Delegado de centro
        assert v.postproc["preguntas"][0]["titulo"] == "elige representante de delegado de centro de la candidatura \"Candidatura de ejemplo\""
        assert len(v.postproc["preguntas"][0]["opts"]) == 10
        assert len(v.postproc["preguntas"][0]["opts"][0]["estadisticas"]) == 8
        assert v.postproc["preguntas"][0]["opts"][0]["estadisticas"]["votos_censo"] == 100.0

    # Primero
        assert v.postproc["preguntas"][1]["titulo"] == "elige representante de primero de la candidatura \"Candidatura de ejemplo\""
        assert len(v.postproc["preguntas"][1]["opts"]) == 2
        assert len(v.postproc["preguntas"][1]["opts"][0]["estadisticas"]) == 3
        assert v.postproc["preguntas"][1]["opts"][0]["estadisticas"]["votos_censo"] == 100.0

    # Segundo
        assert v.postproc["preguntas"][2]["titulo"] == "elige representante de segundo de la candidatura \"Candidatura de ejemplo\""
        assert int(len(v.postproc["preguntas"][2]["opts"])) == 2
        assert len(v.postproc["preguntas"][2]["opts"][0]["estadisticas"]) == 3
        assert v.postproc["preguntas"][2]["opts"][0]["estadisticas"]["votos_censo"] == 0

    # Tercero
        assert v.postproc["preguntas"][3]["titulo"] == "elige representante de tercero de la candidatura \"Candidatura de ejemplo\""
        assert int(len(v.postproc["preguntas"][3]["opts"])) == 2
        assert len(v.postproc["preguntas"][3]["opts"][0]["estadisticas"]) == 3
        assert v.postproc["preguntas"][3]["opts"][0]["estadisticas"]["votos_censo"] == 0

    # Cuarto
        assert v.postproc["preguntas"][4]["titulo"] == "elige representante de cuarto de la candidatura \"Candidatura de ejemplo\""
        assert int(len(v.postproc["preguntas"][4]["opts"])) == 2
        assert len(v.postproc["preguntas"][4]["opts"][0]["estadisticas"]) == 3
        assert v.postproc["preguntas"][4]["opts"][0]["estadisticas"]["votos_censo"] == 0
    
    # Master
        assert v.postproc["preguntas"][5]["titulo"] == "elige representante de m\u00e1ster de la candidatura \"Candidatura de ejemplo\""
        assert int(len(v.postproc["preguntas"][5]["opts"])) == 2
        assert len(v.postproc["preguntas"][5]["opts"][0]["estadisticas"]) == 3
        assert v.postproc["preguntas"][5]["opts"][0]["estadisticas"]["votos_censo"] == 0
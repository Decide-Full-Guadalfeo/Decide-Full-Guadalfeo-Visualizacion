from voting.models import Voting
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
from selenium.webdriver.common.by import By
from base.tests import BaseTestCase
import time
import re


class VisualizerTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        call_command("loaddata", "test_data_visualizer.json")

    def tearDown(self):
        super().tearDown()
        call_command("flush", interactive=False)

    def test_access_bot_no_admin_404(self):
        data = {}
        self.login(user='franpe', password="complexpassword")
        response = self.client.get('/visualizer/botResults/{}/'.format(1), data, format= 'json')
        self.assertEquals(response.status_code, 404)

    def test_access_bot_404(self):
        data = {}
        self.login()
        response = self.client.get('/visualizer/{}/'.format(-1), data, format= 'json')
        self.assertEquals(response.status_code, 404)

    def test_access_visualizer_200(self):
        data = {}
        self.login()
        response = self.client.get('/visualizer/{}/'.format(1), data, format= 'json')
        self.assertEquals(response.status_code, 200)

    def test_access_visualizer_404(self):
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

    def test_access_contactus_200(self):
        data = {}
        self.login()
        response = self.client.get('/visualizer/contactUs/', data, format= 'json')
        self.assertEquals(response.status_code, 200)

    def test_access_contactus_404(self):
        data = {}
        self.login()
        response = self.client.get('/visualizer/contactUs/{}'.format(-1), data, format= 'json')
        self.assertEquals(response.status_code, 404)

class TestExport(StaticLiveServerTestCase):
    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()

    def test_voting_in_process(self):
        self.driver.get("http://localhost:8000/visualizer/2")
        self.driver.maximize_window()
        assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Votación en curso"

    # def test_voting_is_not_started(self):
    #     self.driver.get("http://localhost:8000/visualizer/3")
    #     self.driver.maximize_window()
    #     assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Votación no comenzada"

    # def test_voting_without_tally(self):
    #     self.driver.get("http://localhost:8000/visualizer/4")
    #     self.driver.maximize_window()
    #     assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Votación sin recuento"

    def test_exportar_PDF(self):
        self.driver.get("http://localhost:8000/visualizer/1")
        self.driver.maximize_window()
        self.driver.find_element(By.LINK_TEXT,"▼ Exportar").click()
        self.driver.find_element(By.LINK_TEXT, "PDF").click()

    def test_exportar_Excel(self):
        self.driver.get("http://localhost:8000/visualizer/1")
        self.driver.maximize_window()
        self.driver.find_element(By.LINK_TEXT,"▼ Exportar").click()
        self.driver.find_element(By.LINK_TEXT, "Excel").click()

    def test_sectores_delegado(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        self.driver.set_window_size(970, 679)
        elements = self.driver.find_elements(By.ID, "tituloGraficosSexo0")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "myPieCharm0-0")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "tituloGraficosCurso0")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "myPieCharmCurso0-0")
        assert len(elements) > 0

    def test_sectores_cursos(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        self.driver.set_window_size(970, 679)
        elements = self.driver.find_elements(By.ID, "tituloGraficosCurso1")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "myPieCharm1-0")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "tituloGraficosCurso2")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "myPieCharm2-0")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "tituloGraficosCurso3")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "myPieCharm3-0")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "tituloGraficosCurso4")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "myPieCharm4-0")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "tituloGraficosCurso5")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "myPieCharm5-0")
        assert len(elements) > 0

    def test_acceso_AboutUs_section(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        self.driver.set_window_size(970, 679)
        self.driver.find_element(By.LINK_TEXT, "About Us").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".body > h1").text == "SOBRE NOSOTROS"

    def test_botones_AboutUs(self):
        self.driver.get("http://localhost:8000/visualizer/aboutUs/")
        self.driver.set_window_size(970, 679)
        self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > .enlace img").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".js-pinned-items-reorder-container > .f4").text == "Popular repositories"

    def test_first_table_present(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_result > .heading")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_titulo0 > .heading")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".display-15 th:nth-child(1) > font")
        assert len(elements) > 0

    def test_middle_tables_presents(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_result > .heading")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_titulo1 > .heading")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_titulo2 > .heading")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_titulo3 > .heading")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_titulo4 > .heading")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_titulo5 > .heading")
        assert len(elements) > 0

    def test_acceso_ContactUs_section(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        self.driver.set_window_size(1936, 1056)
        self.driver.find_element(By.LINK_TEXT, "Contact Us").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".body > h1").text == "¡Contáctanos!"

    def test_botones_ContactUs(self):
        self.driver.get("http://localhost:8000/visualizer/contactUs/")
        self.driver.set_window_size(1936, 1056)
        self.driver.find_element(By.ID, "correoEz").click()

    def test_graficas_barras_first_section_show(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        self.driver.set_window_size(1936, 1056)
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_titulo0 > .heading")
        assert len(elements) > 0
        assert self.driver.find_element(By.CSS_SELECTOR, "#divMyChartVotes0 > h6").text == "Votos de todos los candidatos"
        elements = self.driver.find_elements(By.ID, "myChartVotes0")
        assert len(elements) > 0
        assert self.driver.find_element(By.CSS_SELECTOR, "#divMyChartAges0 > h6").text == "Media de edad de los votantes"
        elements = self.driver.find_elements(By.ID, "myChartAges0")
        assert len(elements) > 0

    def test_graficas_barras_second_section_show(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        self.driver.set_window_size(1936, 1056)
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_titulo1 > .heading")
        assert len(elements) > 0
        assert self.driver.find_element(By.CSS_SELECTOR, "#divMyChartVotes1 > h6").text == "Votos de todos los candidatos"
        elements = self.driver.find_elements(By.ID, "myChartVotes1")
        assert len(elements) > 0
        assert self.driver.find_element(By.CSS_SELECTOR, "#divMyChartAges1 > h6").text == "Media de edad de los votantes"
        elements = self.driver.find_elements(By.ID, "myChartAges1")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_titulo2 > .heading")
        assert len(elements) > 0
        assert self.driver.find_element(By.CSS_SELECTOR, "#divMyChartVotes2 > h6").text == "Votos de todos los candidatos"
        elements = self.driver.find_elements(By.ID, "myChartVotes2")
        assert len(elements) > 0
        assert self.driver.find_element(By.CSS_SELECTOR, "#divMyChartAges2 > h6").text == "Media de edad de los votantes"
        elements = self.driver.find_elements(By.ID, "myChartAges2")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_titulo3 > .heading")
        assert len(elements) > 0
        assert self.driver.find_element(By.CSS_SELECTOR, "#divMyChartVotes3 > h6").text == "Votos de todos los candidatos"
        elements = self.driver.find_elements(By.ID, "myChartVotes3")
        assert len(elements) > 0
        assert self.driver.find_element(By.CSS_SELECTOR, "#divMyChartAges3 > h6").text == "Media de edad de los votantes"
        elements = self.driver.find_elements(By.ID, "myChartAges3")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_titulo4 > .heading")
        assert len(elements) > 0
        assert self.driver.find_element(By.CSS_SELECTOR, "#divMyChartVotes4 > h6").text == "Votos de todos los candidatos"
        elements = self.driver.find_elements(By.ID, "myChartVotes4")
        assert len(elements) > 0
        assert self.driver.find_element(By.CSS_SELECTOR, "#divMyChartAges4 > h6").text == "Media de edad de los votantes"
        elements = self.driver.find_elements(By.ID, "myChartAges4")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_titulo5 > .heading")
        assert len(elements) > 0
        assert self.driver.find_element(By.CSS_SELECTOR, "#divMyChartVotes5 > h6").text == "Votos de todos los candidatos"
        elements = self.driver.find_elements(By.ID, "myChartVotes5")
        assert len(elements) > 0
        assert self.driver.find_element(By.CSS_SELECTOR, "#divMyChartAges5 > h6").text == "Media de edad de los votantes"
        elements = self.driver.find_elements(By.ID, "myChartAges5")
        assert len(elements) > 0

    def test_graficas_barras_third_section_not_show(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        self.driver.set_window_size(1936, 1056)
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_titulo6 > .heading")
        assert len(elements) == 0
        elements = self.driver.find_elements(By.ID, "myChartVotes")
        assert len(elements) == 0
        elements = self.driver.find_elements(By.ID, "myChartAges")
        assert len(elements) == 0

    # def test_graficas_barras_third_section_show(self):
    #     self.driver.get("http://localhost:8000/visualizer//")
    #     self.driver.set_window_size(1936, 1056)
    #     elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_titulo6 > .heading")
    #     assert len(elements) > 0
    #     assert self.driver.find_element(By.CSS_SELECTOR, "#divMyChartVotes6 > h6").text == "Votos de todos los candidatos"
    #     elements = self.driver.find_elements(By.ID, "myChartVotes6")
    #     assert len(elements) > 0
    #     assert self.driver.find_element(By.CSS_SELECTOR, "#divMyChartAges6 > h6").text == "Media de edad de los votantes"
    #     elements = self.driver.find_elements(By.ID, "myChartAges6")
    #     assert len(elements) > 0
        
    def test_last_table_not_present(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_titulo6 > .heading")
        assert len(elements) == 0
        
    def test_light_mode(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        self.driver.set_window_size(1936, 1056)
        color = self.driver.find_elements(By.CSS_SELECTOR, ".dark-mode")
        assert len(color) == 0
    
    def test_dark_mode(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        self.driver.set_window_size(1936, 1056)
        self.driver.find_element(By.CSS_SELECTOR, "p .slider").click()
        color = self.driver.find_elements(By.CSS_SELECTOR, ".dark-mode")
        assert len(color) > 0

    def test_prueba_tablas_estadistica_abstencion(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        elements  = self.driver.find_element(By.CSS_SELECTOR, ".table:nth-child(4) th:nth-child(2)").text
        assert  elements == "Totales" 

    def test_prueba_tablas_estadistica_delegado(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        elements = self.driver.find_element(By.CSS_SELECTOR, ".table:nth-child(7) th:nth-child(1) > font").text
        assert  elements == "Candidato"

    def test_prueba_tablas_estadistica_cursos(self):
        self.driver.get("http://localhost:8000/visualizer/1/")   
        elements  =self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(8) > .table th:nth-child(1)").text
        assert  elements == "Candidato"
        elements  =self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(9) > .table th:nth-child(1)").text
        assert  elements == "Candidato"
        elements  =self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(10) th:nth-child(1)").text
        assert  elements == "Candidato"
        elements  =self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(11) th:nth-child(1)").text
        assert  elements == "Candidato"
        elements  =self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(12) th:nth-child(1)").text
        assert  elements == "Candidato"

    # Estas pruebas son para cuando se pueda testear mirar que no haya tabla delegacion de alumno en una primaria y testear que si la haya en una general

    # def test_pruebatablassestadistica(self):
    #     self.driver.get("http://localhost:8000/visualizer/1/")    
    #     elements = self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(8) > .table th:nth-child(1)").text()
    #     assert  elements == "Candidato"

    # def test_pruebatablassestadistica(self):
    #     self.driver.get("http://localhost:8000/visualizer/1/")    
    #     elements = self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(8) > .table th:nth-child(1)").text()
    #     assert  elements != "Candidato"


    #================================================================================


    # def test_last_table_present(self):
    #     self.driver.get("http://localhost:8000/visualizer//")
    #     elements = self.driver.find_elements(By.CSS_SELECTOR, "#enun_titulo6 > .heading")
    #     assert len(elements) > 0

    def test_join_telegram(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        self.driver.find_element(By.LINK_TEXT, "▼ Telegram").click()
        valor = self.driver.find_element(By.LINK_TEXT, "Unirse al canal de Telegram").get_attribute("href")
        self.driver.get(valor)
        elements = self.driver.find_elements(By.XPATH, "//span[contains(.,\'guadalfeo-visualizacion\')]")
        assert len(elements) > 0

    def test_share_whatsapp(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        self.driver.find_element(By.LINK_TEXT, "▼ Compartir").click()
        valor = self.driver.find_element(By.LINK_TEXT, "Whatsapp").get_attribute("href")
        self.driver.get(valor)
        url = self.driver.current_url
        pattern = re.compile("^https://api.whatsapp.com/")
        assert pattern.match(url)

    def test_share_twitter(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        self.driver.find_element(By.LINK_TEXT, "▼ Compartir").click()
        valor = self.driver.find_element(By.LINK_TEXT, "Twitter").get_attribute("href")
        self.driver.get(valor)
        url = self.driver.current_url
        pattern = re.compile("^https://twitter.com/")
        assert pattern.match(url)

    def test_share_facebook(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        self.driver.find_element(By.LINK_TEXT, "▼ Compartir").click()
        valor = self.driver.find_element(By.LINK_TEXT, "Facebook").get_attribute("href")
        self.driver.get(valor)
        url = self.driver.current_url
        pattern = re.compile("^https://www.facebook.com/")
        assert pattern.match(url)
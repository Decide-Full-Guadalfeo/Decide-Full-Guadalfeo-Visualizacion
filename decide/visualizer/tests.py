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

    def voting_in_process(self):
        self.driver.get("http://localhost:8000/visualizer/2")
        self.driver.maximize_window()
        self.assertTrue(self.driver.find_element_by_css_selector('h2')=="Votación en curso")

    def voting_is_not_started(self):
        self.driver.get("http://localhost:8000/visualizer/3")
        self.driver.maximize_window()
        self.assertTrue(self.driver.find_element_by_css_selector('h2')=="Votación no comenzada")

    def voting_without_tally(self):
        self.driver.get("http://localhost:8000/visualizer/4")
        self.driver.maximize_window()
        self.assertTrue(self.driver.find_element_by_css_selector('h2')=="Votación sin recuento")

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

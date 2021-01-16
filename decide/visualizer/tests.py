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

class TesExport(StaticLiveServerTestCase):
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

    def test_voting_is_not_started(self):
        self.driver.get("http://localhost:8000/visualizer/3")
        self.driver.maximize_window()
        assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Votación no comenzada"

    def test_voting_without_tally(self):
        self.driver.get("http://localhost:8000/visualizer/4")
        self.driver.maximize_window()
        assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Votación sin recuento"
        
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

    def test_grafico_sectores_vsexo(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        self.driver.set_window_size(1550, 838)
        self.driver.find_element(By.ID, "tituloGraficosSexo0").click()
        self.driver.find_element(By.ID, "myPieCharm0-0").click()
        self.assertTrue(self.driver.find_element_by_id('tituloGraficosSexo0')!=None)
        self.assertTrue(self.driver.find_element_by_id('myPieCharm0-0')!=None)  

    def test_grafico_sectores_vcurso(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        self.driver.set_window_size(969, 677)
        self.driver.find_element(By.ID, "tituloGraficosCurso0").click()
        self.driver.find_element(By.ID, "myPieCharmCurso0-0").click()
        self.assertTrue(self.driver.find_element_by_id('tituloGraficosCurso0')!=None)
        self.assertTrue(self.driver.find_element_by_id('myPieCharmCurso0-0')!=None) 

    def test_aboutus_link(self):
        self.driver.get("http://localhost:8000/visualizer/1/")
        self.driver.set_window_size(969, 677)
        elements = self.driver.find_elements(By.LINK_TEXT, "About Us")
        assert len(elements) > 0

    def test_aboutus_section(self):
        self.driver.get("http://localhost:8000/visualizer/aboutUs/")
        self.driver.set_window_size(969, 677)
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".body > h1")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "h2")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "p")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "b")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "th:nth-child(1)")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, "tr:nth-child(2) > td:nth-child(1)")
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
        


from voting.models import Voting, Question, QuestionOption
from mixnet.models import Auth
from django.conf import settings
from pathlib import Path

# Create your tests here.
from base.tests import BaseTestCase
import json

class VisualizerTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def create_voting(self,opt_number=5):
        q = Question(desc='test question')
        q.save()
        for i in range(opt_number):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
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

    def test_access_bot_200(self):
        v = self.create_voting()
        data = {} #El campo action es requerido en la request
        self.login()
        response = self.client.get('/visualizer/botResults/{}/'.format(v.pk), data, format= 'json')
        self.assertEquals(response.status_code, 200)

    def test_access_bot_400(self):
        data = {} #El campo action es requerido en la request
        self.login()
        response = self.client.get('/visualizer/botResults/{}/'.format(-1), data, format= 'json')
        self.assertEquals(response.status_code, 404)

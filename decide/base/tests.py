from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class BaseTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.token = None
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None
        self.token = None

    def login(self, user='admin', password='complexpassword'):
        data = {'username': user, 'password': password}
        response = mods.post('authentication/login', json=data, response=True)
        self.assertEqual(response.status_code, 200)
        self.token = response.json().get('token')
        self.assertTrue(self.token)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def logout(self):
        self.client.credentials()

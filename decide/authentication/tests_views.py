from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from .models import VotingUser
from rest_framework.authtoken.models import Token
from .forms import RegisterVotingUserForm, CustomUserCreationForm

from base import mods
from parameterized import parameterized


class AuthTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u1 = User(first_name='User', last_name='Voting', username='voter1')
        u1.set_password('123')
        u1.save()
        self.user1 = u1
        t1 = Token(user=u1)
        t1.save()
        self.token1 = t1

        u2 = User(first_name='User', last_name='Voting2', username='voter2', email='voter2@gmail.com')
        u2.set_password('123')
        u2.save()
        self.user2 = u2
        vu2 = VotingUser(user=u2, dni='45454545T', sexo='Man', titulo='Software', curso='First', edad=18)
        vu2.save()
        self.votingUser = vu2
        t2 = Token(user=u2)
        t2.save()
        self.token2 = t2

        u3 = User(first_name='User', last_name='Voting3', username='voter3')
        u3.set_password('123')
        u3.save()
        self.user3 = u3

    def tearDown(self):
        self.client = None

    def generate_data(self, first_name="User", last_name="Voting", username="username1999",
                      email="username1999@gmail.com", password1="password1234", password2="password1234",
                      dni="11112222A", sexo="Woman", titulo="Software", curso="First", candidatura="", edad="18"):

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "password1": password1,
            "password2": password2,
            "dni": dni,
            "sexo": sexo,
            "titulo": titulo,
            "curso": curso,
            "candidatura": candidatura,
            "edad": edad
        }
        return data

    def test_get_index_view(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/index.html')

    def test_get_register_anonymous(self):
        response = self.client.get('/authentication/decide/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'votingusers/registro.html')

        user_form = response.context['user_form']
        self.assertIsInstance(user_form, CustomUserCreationForm)
        votinguser_form = response.context['votinguser_form']
        self.assertIsInstance(votinguser_form, RegisterVotingUserForm)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_get_register_logged_user_incomplete_profile(self):
        self.client.force_authenticate(self.user1)

        response = self.client.get('/authentication/decide/register/')
        self.assertRedirects(response, '/authentication/decide/register/complete/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_get_register_logged_user_complete_profile(self):
        self.client.force_authenticate(self.user2)

        response = self.client.get('/authentication/decide/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'votingusers/registro.html')
        self.assertNotIn('user_form', response.context)
        self.assertNotIn('votinguser_form', response.context)

    def test_register_correct(self):
        self.assertTrue(User.objects.count() == 3)

        response = self.client.get('/authentication/decide/register/')
        csrftoken = response.cookies['csrftoken']
        self.assertEqual(response.status_code, 200)

        data = self.generate_data()
        response = self.client.post('/authentication/decide/register/', data=data, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            'X-CSRFToken': csrftoken
        })

        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertTrue(User.objects.count() == 4)
        self.assertTrue(User.objects.filter(username="username1999").count() == 1)

    @parameterized.expand(["", " "])
    def test_register_empty_fields(self, blank):
        self.assertTrue(User.objects.count() == 3)

        response = self.client.get('/authentication/decide/register/')
        csrftoken = response.cookies['csrftoken']
        self.assertEqual(response.status_code, 200)

        data = self.generate_data(first_name=blank, last_name=blank, username=blank, password1=blank, password2=blank,
                                  dni=blank)
        response = self.client.post('/authentication/decide/register/', data=data, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            'X-CSRFToken': csrftoken
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'votingusers/registro.html')

        user_form = response.context['user_form']
        self.assertIsInstance(user_form, CustomUserCreationForm)
        # self.assertEqual(len(user_form.errors),5)
        self.assertEqual(user_form.errors["first_name"], ["This field is required."])
        self.assertEqual(user_form.errors["last_name"], ["This field is required."])
        self.assertEqual(user_form.errors["username"], ["This field is required."])
        if blank == " ":
            self.assertEqual(user_form.errors["password2"],
                             ["This password is too short. It must contain at least 8 characters."])
        else:
            self.assertEqual(user_form.errors["password1"], ["This field is required."])
            self.assertEqual(user_form.errors["password2"], ["This field is required."])

        votinguser_form = response.context['votinguser_form']
        self.assertIsInstance(votinguser_form, RegisterVotingUserForm)
        self.assertEqual(len(votinguser_form.errors), 1)
        self.assertEqual(votinguser_form.errors["dni"], ["This field is required."])

        self.assertTrue(User.objects.count() == 3)

    def test_register_duplicated_username(self):
        self.assertTrue(User.objects.count() == 3)

        response = self.client.get('/authentication/decide/register/')
        csrftoken = response.cookies['csrftoken']
        self.assertEqual(response.status_code, 200)

        data = self.generate_data(username="voter1")
        response = self.client.post('/authentication/decide/register/', data=data, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            'X-CSRFToken': csrftoken
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'votingusers/registro.html')

        user_form = response.context['user_form']
        self.assertIsInstance(user_form, CustomUserCreationForm)
        self.assertEqual(len(user_form.errors), 1)
        self.assertEqual(user_form.errors["username"], ["A user with that username already exists."])

        votinguser_form = response.context['votinguser_form']
        self.assertIsInstance(votinguser_form, RegisterVotingUserForm)
        self.assertEqual(len(votinguser_form.errors), 0)

        self.assertTrue(User.objects.count() == 3)

    def test_register_duplicated_email(self):
        self.assertTrue(User.objects.count() == 3)

        response = self.client.get('/authentication/decide/register/')
        csrftoken = response.cookies['csrftoken']
        self.assertEqual(response.status_code, 200)

        data = self.generate_data(email="voter2@gmail.com")
        response = self.client.post('/authentication/decide/register/', data=data, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            'X-CSRFToken': csrftoken
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'votingusers/registro.html')

        user_form = response.context['user_form']
        self.assertIsInstance(user_form, CustomUserCreationForm)
        self.assertEqual(len(user_form.errors), 1)
        self.assertEqual(user_form.errors["email"], ["This email is already in use"])

        votinguser_form = response.context['votinguser_form']
        self.assertIsInstance(votinguser_form, RegisterVotingUserForm)
        self.assertEqual(len(votinguser_form.errors), 0)

        self.assertTrue(User.objects.count() == 3)

    def test_register_duplicated_dni(self):
        self.assertTrue(User.objects.count() == 3)

        response = self.client.get('/authentication/decide/register/')
        csrftoken = response.cookies['csrftoken']
        self.assertEqual(response.status_code, 200)

        data = self.generate_data(dni="45454545T")
        response = self.client.post('/authentication/decide/register/', data=data, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            'X-CSRFToken': csrftoken
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'votingusers/registro.html')

        user_form = response.context['user_form']
        self.assertIsInstance(user_form, CustomUserCreationForm)
        self.assertEqual(len(user_form.errors), 0)

        votinguser_form = response.context['votinguser_form']
        self.assertIsInstance(votinguser_form, RegisterVotingUserForm)
        self.assertEqual(len(votinguser_form.errors), 1)
        self.assertEqual(votinguser_form.errors["dni"], ["Voting user with this NIF already exists."])

        self.assertTrue(User.objects.count() == 3)

    @parameterized.expand(["username1999", "pass12", "password", "87512396"])
    def test_register_wrong_password_format(self, password):
        self.assertTrue(User.objects.count() == 3)

        response = self.client.get('/authentication/decide/register/')
        csrftoken = response.cookies['csrftoken']
        self.assertEqual(response.status_code, 200)

        data = self.generate_data(password1=password, password2=password)
        response = self.client.post('/authentication/decide/register/', data=data, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            'X-CSRFToken': csrftoken
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'votingusers/registro.html')

        user_form = response.context['user_form']
        self.assertIsInstance(user_form, CustomUserCreationForm)
        self.assertEqual(len(user_form.errors), 1)
        if password == "username1999":
            self.assertEqual(user_form.errors["password2"], ["The password is too similar to the username."])
        if password == "pass12":
            self.assertEqual(user_form.errors["password2"],
                             ["This password is too short. It must contain at least 8 characters."])
        if password == "password":
            self.assertEqual(user_form.errors["password2"], ["This password is too common."])
        if password == "12345678":
            self.assertEqual(user_form.errors["password2"], ["This password is entirely numeric."])

        votinguser_form = response.context['votinguser_form']
        self.assertIsInstance(votinguser_form, RegisterVotingUserForm)
        self.assertEqual(len(votinguser_form.errors), 0)

        self.assertTrue(User.objects.count() == 3)

    def test_register_different_passwords(self):
        self.assertTrue(User.objects.count() == 3)

        response = self.client.get('/authentication/decide/register/')
        csrftoken = response.cookies['csrftoken']
        self.assertEqual(response.status_code, 200)

        data = self.generate_data(password2="1234password")
        response = self.client.post('/authentication/decide/register/', data=data, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            'X-CSRFToken': csrftoken
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'votingusers/registro.html')

        user_form = response.context['user_form']
        self.assertIsInstance(user_form, CustomUserCreationForm)
        self.assertEqual(len(user_form.errors), 1)
        self.assertEqual(user_form.errors["password2"], ["The two password fields didn't match."])

        votinguser_form = response.context['votinguser_form']
        self.assertIsInstance(votinguser_form, RegisterVotingUserForm)
        self.assertEqual(len(votinguser_form.errors), 0)

        self.assertTrue(User.objects.count() == 3)

    @parameterized.expand(["16", "101", ])
    def test_register_wrong_age(self, edad):
        self.assertTrue(User.objects.count() == 3)

        response = self.client.get('/authentication/decide/register/')
        csrftoken = response.cookies['csrftoken']
        self.assertEqual(response.status_code, 200)

        data = self.generate_data(edad=edad)
        response = self.client.post('/authentication/decide/register/', data=data, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            'X-CSRFToken': csrftoken
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'votingusers/registro.html')

        user_form = response.context['user_form']
        self.assertIsInstance(user_form, CustomUserCreationForm)
        self.assertEqual(len(user_form.errors), 0)

        votinguser_form = response.context['votinguser_form']
        self.assertIsInstance(votinguser_form, RegisterVotingUserForm)
        self.assertEqual(len(votinguser_form.errors), 1)
        if int(edad) < 17:
            self.assertEqual(votinguser_form.errors["edad"], ["Ensure this value is greater than or equal to 17."])
        if int(edad) > 100:
            self.assertEqual(votinguser_form.errors["edad"], ["Ensure this value is less than or equal to 100."])

        self.assertTrue(User.objects.count() == 3)

    def test_get_user(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_user_anonymous(self):
        data = {}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 400)


    def test_get_user_without_token(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/authentication/getuser/', format='json')
        self.assertEqual(response.status_code, 404)

    def test_get_user_incomplete_profile(self):
        data = {'username': 'voter1'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    #Test GetUserDetailsView

    def test_get_user_details(self):
        response = self.client.get('/user/1/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_user_details_invalid_id(self):
        response = self.client.get('/user/', format='json')
        self.assertEqual(response.status_code, 404)

    def test_post_user_details_invalid_id(self):
        response = self.client.post('/user/', format='json')
        self.assertEqual(response.status_code, 404)

    #CompleteVotingUserDetails

    def test_get_complete_voting_user_details(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get('/decide/register/complete/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_post_complete_voting_user_details(self):
        response = self.client.post('/decide/register/complete/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        self.client.logout()
        LOGIN_URL = '/authentication/decide/login/'

        response = self.client.get(LOGIN_URL)
        csrftoken = response.cookies['csrftoken']
        self.assertEqual(response.status_code, 200)

        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post(LOGIN_URL, data=data, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            'X-CSRFToken': csrftoken
        })
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_login_fail_incorrect_credentials(self):

        self.client.logout()
        LOGIN_URL = '/authentication/decide/login/'

        response = self.client.get(LOGIN_URL)
        csrftoken = response.cookies['csrftoken']
        self.assertEqual(response.status_code, 200)

        data = {'username': 'voter1', 'password': '543'}
        response = self.client.post(LOGIN_URL, data=data, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            'X-CSRFToken': csrftoken,
        })

        self.assertRedirects(response, '/authentication/decide/login', status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    def test_logout(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get('/authentication/decide/logout/')
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=False)


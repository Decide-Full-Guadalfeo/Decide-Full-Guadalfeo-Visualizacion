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
        u1 = User(username='voter1')
        u1.set_password('123')
        u1.save()
        self.user1 = u1
        t1 = Token(user=u1)
        t1.save()
        self.token1 = t1

        u2 = User(username='voter2', email='voter2@gmail.com')
        u2.set_password('123')
        u2.save()
        self.user2 = u2
        vu2 = VotingUser(user=u2, dni='45454545T', sexo='Man', titulo='Software', curso='First', edad=18)
        vu2.save()
        self.votingUser = vu2
        t2 = Token(user=u2)
        t2.save()
        self.token2 = t2

        u3 = User(username='voter3')
        u3.set_password('123')
        u3.save()
        self.user3 = u3

    def tearDown(self):
        self.client = None

    def generate_data(self,username="username1999",email="username1999@gmail.com",password1="password1234",password2="password1234",
            dni="11112222A",sexo="Woman",titulo="Software",curso="First",candidatura="",edad="18"):

        data = {
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

    def test_get_register_anonymous(self):
        self.client.logout()
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
        self.assertRedirects(response, '/authentication/decide/register/complete/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_get_register_logged_user_complete_profile(self):
        self.client.force_authenticate(self.user2)

        response = self.client.get('/authentication/decide/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'votingusers/registro.html')
        self.assertNotIn('user_form', response.context)
        self.assertNotIn('votinguser_form', response.context)

    def test_register_correct(self):
        self.client.logout()
        response = self.client.get('/authentication/decide/register/')
        csrftoken = response.cookies['csrftoken']
        self.assertEqual(response.status_code, 200)

        data = self.generate_data()
        response = self.client.post('/authentication/decide/register/', data=data, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            'X-CSRFToken': csrftoken
        })

        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_register_empty_fields(self):
        self.client.logout()
        response = self.client.get('/authentication/decide/register/')
        csrftoken = response.cookies['csrftoken']
        self.assertEqual(response.status_code, 200)

        data = self.generate_data(username="",password1="",password2="",dni="")
        response = self.client.post('/authentication/decide/register/', data=data, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            'X-CSRFToken': csrftoken
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'votingusers/registro.html')

        user_form = response.context['user_form']
        self.assertIsInstance(user_form, CustomUserCreationForm)
        self.assertEqual(len(user_form.errors),3)
        self.assertEqual(user_form.errors["username"], ["This field is required."])
        self.assertEqual(user_form.errors["password1"], ["This field is required."])
        self.assertEqual(user_form.errors["password2"], ["This field is required."])
        
        votinguser_form = response.context['votinguser_form']
        self.assertIsInstance(votinguser_form, RegisterVotingUserForm)
        self.assertEqual(len(votinguser_form.errors),1)
        self.assertEqual(votinguser_form.errors["dni"], ["This field is required."])

    def test_register_duplicated_username(self):
        self.client.logout()
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
        self.assertEqual(len(user_form.errors),1)
        self.assertEqual(user_form.errors["username"], ["A user with that username already exists."])
        
        votinguser_form = response.context['votinguser_form']
        self.assertIsInstance(votinguser_form, RegisterVotingUserForm)
        self.assertEqual(len(votinguser_form.errors),0)

    def test_register_duplicated_email(self):
        self.client.logout()
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
        self.assertEqual(len(user_form.errors),1)
        self.assertEqual(user_form.errors["email"], ["This email is already in use"])
        
        votinguser_form = response.context['votinguser_form']
        self.assertIsInstance(votinguser_form, RegisterVotingUserForm)
        self.assertEqual(len(votinguser_form.errors),0)

    def test_register_duplicated_dni(self):
        self.client.logout()
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
        self.assertEqual(len(user_form.errors),0)
        
        votinguser_form = response.context['votinguser_form']
        self.assertIsInstance(votinguser_form, RegisterVotingUserForm)
        self.assertEqual(len(votinguser_form.errors),1)
        self.assertEqual(votinguser_form.errors["dni"], ["Voting user with this NIF already exists."])

    @parameterized.expand(["username1999","pass12","password","87512396"])
    def test_register_wrong_password_format(self,password):
        self.client.logout()
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
        self.assertEqual(len(user_form.errors),1)
        if password == "username1999":
            self.assertEqual(user_form.errors["password2"], ["The password is too similar to the username."])
        if password == "pass12":
            self.assertEqual(user_form.errors["password2"], ["This password is too short. It must contain at least 8 characters."])
        if password == "password":
            self.assertEqual(user_form.errors["password2"], ["This password is too common."])
        if password == "12345678":
            self.assertEqual(user_form.errors["password2"], ["This password is entirely numeric."])
        
        votinguser_form = response.context['votinguser_form']
        self.assertIsInstance(votinguser_form, RegisterVotingUserForm)
        self.assertEqual(len(votinguser_form.errors),0)

    def test_register_different_passwords(self):
        self.client.logout()
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
        self.assertEqual(len(user_form.errors),1)
        self.assertEqual(user_form.errors["password2"], ["The two password fields didn't match."])
        
        votinguser_form = response.context['votinguser_form']
        self.assertIsInstance(votinguser_form, RegisterVotingUserForm)
        self.assertEqual(len(votinguser_form.errors),0)

    @parameterized.expand(["16","101",])
    def test_register_wrong_age(self,edad):
        self.client.logout()
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
        self.assertEqual(len(user_form.errors),0)
        
        votinguser_form = response.context['votinguser_form']
        self.assertIsInstance(votinguser_form, RegisterVotingUserForm)
        self.assertEqual(len(votinguser_form.errors),1)
        if int(edad) < 17:
            self.assertEqual(votinguser_form.errors["edad"], ["Ensure this value is greater than or equal to 17."])
        if int(edad) > 100:
            self.assertEqual(votinguser_form.errors["edad"], ["Ensure this value is less than or equal to 100."])

    #API

    def test_get_voting_user_anonymous(self):
        self.client.logout()

        response = self.client.post('/authentication/decide/getVotingUser/', follow=True)

        self.assertRedirects(response, '/authentication/decide/login/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You must be logged to access there!')

    def test_get_voting_user_without_token(self):
        self.client.force_authenticate(self.user3)

        response = self.client.post('/authentication/decide/getVotingUser/', follow=True)

        self.assertRedirects(response, '/authentication/decide/login/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'User not valid!')

    def test_get_voting_user_incomplete_profile(self):
        self.client.force_authenticate(self.user1)

        response = self.client.post('/authentication/decide/getVotingUser/', follow=True)

        self.assertRedirects(response, '/authentication/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Finish setting your user account!')

    def test_get_voting_user_complete_profile(self):
        self.client.force_authenticate(self.user2)

        response = self.client.post('/authentication/decide/getVotingUser/', follow=True)

        self.assertEqual(response.status_code, 200)


    '''def test_login(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('token'))

    def test_login_fail(self):
        data = {'username': 'voter1', 'password': '321'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_getuser(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 200)

        user = response.json()
        self.assertEqual(user['id'], 1)
        self.assertEqual(user['username'], 'voter1')

    def test_getuser_invented_token(self):
        token = {'token': 'invented'}
        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_getuser_invalid_token(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 0)

    def test_register_bad_permissions(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 401)

    def test_register_bad_request(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register_user_already_exist(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update(data)
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1', 'password': 'pwd1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            sorted(list(response.json().keys())),
            ['token', 'user_pk']
        )'''

from django.test import TestCase
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from parameterized import parameterized

class CustomUserCreationFormTests(TestCase):

    def setUp(self):
        u1 = User(first_name='User',last_name='Voting',username='voter1', email='voter1@gmail.com')
        u1.set_password('123')
        u1.save()

    def test_fields_and_labels(self):
        form = CustomUserCreationForm()
        self.assertTrue(len(form.fields) == 6)
        self.assertTrue(form.fields['first_name'])
        self.assertTrue(form.fields['first_name'].label == 'First name')
        self.assertTrue(form.fields['last_name'])
        self.assertTrue(form.fields['last_name'].label == 'Last name')
        self.assertTrue(form.fields['username'])
        self.assertTrue(form.fields['username'].label == 'Username')
        self.assertTrue(form.fields['email'])
        self.assertTrue(form.fields['email'].label == 'Email address')
        self.assertTrue(form.fields['password1'])
        self.assertTrue(form.fields['password1'].label == 'Password')
        self.assertTrue(form.fields['password2'])
        self.assertTrue(form.fields['password2'].label == 'Password confirmation')

    @parameterized.expand(["voter2@gmail.com",""," "])
    def test_form_valid(self,email):
        form = CustomUserCreationForm(data={"first_name":"User","last_name":"Voting","username":"voter2","email":email,"password1":"password1234","password2":"password1234"})
        self.assertTrue(form.is_valid())

    @parameterized.expand([""," "])
    def test_form_first_name_required(self,first_name):
        form = CustomUserCreationForm(data={"first_name":first_name,"last_name":"Voting","username":"voter2","email": "voter2@gmail.com","password1":"password1234","password2":"password1234"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["first_name"], ["This field is required."])

    @parameterized.expand([""," "])
    def test_form_last_name_required(self,last_name):
        form = CustomUserCreationForm(data={"first_name":"User","last_name":last_name,"username":"voter2","email": "voter2@gmail.com","password1":"password1234","password2":"password1234"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["last_name"], ["This field is required."])

    def test_form_not_valid_duplicated_email(self):
        form = CustomUserCreationForm(data={"first_name":"User","last_name":"Voting","username":"voter2","email": "voter1@gmail.com","password1":"password1234","password2":"password1234"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["This email is already in use"])
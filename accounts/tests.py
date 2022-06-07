import email
import imp
from urllib import response
from django.test import TestCase,Client
from . import views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your tests here.

class UserCreation(TestCase):    
    def test_UserCreationForm(self):
        form = UserCreationForm(data={
            'username': 'testuser',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456',
        })
        self.assertTrue(form.is_valid())
        form.save()
        user = User.objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('abcdef123456'))
        
class AccountTest(TestCase):
    def setUp(self):
        self.data = {
            'username': 'testuser',
            'password': 'abcdef123456',
        }
        self.data2 = {
            'username': 'testuser2',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456',
        }
        User.objects.create_user(**self.data)
        form = UserCreationForm(data=self.data2)
        if form.is_valid:
            form.save()
    def test_login(self):
        response = self.client.login(username= 'testuser', password= 'abcdef123456')
        self.assertEqual(response, True)
    def test_logout(self):
        self.client.login(username= 'testuser', password= 'abcdef123456')
        response = self.client.logout()
        self.assertEqual(response, None)
    def test_login_API(self):
        response = self.client.post('/accounts/login/', self.data, follow=True)
        self.assertTrue(response.context['user'].is_active)
        self.assertEqual(response.status_code, 200)
    def test_logout_API(self):
        self.client.login(username= 'testuser', password= 'abcdef123456')
        response = self.client.post('/accounts/logout/', follow=True)
        self.assertFalse(response.context['user'].is_active)
        self.assertEqual(response.status_code, 200)
    def test_register_API(self):
        response = self.client.post('/accounts/register/', self.data2, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.login(username= 'testuser2', password= 'abcdef123456')
        self.assertTrue(response)
    def test_editAccount(self):
        # Check used correct template
        response = self.client.get('/accounts/edit/1')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'registration/editAccount.html')
        # Check User correctly edited
        response = self.client.post('/accounts/edit/1', data = 
                                                        {'username': 'testuser3',
                                                        'password1': 'abcdef123456',
                                                        'password2': 'abcdef123456'},
                                                        follow=True)
        self.assertEqual(response.status_code,200)
        self.assertRedirects(response, '/')
        self.client.login(username= 'testuser3', password= 'abcdef123456')
        self.assertTrue(response)
        # Check User doesn't exit
        response = self.client.get('/accounts/edit/3')
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response, '/accounts/register/')
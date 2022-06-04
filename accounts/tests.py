import email
import imp
from django.test import TestCase
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
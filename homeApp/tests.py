from django.test import TestCase
from django.urls import resolve
from . import views
# Create your tests here.
class TestHomePage(TestCase):
    def test_homepage_resolves(self):
        home_page = resolve('/')
        self.assertEqual(home_page.func, views.home)
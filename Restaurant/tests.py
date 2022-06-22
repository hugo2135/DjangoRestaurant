from django.test import TestCase
from django.urls import resolve
from Restaurant.models import Restaurant
from Restaurant import forms
from django.contrib.auth.models import User
from django import setup
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RestaurantRecommendSystem.settings')
setup()

class ResturantModelTestCase(TestCase):
    def setUp(self):
        Restaurant.objects.create(Name='Pizza Palace', Style='Italian', Price=100,
                                         Img='None',Distance=1.5, Address='清水河畔', Rating=4.5)
        Restaurant.objects.create(Name='Bobs BBQ', Style='BBQ', Price=65, 
                                         Img='None',Distance=3, Address='農安街', Rating=1.5)
    
    def test_returant_name(self):
        resturant1 = Restaurant.objects.get(Name='Pizza Palace')
        self.assertEqual(resturant1.Name, 'Pizza Palace')
        resturant2 = Restaurant.objects.get(Name='Bobs BBQ')
        self.assertEqual(resturant2.Name, 'Bobs BBQ')
        
    def test_resturant_style(self):
        resturant1 = Restaurant.objects.get(Name='Pizza Palace')
        self.assertEqual(resturant1.Style, 'Italian')
        resturant2 = Restaurant.objects.get(Name='Bobs BBQ')
        self.assertEqual(resturant2.Style, 'BBQ')
        
    def test_resturant_price(self):
        resturant1 = Restaurant.objects.get(Name='Pizza Palace')
        self.assertEqual(resturant1.Price, 100)
        resturant2 = Restaurant.objects.get(Name='Bobs BBQ')
        self.assertEqual(resturant2.Price, 65)
        
    def test_resturant_img(self):
        resturant1 = Restaurant.objects.get(Name='Pizza Palace')
        self.assertEqual(resturant1.Img, 'None')
        resturant2 = Restaurant.objects.get(Name='Bobs BBQ')
        self.assertEqual(resturant2.Img, 'None')
        
    def test_resturant_distance(self):
        resturant1 = Restaurant.objects.get(Name='Pizza Palace')
        self.assertEqual(resturant1.Distance, 1.5)
        resturant2 = Restaurant.objects.get(Name='Bobs BBQ')
        self.assertEqual(resturant2.Distance, 3)
    
    def test_resturant_address(self):
        resturant1 = Restaurant.objects.get(Name='Pizza Palace')
        self.assertEqual(resturant1.Address, '清水河畔')
        resturant2 = Restaurant.objects.get(Name='Bobs BBQ')
        self.assertEqual(resturant2.Address, '農安街')
        
    def test_resturant_rating(self):
        resturant1 = Restaurant.objects.get(Name='Pizza Palace')
        self.assertEqual(resturant1.Rating, 4.5)
        resturant2 = Restaurant.objects.get(Name='Bobs BBQ')
        self.assertEqual(resturant2.Rating, 1.5)
        
class TestResturantViewLoggedIn(TestCase):
    def setUp(self):
        #Simulate 2 resturants
        resturant1 = Restaurant.objects.create(Name='Pizza Palace', Style='Italian', Price=100,
                                         Img='None',Distance=1.5, Address='清水河畔', Rating=4.5)
        resturant2 = Restaurant.objects.create(Name='Bobs BBQ', Style='BBQ', Price=65, 
                                         Img='None',Distance=3, Address='農安街', Rating=1.5)
        forms.RestaurantCreate(resturant1)
        forms.RestaurantCreate(resturant2)
        
        # Simulate a logged in user
        User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.added_data= {'Name':"Kevin's BBQ", 'Style':'BBQ', 'Price':500,
                     'Img':'None','Distance':6, 'Address':'行天宮', 'Rating':4.5}
    def test_resolve_to_homepage(self):
        resolver = resolve('/')                                   #我有改基底url，這邊就一起動了
        self.assertEqual(resolver.view_name, 'index')
        
        
    def test_get_homepage(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'Restaurant/listRestaurant.html')
        self.assertEqual(response.status_code, 200)
        
    def test_get_addRestaurant(self):
        # Check used correct template
        response = self.client.get('/add/')
        self.assertTemplateUsed(response, 'Restaurant/editRestaurant.html')
        self.assertEqual(response.status_code, 200)
        # Check Resturant correctly added
        response = self.client.post('/add/', self.added_data, follow=True)
        resturant = Restaurant.objects.get(id=3)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/')
        self.assertEqual(resturant.Name, "Kevin's BBQ")
        
    def test_get_editRestaurant(self):
        # Check used correct template
        response_1 = self.client.get('/resturant/edit/1')
        self.assertEqual(response_1.status_code, 200)
        self.assertTemplateUsed(response_1, 'Restaurant/editRestaurant.html')
        response_2 = self.client.get('/resturant/edit/2')
        self.assertEqual(response_2.status_code, 200)
        self.assertTemplateUsed(response_2, 'Restaurant/editRestaurant.html')
        # Check Resturant correctly edited
        response = self.client.post('/resturant/edit/1', self.added_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/')
        resturant = Restaurant.objects.get(id=1)
        self.assertEqual(resturant.Name, "Kevin's BBQ")
        
    def test_get_deleteRestaurant(self):
        count = Restaurant.objects.all().count()
        self.assertEqual(count,2)
        response = self.client.post('/resturant/delete/1', follow=True)
        count = Restaurant.objects.all().count()
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/')
        self.assertEqual(count,1)
class TestResturantViewNotLoggedIn(TestCase):
    def setUp(self):
        #Simulate 2 resturants
        resturant1 = Restaurant.objects.create(Name='Pizza Palace', Style='Italian', Price=100,
                                         Img='None',Distance=1.5, Address='清水河畔', Rating=4.5)
        resturant2 = Restaurant.objects.create(Name='Bobs BBQ', Style='BBQ', Price=65, 
                                         Img='None',Distance=3, Address='農安街', Rating=1.5)
        forms.RestaurantCreate(resturant1)
        forms.RestaurantCreate(resturant2)
        
    def test_get_addRestaurant_No(self):
        response = self.client.get('/add/')
        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 302)
        
    def test_get_editRestaurant_No(self):
        response_1 = self.client.get('/resturant/edit/1')
        self.assertRedirects(response_1, '/')
        self.assertEqual(response_1.status_code, 302)
        response_2 = self.client.get('/resturant/edit/2')
        self.assertRedirects(response_2, '/')
        self.assertEqual(response_2.status_code, 302)
        
    def test_get_deleteRestaurant_No(self):
        # Make sure before delete there are 2 resturants
        count = Restaurant.objects.all().count()
        self.assertEqual(count,2)
        response = self.client.post('/resturant/delete/1', follow=True)
        # Make sure after delete there are still 2 resturants
        count = Restaurant.objects.all().count()
        self.assertEqual(count,2)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/')
        
class TestResturantRecommendation(TestCase):
    def setUp(self):
        resturant1 = Restaurant.objects.create(Name='Pizza Palace', Style='Italian', Price=100,
                                         Img='None',Distance=1.5, Address='清水河畔', Rating=4.5)
        resturant2 = Restaurant.objects.create(Name='Bobs BBQ', Style='BBQ', Price=65, 
                                         Img='None',Distance=3, Address='農安街', Rating=1.5)
        resturant3 = Restaurant.objects.create(Name="Kevins BBQ", Style='BBQ', Price=500,
                                            Img='None',Distance=6, Address='行天宮', Rating=4.5)
        forms.RestaurantCreate(resturant1)
        forms.RestaurantCreate(resturant2)
        forms.RestaurantCreate(resturant3)
        
    def test_random_resturant_recommendation(self):
        response = self.client.post('/random/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Restaurant/listRestaurant_random.html')
        self.assertContains(response, response.context['Restaurant_selected'].Name)
        print(f"{response.context['Restaurant_selected'].Name} is the recommended resturant")


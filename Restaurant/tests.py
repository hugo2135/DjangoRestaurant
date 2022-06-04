from django.test import TestCase
from django.urls import resolve
from Restaurant.models import Restaurant
from . import views,forms
from selenium import webdriver

# Create your tests her
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
        
class TestWebPagesView(TestCase):
    def setUp(self):
        resturant1 = Restaurant.objects.create(Name='Pizza Palace', Style='Italian', Price=100,
                                         Img='None',Distance=1.5, Address='清水河畔', Rating=4.5)
        resturant2 = Restaurant.objects.create(Name='Bobs BBQ', Style='BBQ', Price=65, 
                                         Img='None',Distance=3, Address='農安街', Rating=1.5)
        forms.RestaurantCreate(resturant1)
        forms.RestaurantCreate(resturant2)
        
    def test_resolve_to_home_page(self):
        resolver = resolve('/restaurants/')                                   #我有改基底url，這邊就一起動了
        self.assertEqual(resolver.view_name, 'index')
        
    def test_get_home_page(self):
        response = self.client.get('/restaurants/')
        self.assertTemplateUsed(response, 'Restaurant/listRestaurant.html')
        
    def test_get_add_restaurant(self):
        response = self.client.get('/restaurants/add/')
        self.assertTemplateUsed(response, 'Restaurant/editRestaurant.html')
        
    def test_get_edit_restaurant(self):
        response_1 = self.client.get('/restaurants/edit/1')
        self.assertTemplateUsed(response_1, 'Restaurant/editRestaurant.html')
        response_2 = self.client.get('/restaurants/edit/2')
        self.assertTemplateUsed(response_2, 'Restaurant/editRestaurant.html')
        
    def test_get_delete_restaurant(self):
        resolver_1 = resolve('/restaurants/delete/1')
        self.assertEqual(resolver_1.view_name, 'Restaurant.views.deleteRestaurant')
        resolver_2 = resolve('/restaurants/delete/2')
        self.assertEqual(resolver_2.view_name, 'Restaurant.views.deleteRestaurant')
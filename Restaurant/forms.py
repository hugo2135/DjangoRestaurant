from dataclasses import field
from django import forms
from .models import Restaurant

class RestaurantCreate(forms.ModelForm):
    
    class Meta:
        model = Restaurant
        field = '__all__'
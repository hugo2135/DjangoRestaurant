from django import forms
from .models import Restaurant

class RestaurantCreate(forms.ModelForm):
    
    class Meta:
        model = Restaurant
        fields = '__all__'
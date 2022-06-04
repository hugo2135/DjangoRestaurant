from django.urls import path
from . import views
from RestaurantRecommendSystem.settings import DEBUG, STATIC_ROOT, STATIC_URL, MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.addRestaurant, name='add-restaurant'),
    path('edit/<int:restaturant_id>', views.editRestaurant),
    path('delete/<int:restaturant_id>', views.deleteRestaurant)
]

if DEBUG :
    urlpatterns += static(STATIC_URL, document_root = STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)
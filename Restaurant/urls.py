from django.urls import path, include
from . import views
from RestaurantRecommendSystem.settings import DEBUG, STATIC_ROOT, STATIC_URL, MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('random/', views.random_recommend_restaurant, name='random'),
    path('add/', views.addRestaurant, name='add-restaurant'),
    path('resturant/edit/<int:restaturant_id>', views.editRestaurant),
    path('resturant/delete/<int:restaturant_id>', views.deleteRestaurant),
    path('resturant/<int:restaturant_id>', views.viewResturantInfo),
    path('resturant/rating/<int:restaturant_id>', views.ratingRestaurant),
    path('preference/', views.filter_recommend_restaurant, name='preference'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
]

if DEBUG :
    urlpatterns += static(STATIC_URL, document_root = STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)
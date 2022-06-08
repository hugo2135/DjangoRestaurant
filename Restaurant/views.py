from glob import glob
from pickle import FALSE
from django.shortcuts import render, redirect
from .models import Restaurant
from .forms import RestaurantCreate
from django.http import HttpResponse
import random as rd

# Create your views here.

random_msg_trigger = True
authenticated_msg_trigger = False

authenticated_msg = None
randomrestaurant_info = None

# def random_get_restaurant(request):
#     RestaurantList = Restaurant.objects.all()
#     num = RestaurantList.last().id    #latest id of Restaurant
#     sign = True
#     Id = rd.randint(1, num)
#     random_restaurant = None
#     while(Id <= num and sign):
#         try:
#             random_restaurant = RestaurantList.get(id = Id)
#             sign = False
#         except:
#             sign = True
#             print(f'ID:{Id} restaurant not found.')
#             Id = rd.randint(1, num)
            
#     print(f'ID = {Id}')
#     temp_list = list_of_render
#     temp_list['RandomRestaurant'] = random_restaurant.Name
#     return render(request, 'Restaurant/listRestaurant.html', temp_list)

def random_get_restaurant(request):
    RestaurantList = Restaurant.objects.all()
    global random_msg_trigger
    random_msg_trigger = True
    num = RestaurantList.last().id    #latest id of Restaurant
    sign = True
    Id = rd.randint(1, num)
    random_restaurant = None
    while(Id <= num and sign):
        try:
            random_restaurant = RestaurantList.get(id = Id)
            sign = False
        except:
            sign = True
            print(f'ID:{Id} restaurant not found.')
            Id = rd.randint(1, num)
            
    global randomrestaurant_info
    randomrestaurant_info = random_restaurant
    return redirect('index')



def index(request):
    list_of_render = {
        'RestaurantList' : None,
        'Authenticated_msg' : None,
        'RandomRestaurant' : None
    }
    RestaurantList = Restaurant.objects.all()
    list_of_render['RestaurantList'] = RestaurantList
    global random_msg_trigger
    global authenticated_msg_trigger
    if random_msg_trigger == True:
        random_msg_trigger = False
        if randomrestaurant_info != None:
            list_of_render['RandomRestaurant'] = randomrestaurant_info.Name
    if authenticated_msg_trigger:
        authenticated_msg_trigger = False
        list_of_render['Authenticated_msg'] = authenticated_msg
    return render(request, 'Restaurant/listRestaurant.html', list_of_render)

def addRestaurant(request):
    if not request.user.is_authenticated:
        global authenticated_msg_trigger
        global authenticated_msg
        authenticated_msg_trigger = True
        authenticated_msg = '欲操作餐廳資料，請先登入'
        return redirect('index')
    addRestaurant = RestaurantCreate()
    if request.method == 'POST':
        addRestaurant = RestaurantCreate(request.POST, request.FILES)
        if addRestaurant.is_valid():
            addRestaurant.save()
            return redirect('index')
        else:
            HttpResponse(""" Input Wrong. Please reload this website by click <a href="{{url:'index'}}">Reload</a>""")
    else:
        return render(request, 'Restaurant/editRestaurant.html', {'Restaurant_form':addRestaurant})

def editRestaurant(request, restaturant_id):
    if not request.user.is_authenticated:
        global authenticated_msg_trigger
        global authenticated_msg
        authenticated_msg_trigger = True
        authenticated_msg = '欲操作餐廳資料，請先登入'
        return redirect('index')
    restaturant_id = int(restaturant_id)
    try:
        restaturant_selected = Restaurant.objects.get(id = restaturant_id)
    except Restaurant.DoesNotExist:
        return redirect('index')
    restaturant_form = RestaurantCreate(request.POST or None, instance=restaturant_selected)
    if restaturant_form.is_valid():
        restaturant_form.save()
        return redirect('index')
    return render(request, 'Restaurant/editRestaurant.html', {'Restaurant_form':restaturant_form})

def deleteRestaurant(request, restaturant_id):
    if not request.user.is_authenticated:
        global authenticated_msg_trigger
        global authenticated_msg
        authenticated_msg_trigger = True
        authenticated_msg = '欲操作餐廳資料，請先登入'
        return redirect('index')
    try:
        restaturant_selected = Restaurant.objects.get(id = restaturant_id)
    except:
        return redirect('index')
    restaturant_selected.delete()
    return redirect('index')
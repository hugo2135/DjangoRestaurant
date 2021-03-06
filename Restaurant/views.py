from glob import glob
from pickle import FALSE
from unicodedata import decimal
from django.shortcuts import render, redirect
from .models import Restaurant
from .forms import RestaurantCreate
from django.http import HttpResponse
import random as rd
from django.contrib import messages
random_msg_trigger = True
authenticated_msg_trigger = False

authenticated_msg = None
randomrestaurant_info = None

def random_recommend_restaurant(request):
    RestaurantList = list(Restaurant.objects.all())
    try:
        random_restaurant = rd.choice(RestaurantList)
    except:
        messages.error(request, '沒有餐廳資料')
        return redirect('index')     
    return render(request, 'Restaurant/listRestaurant_random.html', {'Restaurant_selected':random_restaurant,'RandomRestaurant':True})
    
def filter_recommend_restaurant(request):
    filter_distance = None
    filter_price = None
    filter_rating = None
    if request.method == 'POST' and (request.POST["filter_name"]!="" or request.POST["filter_style"]!="" or request.POST["filter_price"]!="" or request.POST["filter_distance"]!="" or request.POST["filter_rating"]!=""):
        filter_name = request.POST["filter_name"]
        filtered_restaurants = Restaurant.objects.all().filter(Name__contains=filter_name)
        filter_style = request.POST["filter_style"]
        filtered_restaurants = filtered_restaurants.filter(Style__contains=filter_style)
        if request.POST["filter_distance"] != "":
            try:
                filter_distance = float(request.POST["filter_distance"])
            except:
                messages.error(request, '距離請輸入數字')
                return redirect('index')
            filtered_restaurants = filtered_restaurants.filter(Distance__lte=filter_distance)
        if request.POST["filter_price"] != "":
            try:
                filter_price = float(request.POST["filter_price"])
            except:
                messages.error(request, '價格請輸入數字')
                return redirect('index')
            filtered_restaurants = filtered_restaurants.filter(Price__lte=filter_price)
        if request.POST["filter_rating"] != "":
            try:
                filter_rating = float(request.POST["filter_rating"])
            except:
                messages.error(request, '評分請輸入數字')
                return redirect('index')
            filtered_restaurants = filtered_restaurants.filter(Rating__gte=filter_rating)
        filtered_restaurants = filtered_restaurants.order_by('-Rating__average')
        print(filter_name,filter_style,filter_distance,filter_price,filter_rating)
        messages.success(request, '搜尋成功')
        return render(request, 'Restaurant/preference.html', {'Restaurant_preferenced':filtered_restaurants,'Filter_name':filter_name,'Filter_style':filter_style,'Filter_distance':filter_distance,'Filter_price':filter_price,'Filter_rating':filter_rating})
    else:
        messages.error(request, '請先輸入餐廳偏好')
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
    if not request.user.is_staff:
        messages.error(request, '欲新增餐廳，請先登入')
        return redirect('index')
    addRestaurant = RestaurantCreate()
    if request.method == 'POST':
        addRestaurant = RestaurantCreate(request.POST, request.FILES)
        if addRestaurant.is_valid():
            addRestaurant.save()
            messages.success(request, '餐廳新增成功')
            return redirect('index')
        else:
            HttpResponse(""" Input Wrong. Please reload this website by click <a href="{{url:'index'}}">Reload</a>""")
    else:
        return render(request, 'Restaurant/editRestaurant.html', {'Restaurant_form':addRestaurant})
    
def viewResturantInfo(request, restaturant_id):
    restaturant_id = int(restaturant_id)
    try:
        resturant_selected = Restaurant.objects.get(id = restaturant_id)
    except Restaurant.DoesNotExist:
        messages.error(request, '餐廳不存在')
        return redirect('index')
    
    print(request.GET.get('rate'))
    return render(request, 'Restaurant/ResturantInfo.html', {'Restaurant_selected':resturant_selected})

def editRestaurant(request, restaturant_id):
    if not request.user.is_staff:
        messages.error(request, '欲編輯餐廳，請先登入管理員')
        return redirect('index')
    restaturant_id = int(restaturant_id)
    try:
        restaturant_selected = Restaurant.objects.get(id = restaturant_id)
    except Restaurant.DoesNotExist:
        messages.error(request, '餐廳不存在')
        return redirect('index')
    restaturant_form = RestaurantCreate(request.POST or None, instance=restaturant_selected)
    
    if restaturant_form.is_valid():
        restaturant_form.save()
        messages.success(request, f'餐廳編輯成功 ({restaturant_selected.Name})')
        return redirect('index')
    
    return render(request, 'Restaurant/editRestaurant.html', {'Restaurant_form':restaturant_form})

def deleteRestaurant(request, restaturant_id):
    if not request.user.is_staff:
        messages.error(request, '欲刪除餐廳，請先登入管理員')
        return redirect('index')
    try:
        restaturant_selected = Restaurant.objects.get(id = restaturant_id)
    except:
        messages.error(request, '餐廳不存在')
        return redirect('index')
    restaturant_selected.delete()
    
    messages.success(request, f'餐廳刪除成功 ({restaturant_selected.Name})')
    return redirect('index')

def ratingRestaurant(request, restaturant_id):
    if not request.user.is_authenticated:
        messages.error(request, '欲評價餐廳，請先登入')
    return redirect('/resturant/'+str(restaturant_id))
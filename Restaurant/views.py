from glob import glob
from pickle import FALSE
from django.shortcuts import render, redirect
from .models import Restaurant
from .forms import RestaurantCreate
from django.http import HttpResponse
import random as rd
from django.contrib import messages

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
    RestaurantList = list(Restaurant.objects.all())
    try:
        random_restaurant = rd.choice(RestaurantList)
    except:
        messages.error(request, '沒有餐廳資料')
        return redirect('index')
    messages.success(request, f'隨機餐廳為 {random_restaurant.Name}, 好好體驗沒吃過的餐廳!')
    return redirect(f'/resturant/{random_restaurant.id}')       
    # return render(request, 'Restaurant/ResturantInfo.html', {'Restaurant_selected':random_restaurant},{'isRandomRecommend':True})



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
        #list_of_render['Authenticated_msg'] = '欲操作餐廳資料，請先登入'
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
    return render(request, 'Restaurant/ResturantInfo.html', {'Restaurant_selected':resturant_selected})

def editRestaurant(request, restaturant_id):
    if not request.user.is_authenticated:
        global authenticated_msg_trigger
        global authenticated_msg
        authenticated_msg_trigger = True
        authenticated_msg = '欲操作餐廳資料，請先登入'
        #list_of_render['Authenticated_msg'] = '欲操作餐廳資料，請先登入'
        messages.error(request, '欲編輯餐廳，請先登入')
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
    if not request.user.is_authenticated:
        global authenticated_msg_trigger
        global authenticated_msg
        authenticated_msg_trigger = True
        authenticated_msg = '欲操作餐廳資料，請先登入'
        #list_of_render['Authenticated_msg'] = '欲操作餐廳資料，請先登入'
        messages.error(request, '欲刪除餐廳，請先登入')
        return redirect('index')
    try:
        restaturant_selected = Restaurant.objects.get(id = restaturant_id)
    except:
        messages.error(request, '餐廳不存在')
        return redirect('index')
    restaturant_selected.delete()
    
    messages.success(request, f'餐廳刪除成功 ({restaturant_selected.Name})')
    return redirect('index')
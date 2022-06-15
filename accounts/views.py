from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
list_of_render = {
    'account_list':None,
    'Authenticated_msg':None    
}
# Create your views here.
def accounts_index(request):
    AccountList = User.objects.all()
    list_of_render['account_list'] = AccountList
    return render(request, 'registration/listAccount.html',list_of_render)

def register(request):
    context = {
        'form':None,
        'error':None
    }
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password1']
        if form.is_valid():
            messages.success(request, '註冊成功')
            form.save()
            return redirect('accounts-index')
        else:
            messages.error(request, '註冊失敗')
            context['error'] = form.errors
    else:
        form = UserCreationForm()    
    context['form'] = form
    return render(request, 'registration/register.html', context)

def editAccount(request,account_id):
    if not request.user.is_authenticated:
        messages.error(request, '欲編輯帳戶，請先登入')
        return redirect('accounts-index')
    account_id = int(account_id)
    try:
        account_selected = User.objects.get(id = account_id)
    except User.DoesNotExist:
        messages.error(request, '帳戶不存在')
        return redirect('register')
    account_form = UserCreationForm(request.POST or None, instance=account_selected)
    if account_form.is_valid():
        account_form.save()
        messages.success(request, '編輯成功') 
        return redirect('accounts-index')                                                  
    return render(request, 'registration/editAccount.html', {'account_form':account_form})

def deleteAccount(request,account_id):
    if not request.user.is_authenticated:
        messages.error(request, '欲刪除帳戶，請先登入')
        return redirect('accounts-index')
    account_id = int(account_id)
    try:
        account_selected = User.objects.get(id = account_id)
    except User.DoesNotExist:
        messages.error(request, '帳戶不存在')
        return redirect('register')
    account_selected.delete()
    messages.success(request, '刪除成功')
    return redirect('accounts-index')
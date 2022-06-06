from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    context = {
        'form':None,
        'error':None
    }
    if request.method == 'POST':
        print('POST')
        form = UserCreationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password1']
        if form.is_valid():
            print('fuck')
            form.save()
        else:
            context['error'] = form.errors
    else:
        print('else')
        form = UserCreationForm()

    context['form'] = form
    
    return render(request, 'registration/register.html', context)

def editAccount(request,account_id):
    account_id = int(account_id)
    try:
        account_selected = User.objects.get(id = account_id)
    except User.DoesNotExist:
        return redirect('register')
    account_form = UserCreationForm(request.POST or None, instance=account_selected)
    if account_form.is_valid():
        account_form.save()
        return redirect('register')
                                                        #account_form is a var used in the html
    return render(request, 'registration/editAccount.html', {'account_form':account_form})
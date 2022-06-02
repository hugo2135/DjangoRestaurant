from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

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
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView 
from django.views.decorators.csrf import csrf_exempt

from auth_user.models import User 
from auth_user.forms import RegisterForm


import pdb 
@csrf_exempt
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_conf = request.POST.get('password_confirmation')
        if password == password_conf:
            user = User.objects.create(
                name=name,
                email=email,
                password=password
            )
            return HttpResponseRedirect(f"/user_profiile/{user.pk}/")
    return render(request, 'auth_user/register_form.html')


def detail_view(request, pk):
    user = User.objects.get(pk=pk)
    if not user.is_active:
        raise User.DoesNotExist('User matching query does not exist')

    context = {
        'user': user
    }
    
    return render(request, 'auth_user/user_detail.html', context=context)
    

def update_profile(request):
    pass


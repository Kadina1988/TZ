from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView 
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

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
            request.session['user_id'] = user.pk 
            return HttpResponseRedirect("/user_detail/")
    
    return render(request, 'auth_user/register_form.html')


def user_detail(request):
    try:
        user = User.objects.get(pk=request.session['user_id'])
        if not user.is_active:
            raise ObjectDoesNotExist

        context = {
            'user': user
        }
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/login/')
    
    return render(request, 'auth_user/user_detail.html', context=context)
    
@csrf_exempt
def user_update(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.session['user_id'])
        name = request.POST.get('name')
        email = request.POST.get('email')
        user.name = name 
        user.email = email 
        user.save()
        return HttpResponseRedirect("/user_detail/")
    return render(request, 'auth_user/user_update_form.html')
    
    
def delete_user(request):
    user = User.objects.get(pk=request.session['user_id'])
    user.is_active = False 
    user.save()
    logout(request)
    return HttpResponseRedirect('/register/')   


@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email, is_active=True)
        except:
            return render(request, 'auth_user/login_form.html', {'message': 'Несуществующий пользователь'})
        
        if user.password == password:
            request.session['user_id'] = user.pk 
            return HttpResponseRedirect('/user_detail/')
        else:
            return render(request, 'auth_user/login_form.html', {'message': 'Неверный пароль'})
    
    return render(request, 'auth_user/login_form.html')


def logout(request):
    request.session['user_id'] = None 
    return HttpResponseRedirect('/login/')

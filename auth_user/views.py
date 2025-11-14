from django.http import HttpResponseRedirect
from django.shortcuts import render

from auth_user.models import User 
from auth_user.forms import RegisterForm


import pdb 
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['password_confirmation']:
            user = User.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'] 
            )
            return HttpResponseRedirect('/profile')

    context = {
        'form': RegisterForm(),
    }
    return render(request, 'auth_user/register.html', context=context)



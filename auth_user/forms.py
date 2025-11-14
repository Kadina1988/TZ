from django import forms 

from auth_user.models import User 

from django.contrib.auth.forms import UserCreationForm

class RegisterForm(forms.Form):
    name = forms.CharField(label='Your name')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='password')
    password_confirmation = forms.CharField(label='password_confirmation')

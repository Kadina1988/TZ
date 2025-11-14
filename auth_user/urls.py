from django.urls import path 
from auth_user import views

urlpatterns = [
    path('register/', views.register, name='register')
]

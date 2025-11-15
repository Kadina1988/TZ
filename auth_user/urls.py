from django.urls import path 
from auth_user import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_detail/', views.user_detail, name='user_detail'),
    path('user_update/', views.user_update, name='update'),
    path('user_delete/', views.delete_user, name='delete'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
]

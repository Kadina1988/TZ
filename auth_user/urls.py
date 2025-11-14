from django.urls import path 
from auth_user import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_profile/<int:pk>/', views.detail_view, name='user_profiile'),
    # path('user_update/<int:pk>/', views.ProfileUpdateView.as_view()) 
]

from django.urls import path 
from auth_user import views

urlpatterns = [
    path('register/', views.register),
    path('user_detail/<int:pk>/', views.user_detail),
    path('user_update/', views.user_update),
    path('user_delete/', views.delete_user),
    path('login/', views.login),
    path('logout/', views.logout),
    path('roles/', views.roles_list),
    path('books/', views.books_list),
    path('users/', views.users_list),
    path('change_role/<int:pk>/', views.change_role),
    path('book_detail/<int:pk>/', views.book_detail),
    path('book_change/<int:pk>/', views.book_change),
]

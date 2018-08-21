from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings

app_name='recognition'

urlpatterns = [
 	path('', views.Home, name='home'),
 	path('settings/', views.Home, name='settings'),

 	path('login/', views.UserLoginView.as_view(), name='login'),
 	path('register/', views.UserRegistrationView.as_view(), name='register'),
 	path('reg-face/', views.UserFaceRegView.as_view(), name='reg-face'),
 	path('apis/auth/', views.Auth.as_view(), name='api-auth')
]


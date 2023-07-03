from django.urls import include, path
from . import views

urlpatterns = [
    path('login', views.loginUser, name='login'),
    path('register', views.registerUser, name='register'),
    path('logout', views.logoutUser, name='logout'),
]
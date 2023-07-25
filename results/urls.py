from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.getResults, name='getResults'),
    path('', views.saveResult, name='saveResult')
]
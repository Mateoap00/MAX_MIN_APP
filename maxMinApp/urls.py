"""
URL configuration for maxMinApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render, redirect

def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            print("Logged in")
            return render(request, 'maxMinApp/index.html', {})
        else:
            print("Not logged in")
            return redirect('login')
    if request.method == 'POST':
        restrictions = request.POST.get('restrictions')
        variables = request.POST.get('variables')
        operation = request.POST.get('operation')
        var = range(0, int(variables))
        context = {
            'operation': operation,
            'restrictions': {
                'value': int(restrictions),
                'range': range(1, int(restrictions)+1)
            },
            'variables': {
                'value': int(variables),
                'range': range(1, int(variables)+1)
            }
        }
        return render(request, 'maxMinApp/model.html', context)
    

urlpatterns = [
    path('', home, name='index'),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
]

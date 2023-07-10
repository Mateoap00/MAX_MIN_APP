from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser

def loginUser(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('Login succeed!')
            # login(request, user)
            return redirect('model')
        else:
            print('Login failed with wrong credentials!')
            return redirect('login')
    else:
        return render(request, 'users/login.html', {})
    
def registerUser(request):
    if request.method == 'POST':
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password1"]
        user = CustomUser.objects.create_user(email=email, username=username, password=password)
        if user is not None:
            print('Registration succeed!')
            return redirect('login')
        else:
            print('Registration failed!')
            return redirect('register')
    else:
        return render(request, 'users/register.html', {})
    
def logoutUser(request):
    if request.method == 'GET':
        logout(request)
        print('Logout succeed!')
        return redirect('index')
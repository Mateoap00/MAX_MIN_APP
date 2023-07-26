from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from .models import CustomUser

def loginUser(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            msg = f"Hola {user.username}! Inicio de sesión exitoso."
            messages.success(request, msg)
            print('Login succeed!')
            return redirect('model')
        else:
            messages.error(request, 'Error: Nombre de usuario o contraseña incorrectas.')
            return redirect('login')
    else:
        return render(request, 'users/login.html', {})
    
def registerUser(request):
    if request.method == 'POST':
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password1"]
        password2 = request.POST["password2"]
        if password == password2:
            try:
                user = CustomUser.objects.create_user(email=email, username=username, password=password)
                if user is not None:
                    msg = f"Nuevo usuario {user.username} registrado con éxito."
                    messages.success(request, msg)
                    return redirect('login')
                else:
                    messages.error(request, 'Error: No se pudo registrar el nuevo usuario.')
                    return redirect('register')
            except IntegrityError:
                msg = f"Error: Usuario con el nombre '{username}' y email '{email}' ya se encuentra registrado."
                messages.error(request, msg)
                return redirect('register')            
        else:
            messages.error(request, 'Error: Las contraseñas ingresadas no son iguales.')
            return redirect('register')
    else:
        return render(request, 'users/register.html', {})
    
def logoutUser(request):
    if request.method == 'GET':
        logout(request)
        print('Logout succeed!')
        return redirect('index')
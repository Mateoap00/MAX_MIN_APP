from django.shortcuts import render, redirect

def index(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('model')
        else:
            return redirect('login')

def custom404NotFound(request):
    context = {
        'info': 'Pagina'
    }
    return render(request, 'maxMinApp/notfound.html', context)
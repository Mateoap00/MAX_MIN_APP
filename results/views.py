from django.shortcuts import render, redirect
from django.db import OperationalError
from django.contrib import messages
from .models import Result
import json

def getResults(request):
    if request.method == 'GET':        
        user = request.user
        try:            
            results = user.result_set.all()
            allResults = []
            if len(results) > 0:
                for res in results:
                    objFunction = res.objFunction
                    operation = res.operation            
                    constraints = res.constraints.replace("'", "\"")
                    solution = res.solution.replace("'", "\"")
                    resultDate = res.resultDate
                    result = {
                        'objFunction': objFunction,
                        'operation': operation,
                        'constraints': json.loads(constraints).copy(),
                        'solution': json.loads(solution).copy(),
                        'resultDate': resultDate
                    }
                    allResults.append(result)     
                context = {
                    'allResults': allResults.copy()        
                }
                messages.success(request, 'Resultados cargados con éxito.')
                return render(request, 'results/results.html', context)
            else:
                msg = f"Error: El usuario {user.username} no ha registrado resultados."
                messages.error(request, msg)
                context = {
                    'info': 'Resultados'
                }
                return render(request, 'maxMinApp/notfound.html', context)
        except OperationalError:
            messages.error(request, 'Error: No se pudo acceder a los resultados registrados.')
            context = {
                'info': 'Resultados'
            }
            return render(request, 'maxMinApp/notfound.html', context)
        

def saveResult(request):
    if request.method == 'POST':
        user = request.user
        objFunction = request.POST.get('objFunction')
        operation = request.POST.get('operation') 
        constraints = request.POST.get('constraints')
        solution = request.POST.get('solution')
        try:
            newResult = Result.objects.create(
                user = user, 
                objFunction = objFunction,
                operation = operation, 
                constraints = constraints, 
                solution = solution
            )
            if newResult is not None:
                newResult.save()
                messages.success(request, 'Resultados guardados con éxito.')
                context = {
                    'showMain': True,
                    'showMainMessage': True
                }
                return render(request, 'model/model.html', context)
            else:
                messages.error(request, 'Error: Guardado de resultados fallido.')
                context = {
                    'showMain': True,
                    'showMainMessage': True
                }
                return render(request, 'model/model.html', context)
        except OperationalError:
            messages.error(request, 'Error: Guardado de resultados fallido.')
            context = {
                'showMain': True,
                'showMainMessage': True
            }
            return render(request, 'model/model.html', context) 

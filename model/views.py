from django.shortcuts import render
from utils.simplex import Simplex

def model(request):
    if request.method == 'GET':
        getType = request.GET.get('getType')
        print('getType: ', getType)
        if getType == 'model':
            restrictions = request.GET.get('restrictions')
            variables = request.GET.get('variables')
            operation = request.GET.get('operation')
            context = {
                'showModel': True,
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
            return render(request, 'model/model.html', context)
        elif getType == 'results':
            totalVariables = request.GET.get('variables') 
            totalConstraints = request.GET.get('restrictions')
            operation = request.GET.get('operation')

            objFunCoeffs = []
            allConstraints = []

            for i in range(1, int(totalVariables)+1):
                coeffName = f"funCoeff{i}"
                coefficient = request.GET.get(coeffName)
                objFunCoeffs.append(coefficient)

            for i in range(1, int(totalConstraints)+1):
                constraint = []
                constSelectEqName = f"constSelectEq{i}"
                constSelectEq = request.GET.get(constSelectEqName)
                constEqToName = f"constEqTo{i}"
                constEqTo = request.GET.get(constEqToName)
                for j in range(1, int(totalVariables)+1):
                    constCoeffName = f"constCoeff({i},{j})"
                    constCoeff = request.GET.get(constCoeffName)
                    constraint.append(constCoeff)
                constraint.append(constSelectEq)
                constraint.append(constEqTo)
                allConstraints.append(constraint.copy())

            run = Simplex(
                operation, 
                totalVariables, 
                totalConstraints, 
                objFunCoeffs, 
                allConstraints    
            )

            print('Model: ', run.modelString)
            print('Optimal Solution: ', run.solution)

            context = {
                'operation': run.operation,
                'model': run.modelString,
                'allTables': run.allTables,
                'firstTable': run.firstTable,
                'lastTable': run.lastTable,
                'solution': run.solution,
                'showResults': True,
                'showModel': True
            }
            return render(request, 'model/model.html', context)
        else:
            return render(request, 'model/model.html', {})
        
    if request.method == 'POST':
        restrictions = request.POST.get('restrictions')
        variables = request.POST.get('variables')
        operation = request.POST.get('operation')
        context = {
            'showModel': True,
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
        return render(request, 'model/model.html', context)

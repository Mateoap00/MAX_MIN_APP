from django.shortcuts import render

from utils.simplex import Simplex

def solve(request):
    if request.method == 'GET':
        totalVariables = request.GET.get('variables') 
        totalConstraints = request.GET.get('restrictions')
        operation = request.GET.get('operation')

        objFunCoeffs = []
        allConstraints = []

        for i in range(1, int(totalVariables)+1):
            coeffName = f"funCoeff{i}"
            coefficient = request.GET.get(coeffName)
            objFunCoeffs.append(coefficient)     
        
        print(objFunCoeffs)

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
        
        print(allConstraints)

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
            'solution': run.solution
        }

        return render(request, 'solve/solve.html', context)
    
    if request.method == 'POST':
        pass
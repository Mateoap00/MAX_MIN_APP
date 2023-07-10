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

        print()
        i = 0
        for table in run.allTables:
            i = i+1
            print('########## Table #', i, ' ##########')
            for prop in table:
                if prop == 'table':
                    print('table: ')
                    for row in table[prop]:
                        print(row)
                else:
                    print(prop, ': ', table[prop])
                    print()
            print()

        print("Optimal Solution:")
        print(run.solution)

        context = {
            'simplex': run
        }

        return render(request, 'solve/solve.html', context)
    
    if request.method == 'POST':
        pass
import numpy as np
from fractions import Fraction

############################# WORKS FOR >= CONSTRAINTS ##########################

class Simplex:
    operation = '' 
    nRes = 0
    nVar = 0
    objFun = []
    constraints = []
    firstTable = {}
    lastTable = {}
    allTables = []
    solution = {}

    # operation para definir que se va a resolver, ejercicio de maximizacion 'max' o minimizacion 'min'.
    # nRes, nVar son el numero de restricciones y variables del problema.
    # objFun es un arreglo del tipo ['x1', 'x2', 'x3', ...] con los coeficientes de cada variable en la función objetivo.
    # constraints es una matriz del tipo [['x1', 'x2', 'x3', ..., ('<=' o '>='), 'R'], ['x1', 'x2', 'x3', ..., ('<=' o '>='), 'R'], ...] 
    #   con los coeficientes de cada variable de la restricción, el signo de la desigualdad, y el coeficiente del 
    #   lado derecho de la desigualdad.
    def __init__(self, operation, nVar, nRes, objFun, constraints):
        self.operation = operation        
        self.nVar = nVar
        self.nRes = nRes
        self.model(objFun, constraints)
        self.solve()

    def model(self, objFun, constraints):
        objAux = []
        self.constraints = []
        for i in range(len(objFun)):
            objAux.append(-1 * int(objFun[i]))
        objAux.append(0)
        
        self.objFun = np.array(objAux)
        
        for constraint in constraints:
            newConstraint = []
            for i in range(len(constraint)):
                if constraint[i] != constraint[-2]:
                    newConstraint.append(int(constraint[i]))
                else:
                    newConstraint.append(str(constraint[i]))
            self.constraints.append(np.array(newConstraint))

    def solve(self):
        try:
            # Solve the problem
            final_table = self.simplex_method(self.objFun, self.constraints)
        except ZeroDivisionError:
            print("Error: Division by zero occurred.")

    def format_fraction(self, value):
        if value == 0:
            return '0'
        elif value.denominator == 1:
            return str(value.numerator)
        else:
            return f"{value.numerator}/{value.denominator}"
    
    def format_solution(self, lastTableSolution):
        solution = {}
        varNames = []
        values = []
        varNames.append('Z')

        for i in range(0, int(self.nVar)):
            name = f"X{i+1}"
            varNames.append(name)

        for name in varNames:
            if name in lastTableSolution:
                values.append(lastTableSolution[name])
            else:
                values.append(0)
        
        solution = {
                    k: v for k, v in zip(
                        varNames.copy(), 
                        values.copy()
                    )
                }
        return solution

    def simplex_method(self, z_row, constraints):
        num_variables = len(z_row) - 1
        num_constraints = len(constraints)

        column_names = ['X' + str(i) for i in range(1, num_variables + 1)]
        column_names += ['S' + str(i) for i in range(1, num_constraints + 1)]
        column_names.append('R')

        row_names = []
        row_names.append('Z')
        row_names += ['S' + str(i) for i in range(1, num_constraints + 1)]

        # Create the initial simplex table
        simplex_table = np.zeros((num_constraints + 1, num_variables + num_constraints + 1), dtype=object)
        simplex_table[0][:num_variables] = [Fraction(x) for x in z_row[:-1]]
        simplex_table[0][-1] = Fraction(z_row[-1])

        for constraint in constraints:
            if constraint[-2] == '>=':
                constraint[-2] = '<='
                for i in range(len(constraint)):
                    if str(constraint[i]) != '<=':
                        constraint[i] = str(-1 * int(constraint[i]))

        for i, constraint in enumerate(constraints, start=1):
            simplex_table[i][:num_variables] = [Fraction(x) for x in constraint[:-2]]
            if constraint[-2] == '<=':
                simplex_table[i][num_variables+i-1] = 1  # Add slack variables
            elif constraint[-2] == '>=':
                simplex_table[i][num_variables+i-1] = -1  # Add surplus variables
            simplex_table[i][-1] = Fraction(constraint[-1])  # Right-hand side value

        # Display the initial table
        firstTable = {
            'colsNames': column_names.copy(),
            'rowsNames': row_names.copy(),
            'table': []
        }
        for row in simplex_table:
            auxRow = [self.format_fraction(x) for x in row]
            firstTable['table'].append(auxRow.copy())

        self.allTables.append(firstTable.copy())
        self.firstTable = firstTable.copy()

        tableNum = 0
        done = False
        # Iterate until no negative values in the Z row
        while done == False:
            tableNum = tableNum + 1
            toSaveTable = {}

            pivot_column = np.argmin(simplex_table[0][:-1])

            pivot_row = -1
            min_ratio = float('inf')
            for i in range(1, num_constraints + 1):
                if simplex_table[i][pivot_column] > 0:
                    ratio = simplex_table[i][-1] / simplex_table[i][pivot_column]
                    if ratio < min_ratio:
                        min_ratio = ratio
                        pivot_row = i

            pivot_value = simplex_table[pivot_row][pivot_column]

            entire_pivot_col = [self.format_fraction(x) for x in simplex_table[:, pivot_column]]
            entire_pivot_row = [self.format_fraction(x) for x in simplex_table[pivot_row]]

            toSaveTable = {
                'colsNames': column_names.copy(),
                'rowsNames': row_names.copy(),
                'table': [],
                'pivotCol': {
                    'colName': column_names[pivot_column],
                    'colNum': pivot_column.copy(),
                    'entireCol': entire_pivot_col.copy(),
                    'value': entire_pivot_col[0]
                    },
                'pivotRow': {
                    'rowName': row_names[pivot_row],
                    'rowNum': pivot_row,
                    'entireRow': entire_pivot_row.copy(),
                    'value': entire_pivot_row[pivot_column]
                },
                'pivotNum': pivot_value,
                'enteringRow': {
                    'rowName': column_names[pivot_column],
                    'entireRow': []
                }
            }

            for row in simplex_table:
                auxRow = [self.format_fraction(x) for x in row]
                toSaveTable['table'].append(auxRow.copy())

            row_names[pivot_row] = column_names[pivot_column]
            # Perform row operations
            simplex_table[pivot_row] = simplex_table[pivot_row] / pivot_value

            entering_row = [self.format_fraction(x) for x in simplex_table[pivot_row]]

            toSaveTable['enteringRow']['entireRow'] = entering_row.copy()
            self.allTables.append(toSaveTable.copy())

            for i in range(num_constraints + 1):
                if i != pivot_row:
                    factor = simplex_table[i][pivot_column]
                    simplex_table[i] -= factor * simplex_table[pivot_row]

            # Display the next simplex table
            # print("Next Simplex Table:")
            # print(column_names)
            # print(row_names)
            # for row in simplex_table:
            #     auxRow = [self.format_fraction(x) for x in row]
            #     print(auxRow)
            
            if np.any(simplex_table[0][:-1] < 0):
                done = False
            else:
                done = True
                lastTable = {
                    'colNames': column_names.copy(),
                    'rowNames': row_names.copy(),
                    'table': [],
                    'solution': {}
                }

                for row in simplex_table:
                    auxRow = [self.format_fraction(x) for x in row]
                    lastTable['table'].append(auxRow.copy())
                
                solution = {
                    'varNames': row_names.copy(),
                    'values': [self.format_fraction(Fraction(x)) for x in simplex_table[:, -1].copy()]
                }

                solution = {
                    k: v for k, v in zip(
                        row_names.copy(), 
                        [self.format_fraction(Fraction(x)) for x in simplex_table[:, -1].copy()]
                    )
                }

                lastTable['solution'] = solution

                self.allTables.append(lastTable.copy())
                self.lastTable = lastTable.copy()
                self.solution =  self.format_solution(solution.copy())

        return simplex_table


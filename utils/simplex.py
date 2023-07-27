import numpy as np
from fractions import Fraction

class Simplex:
    operation = '' 
    nRes = 0
    nVar = 0
    objFun = []
    constraints = []
    modelString = {}
    firstTable = {}
    lastTable = {}
    allTables = []
    solution = {}
    errors = []
    solved = False

    # operation para definir que se va a resolver, ejercicio de maximización 'max' o minimización 'min'.
    # nRes, nVar son el numero de restricciones y variables del problema.
    # objFun es un arreglo del tipo ['x1', 'x2', 'x3', ...] con los coeficientes de cada variable en la función objetivo.
    # constraints es una matriz del tipo [['x1', 'x2', 'x3', ..., ('<=' o '>='), 'R'], ['x1', 'x2', 'x3', ..., ('<=' o '>='), 'R'], ...] 
    #   con los coeficientes de cada variable de la restricción, el signo de la desigualdad, y el coeficiente del 
    #   lado derecho de la desigualdad.
    def __init__(self, operation, nVar, nRes, objFun, constraints):
        self.operation = operation        
        self.nVar = nVar
        self.nRes = nRes
        self.allTables = []
        self.errors = []
        self.model(objFun, constraints)
        self.solve()

    def model(self, objFun, constraints):
        objAux = []
        modelString = {
            'objFun': '',
            'constraints': []
        }
        self.constraints = []
        for i in range(len(objFun)):
            objAux.append(-1 * int(objFun[i]))
        objAux.append(0)
        
        self.objFun = np.array(objAux)

        objFunString = ''
        for i in range(0, len(objFun)-1):
            objFunString = objFunString + '(' + str(objFun[i]) + ')' + 'X' + str(i+1) + ' + '
        objFunString = objFunString + '(' + str(objFun[len(objFun)-1]) + ')' + 'X' + str(len(objFun))       
        modelString['objFun'] = objFunString

        for constraint in constraints:
            constraintString = ''
            for i in range(0, len(constraint)-3):
                constraintString = constraintString + '(' + str(constraint[i]) + ')' + 'X' + str(i+1) + ' + '
            constraintString = constraintString + '(' + str(constraint[len(constraint)-3]) + ')' + 'X' + str(len(constraint)-2)
            constraintString = constraintString + ' ' + str(constraint[len(constraint)-2]) + ' '
            constraintString = constraintString + str(constraint[len(constraint)-1])       
            modelString['constraints'].append(constraintString)
        
        self.modelString = modelString
        
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
            self.simplex_method(self.objFun, self.constraints)
        except ZeroDivisionError:
            self.solved = False
            self.errors.append('Error: Division para cero, no es posible encontrar la optimización del problema.')

    def format_fraction(self, value):
        try:
            if value == 0:
                return '0'
            elif value.denominator == 1:
                return str(value.numerator)
            else:
                return f"{value.numerator}/{value.denominator}"
        except AttributeError:
            self.solved = False
        
    def format_table(self, type, simplex_table, table_name, colsNames, rowsNames, pivot_col, pivot_row, pivot_value, entering_row, table_values):
        colsNames = colsNames.copy()
        rowsNames = rowsNames.copy()        
        table_values = table_values.copy()
        if type == 'first':
            formatTable = {
                'tableName': table_name,
                'colsNames': colsNames,
                'rowsNames': rowsNames,
                'table': {row: val for row, val in zip(rowsNames, table_values)} 
            }
        elif type == 'last':
            simplex_table = simplex_table.copy()
            rColumn = {
                k: v for k, v in zip(
                    rowsNames, 
                    [self.format_fraction(Fraction(x)) for x in simplex_table[:, -1].copy()]
                )
            }
            formatTable = {
                'tableName': table_name,
                'colsNames': colsNames,
                'rowsNames': rowsNames,
                'table': {row: val for row, val in zip(rowsNames, table_values)},
                'rColumn': rColumn 
            }
        else:
            simplex_table = simplex_table.copy()
            entire_pivot_col = [self.format_fraction(x) for x in simplex_table[:, pivot_col]]
            entire_pivot_row = [self.format_fraction(x) for x in simplex_table[pivot_row]]
            entering_row = entering_row.copy()
            pivotCol = {
                    'colName': colsNames[pivot_col],
                    'colNum': pivot_col.copy(),
                    'entireCol': entire_pivot_col.copy(),
                    'value': entire_pivot_col[0]
            }
            pivotRow = {
                    'rowName': rowsNames[pivot_row],
                    'rowNum': pivot_row,
                    'entireRow': entire_pivot_row.copy(),
                    'value': entire_pivot_row[pivot_col]
            }
            pivotValue = pivot_value
            enteringRow = {
                    'rowName': colsNames[pivot_col],
                    'entireRow': entering_row
            }
            table = {row: val for row, val in zip(rowsNames, table_values)}

            formatTable = {
                'tableName': table_name,
                'colsNames': colsNames,
                'rowsNames': rowsNames,
                'table': table,
                'pivotCol': pivotCol,
                'pivotRow': pivotRow,
                'pivotValue': pivotValue,
                'enteringRow': enteringRow
            }
        return formatTable
    
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
                values.append('0')
        
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

        # Genera el nombre de las columnas de la tabla simplex inicial.
        column_names = ['X' + str(i) for i in range(1, num_variables + 1)]
        column_names += ['S' + str(i) for i in range(1, num_constraints + 1)]
        column_names.append('R')

        # Genera el nombre de las filas de la tabla simplex inicial.
        row_names = []
        row_names.append('Z')
        row_names += ['S' + str(i) for i in range(1, num_constraints + 1)]

        # Genera la tabla simplex inicial con 0s.
        simplex_table = np.zeros((num_constraints + 1, num_variables + num_constraints + 1), dtype=object)
        simplex_table[0][:num_variables] = [Fraction(x) for x in z_row[:-1]]
        simplex_table[0][-1] = Fraction(z_row[-1])

        # Si alguna restricción tiene signo >= se cambia de sentido toda la restricción multiplicando por (-1).
        for constraint in constraints:
            if constraint[-2] == '>=':
                constraint[-2] = '<='
                for i in range(len(constraint)):
                    if str(constraint[i]) != '<=':
                        constraint[i] = str(-1 * int(constraint[i]))

        # Agrega variables de holgura.
        for i, constraint in enumerate(constraints, start=1):
            simplex_table[i][:num_variables] = [Fraction(x) for x in constraint[:-2]]
            if constraint[-2] == '<=':
                simplex_table[i][num_variables+i-1] = 1
            elif constraint[-2] == '>=':
                simplex_table[i][num_variables+i-1] = -1
            simplex_table[i][-1] = Fraction(constraint[-1])

        # Matriz con los valores de la tabla inicial.
        auxTable = []
        for row in simplex_table:
            auxRow = [self.format_fraction(x) for x in row]
            auxTable.append(auxRow.copy())

        # Genera la tabla simplex inicial y se guarda.
        firstTable = self.format_table(
            'first', 
            None, 
            '1ra', 
            column_names, 
            row_names, 
            None, 
            None, 
            None, 
            None, 
            auxTable
        )
        
        self.firstTable = firstTable

        tableNum = 0
        done = False
        # Se repite hasta que el proceso termine, termina si no existe ningún numero negativo (maximiza) o ningún numero positivo 
        # (minimiza) en la fila Z.
        while done == False:
            tableNum = tableNum + 1

            # Columna pivote, la columna con el menor numero negativo cuando se maximiza y mayor numero positivo cuando se minimiza.
            objRowCopy = np.copy(simplex_table[0][:-1])
            if self.operation == 'max':                
                objRowCopy[objRowCopy == 0] = np.inf
                negatives = objRowCopy[objRowCopy < 0]
                if len(negatives) == 0:
                    done = True
                    self.solved = False
                    self.errors.append('Error: No se puede determinar la columna pivote para empezar la optimización del problema de maximización.')
                    break
                else:
                    pivot_column = np.argmin(simplex_table[0][:-1])         
            elif self.operation == 'min':
                objRowCopy[objRowCopy == 0] = -np.inf
                positives = objRowCopy[objRowCopy > 0]
                if len(positives) == 0:
                    done = True
                    self.solved = False
                    self.errors.append('Error: No se puede determinar la columna pivote para empezar la optimización del problema de minimización.')
                    break
                else:
                    pivot_column = np.argmax(simplex_table[0][:-1])

            # Fila pivote.
            pivot_row = -1
            min_ratio = float('inf')
            for i in range(1, num_constraints + 1):
                # Encuentra el resultado positivo mas pequeño de la division entre los valores de la columna R y la columna pivote.
                if simplex_table[i][pivot_column] > 0:
                    # Columna R / columna pivote.
                    ratio = simplex_table[i][-1] / simplex_table[i][pivot_column]
                    if ratio < min_ratio and ratio > 0:
                        min_ratio = ratio
                        pivot_row = i

            # Numero pivote.
            pivot_value = simplex_table[pivot_row][pivot_column]

            # Matriz con los valores de la nueva tabla.
            auxTable = []
            for row in simplex_table:
                auxRow = [self.format_fraction(x) for x in row]
                auxTable.append(auxRow.copy())
            
            row_names_aux = row_names.copy()

            # Cambia el nombre de la fila pivote por la columna pivote.
            row_names[pivot_row] = column_names[pivot_column]

            simplex_table_aux = simplex_table.copy()

            # Genera la fila entrante para la nueva tabla simplex.
            simplex_table[pivot_row] = simplex_table[pivot_row] / pivot_value
            entering_row = [self.format_fraction(x) for x in simplex_table[pivot_row]]

            # Genera nueva tabla simplex con toda la información y se guarda.
            newTable = self.format_table(
                'new',
                simplex_table_aux,
                '#'+str(tableNum),
                column_names,
                row_names_aux,
                pivot_column,
                pivot_row,
                pivot_value,
                entering_row,
                auxTable
            )
            self.allTables.append(newTable)

            # Operaciones entre filas para convertir números en columna pivote a 0.
            for i in range(num_constraints + 1):
                if i != pivot_row:
                    factor = simplex_table[i][pivot_column]
                    simplex_table[i] -= factor * simplex_table[pivot_row]

            # Si ya no existe ningún numero negativo cuando se maximiza o positivo cuando se minimiza, se genera la tabla final.
            if self.operation == 'max' and np.any(simplex_table[0][:-1] < 0):
                done = False
            elif self.operation == 'min' and np.any(simplex_table[0][:-1] > 0):
                done = False
            else:
                done = True                                

                # Matriz con los valores de la tabla final.
                auxTable = []
                for row in simplex_table:
                    auxRow = [self.format_fraction(x) for x in row]
                    auxTable.append(auxRow.copy())

                # Genera tabla simplex final con toda la información y se guarda.
                lastTable = self.format_table(
                    'last',
                    simplex_table,
                    'Ult',
                    column_names,
                    row_names,
                    None,
                    None,
                    None,
                    None,
                    auxTable
                )
                self.lastTable = lastTable

                # Genera la solución del problema.
                self.solution =  self.format_solution(lastTable['rColumn'])
                self.solved = True                

        return simplex_table


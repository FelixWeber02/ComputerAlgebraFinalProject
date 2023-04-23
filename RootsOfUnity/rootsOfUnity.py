from itertools import combinations, product
import pprint

pp = pprint.PrettyPrinter(indent=1)

actual_values = [
    "1",
    "(E^((2*I*Pi)/9))",
    "(E^((4*I*Pi)/9))",
    "(E^((2*I*Pi)/3))",
    "(E^((8*I*Pi)/9))",
    "(E^(-(8*I*Pi)/9))",
    "(E^(-(2*I*Pi)/3))",
    "(E^(-(4*I*Pi)/9))",
    "(E^(-(2*I*Pi)/9))"
]
polynomials_list = ""
variables_list = "{"

## Read in the sudoku problem
sudoku_problem = []
with open('../SampleProblems/sampleSudoku.csv') as f:
    for _ in range(9):
        sudoku_problem.append(f.readline().split(",")[:9])

# sudoku_problem = [["0" for i in range(9)] for j in range(9)]

## Get our list of variables
variables = []
for i in range(9):
    for j in range(9):
        if sudoku_problem[i][j] == "0":
            variables_list += f'x{i}{j},'
            variables.append(f'x{i}{j}')
            sudoku_problem[i][j] = f'x{i}{j}'
        else:
            sudoku_problem[i][j] = actual_values[int(sudoku_problem[i][j]) - 1]

if variables_list[len(variables_list)-1] == ',':
    variables_list = variables_list[:len(variables_list)-1]

variables_list += "}"

## Generate our list of polynomials
polys = []

# Add the polynomials that ensure that each variable is in the list of possible values
for var in variables:
    val_poly = f'(({var})^9)-1'
    polys.append(val_poly)
    polynomials_list += val_poly + ","

# Add polynomials that ensure each variable in the same row has a different value
for row in sudoku_problem:
    for comb in combinations(row, 2):
        x, y = list(map(str, comb))
        row_poly = f'(({x}^2) + ({x} * {y}) + ({y}^2))*(({x}^6)+({x}^3)*({y}^3) + ({y}^6))'
        polys.append(row_poly)

# Add polynomials that ensure each variable in the same col has a different value
for col in range(9):
    col_vals = [row[col] for row in sudoku_problem]
    for comb in combinations(col_vals, 2):
        x, y = list(map(str, comb))
        col_poly = f'(({x}^2) + ({x} * {y}) + ({y}^2))*(({x}^6)+({x}^3)*({y}^3) + ({y}^6))'
        polys.append(col_poly)

x_incs = [-1, 1, 0]
y_incs = [-1, 1, 0]
box_incs = product(x_incs, y_incs)
# Add polynomials that ensure that each variable in the same box has a different value
for box_x in range(1, 8, 3):
    for box_y in range(1, 8, 3):
        box_vals =[sudoku_problem[box_x + x_inc][box_y + y_inc] for x_inc, y_inc in box_incs]
        for comb in combinations(box_vals, 2):
            x, y = list(map(str, comb))
            col_poly = f'(({x}^2) + ({x} * {y}) + ({y}^2))*(({x}^6)+({x}^3)*({y}^3) + ({y}^6))'
            polys.append(col_poly)

# pp.pprint(polys)
# print(len(polys))

print(variables_list)

## Add commands to string
result_string = 'Expand[{' + ",".join(polys) + '}]'

with open("output.txt", "w") as f:
    f.write(result_string)
    f.close()
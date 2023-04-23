from itertools import combinations, product
import pprint

problem = []
polys = []

pp = pprint.PrettyPrinter(indent=1)

varnames = ["w", "x", "y", "z"]

# Read in the shidoku problem
with open("../SampleProblems/sampleShidoku.csv") as f:
    for i in range(4):
        problem.append(f.readline().split(",")[:4])

# Make a list of variables
varstring = ""
for i in range(4):
    for j in range(4):
        var_poly = ""
        for l in ["w", "x", "y", "z"]:
            var = f'{l + str(i) + str(j)}'
            var_poly += var + "+"
            varstring += f'{var},'
            polys.append(f'{var} * ({var} - 1)')
        if problem[i][j] != 0:
            polys.append(f'{varnames[int(problem[i][j]) - 1] + str(i) + str(j)} - 1')
        var_poly = var_poly[:len(var_poly) - 1] + "-1"
        polys.append(var_poly)

varstring = varstring[:len(varstring) -1]

# Make sure all vars in the same row have different values
for i in range(4):
    for l in varnames:
        row_poly = ""
        for j in range(4):
            row_poly += f'{l + str(i) + str(j)}+'
        row_poly = row_poly[:len(row_poly)-1] + "-1"
        polys.append(row_poly)

# Make sure all vars in same col have different values
for i in range(4):
    for l in varnames:
        col_poly = ""
        for j in range(4):
            col_poly += f'{l + str(j) + str(i)}+'
        col_poly = col_poly[:len(col_poly)-1] + "-1"
        polys.append(col_poly)

# Make sure all vars in the same section have different values
for i in range(0,3,2):
    for j in range(0, 3, 2):
        for l in varnames:
            box_poly = ""
            for x_inc, y_inc in [(0,0), (1, 0), (0,1), (1,1)]:
                box_poly += f'{l + str(i + x_inc) + str(j + y_inc)}+'
            box_poly = box_poly[:len(box_poly) - 1] + "-1"
            polys.append(box_poly)

# Write the output to a file
result_string = 'Expand[{' + ",".join(polys) + '}]'

with open("booleanShidokuOutput.txt", "w") as f:
    f.write(result_string)

pp.pprint(varstring)
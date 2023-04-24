from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
from itertools import product
import pprint
import math

varnames = {
    4: ["w", "x", "y", "z"],
    9: ["a", "b", "c", "d", "k", "f", "g", "h", "j"]
    }

var_to_val_map = {
    4: {
        "w": 1,
        "x": 2,
        "y": 3,
        "z": 4
    },
    9: {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
        "k": 5,
        "f": 6,
        "g": 7,
        "h": 8,
        "j": 9
    }
}

pp = pprint.PrettyPrinter(indent=1)

def read_problem(filename="../SampleProblems/sampleShidoku.csv", size=4):
    # Read in the shidoku problem
    problem = []
    with open(filename) as f:
        for i in range(size):
            problem.append(f.readline().split(",")[:size])
    return problem

def generate_var_polys(problem, size):
    polys = []
    varstring = ""
    # Make a list of variables
    for i in range(size):
        for j in range(size):
            var_poly = ""
            for l in varnames[size]:
                var = f'{l + str(i) + str(j)}'
                var_poly += var + "+"
                varstring += f'{var},'
                polys.append(f'{var} * ({var} - 1)')
            if problem[i][j] != "0":
                polys.append(f'{varnames[size][int(problem[i][j]) - 1] + str(i) + str(j)} - 1')
            var_poly = var_poly[:len(var_poly) - 1] + "-1"
            polys.append(var_poly)
    varstring = varstring[:len(varstring) -1]
    return varstring, polys

def generate_row_polys(problem, size):
    polys = []
    # Make sure all vars in the same row have different values
    for i in range(size):
        for l in varnames[size]:
            row_poly = ""
            for j in range(size):
                row_poly += f'{l + str(i) + str(j)}+'
            row_poly = row_poly[:len(row_poly)-1] + "-1"
            polys.append(row_poly)
    return polys

def generate_col_polys(problem, size):
    polys = []
    # Make sure all vars in same col have different values
    for i in range(size):
        for l in varnames[size]:
            col_poly = ""
            for j in range(size):
                col_poly += f'{l + str(j) + str(i)}+'
            col_poly = col_poly[:len(col_poly)-1] + "-1"
            polys.append(col_poly)
    return polys

def generate_box_polys(problem, size):
    polys = []
    box_incs = [(0,0), (1, 0), (0,1), (1,1)]
    startVal = 0
    if size == 9:
        x_incs = [-1, 1, 0]
        y_incs = [-1, 1, 0]
        box_incs = list(product(x_incs, y_incs))
        startVal = 1
    # Make sure all vars in the same section have different values
    for i in range(startVal,size - 1,math.sqrt(size)):
        for j in range(startVal, size - 1, math.sqrt(size)):
            for l in varnames[size]:
                box_poly = ""
                for x_inc, y_inc in box_incs:
                    box_poly += f'{l + str(i + x_inc) + str(j + y_inc)}+'
                box_poly = box_poly[:len(box_poly) - 1] + "-1"
                polys.append(box_poly)
    return polys


def generate_polys(problem, size=4):
    varstring, polys = generate_var_polys(problem, size)
    polys += generate_row_polys(problem, size)
    polys += generate_col_polys(problem, size)
    polys += generate_box_polys(problem, size)
    return polys, varstring


def translate_solution(sol, size=4):
    real_solution = [[0 for i in range(size)] for j in range(size)]
    for rule in sol[0]:
        var = str(rule[0]).split("`")[1]
        val = int(rule[1])
        if val == 1:
            l, i, j = [*var]
            real_solution[int(i)][int(j)] = str(var_to_val_map[size][l])
    return real_solution

def writeOutput(real_sol):
    with open("booleanSolution.csv", "w") as f:
        for row in real_sol:
            f.write(",".join(row) + ",\n")
        f.close()


if __name__ == "__main__":
    session = WolframLanguageSession()
    problem = read_problem()
    polys, varstring = generate_polys(problem)
    sol = session.evaluate(wlexpr(f'Solve[GroebnerBasis[{"{" + ",".join(polys) + "}"}, {"{" + varstring + "}"}] == 0]'))
    session.terminate()
    real_sol = translate_solution(sol)
    writeOutput(real_sol)

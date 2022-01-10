from src.formula import TwoCNF
from src.graph import Graph
# from src.cut_solvers import *
from src.max2sat_solvers import preciseSolver
from src.max2sat_solvers import multiLaunch, solveMax2SAT

def TCNF():
    formula = TwoCNF.random_formula_feasible(4, 10)

    return multiLaunch(formula).mean(), preciseSolver(formula)

print(TCNF())

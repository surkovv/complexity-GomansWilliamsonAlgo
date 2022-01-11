from src.formula import TwoCNF
from src.graph import Graph
# from src.cut_solvers import *
from src.max2sat_solvers import preciseSolver
from src.max2sat_solvers import multiLaunch, solveMax2SAT

def TCNF():
    formula = TwoCNF.random_formula_same(4, 5)

    if multiLaunch(formula).mean() < preciseSolver(formula):
        for l1, l2 in formula.disjunctions:
            print(l1, l2)
    return 0

def kek():
    formula = TwoCNF()
    formula.add_str('b*', 'b*')
    formula.add_str('c*', 'c*')
    formula.add_str('d*', 'd*')
    formula.add_str('d', 'd')
    formula.add_str('d*', 'd*')

    return multiLaunch(formula).mean()

print(TCNF())


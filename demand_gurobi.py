import gurobipy as gb
import random
import time
import numpy as np

class DemandGUROBI:
    def __init__(self, choreographers, dancers, utilities, capacities):
        self.dancer_names = dancers
        self.dancer_models = []
        budgets = np.linspace(start = 100, stop = 101, num = len(dancers))
        for i in range(len(dancers)):
            self.dancer_models.append(DancerGUROBI(choreographers, utilities[i], budgets[i], capacities[i]))

    def demand(self, prices):
        allocation = np.zeros_like(prices)
        for d in self.dancer_models:
            allocation = np.add(allocation, d.demand(prices))
        return allocation


class DancerGUROBI:
    def __init__(self, choreographers, utility, budget, capacity):
        util = {}
        for i, c in enumerate(choreographers):
            util[c] = utility[i]
        # initialize MIP
        self.prob = gb.Model("dancer")
        self.prob.setParam('OutputFlag', 0)
        # add variables
        self.vars = self.prob.addVars(choreographers, vtype = gb.GRB.BINARY, name='dance')
        # add objective
        self.prob.setObjective(self.vars.prod(util), gb.GRB.MAXIMIZE)
        # constraints
        self.budgetConstraint = self.prob.addConstr(sum(0.0 * self.vars[a] for a in self.vars), sense=gb.GRB.LESS_EQUAL, rhs=float(budget), name='budget')
        self.prob.addConstr(sum(1.0 * self.vars[a] for a in self.vars), sense=gb.GRB.LESS_EQUAL, rhs=float(capacity),name='capacity')

    def demand(self, prices):
        for i in prices:
            self.prob.chgCoeff(self.budgetConstraint, self.vars[i], prices[i])
        self.prob.optimize()
        return np.array([v.x for v in self.prob.getVars()])


def time_trial():
    print('GUROBI')
    start = time.time()
    lst = [DancerGUROBI(choreographers,[random.uniform(0,1) for _ in choreographers],100+random.uniform(0,1),random.randint(1,5)) for _ in range(200)]
    print(time.time()-start)
    start = time.time()
    for _ in range(100):
        prices = [random.uniform(0,1) for _ in range(20)]
        prices = {}
        for c in choreographers:
            prices[c] = random.uniform(0,1)
        for d in lst:
            d.demand(prices)
    print(time.time()-start)
import gurobipy as gb
import random
import time
import numpy as np


class DemandGUROBI:
    # choreographers: list of name
    # dancers: list of names
    # utilities: list of dicts of utilities, corr. w/ dancers
    # capacities: list of capacities, corr. w/ dancers
    # conflicts: list of tuples of conflicts
    def __init__(self, HZchoreographers, EBchoreographers, dancers, utilities, HZcapacities, EBcapacities, conflicts):
        self.dancer_names = dancers
        self.dancer_models = []
        self.choreographers = HZchoreographers + EBchoreographers
        budgets = np.linspace(start = 100, stop = 107, num = len(dancers))
        np.random.shuffle(budgets)
        for i in range(len(dancers)):
            self.dancer_models.append(DancerGUROBI(HZchoreographers, EBchoreographers, utilities[i], 
                                        budgets[i], HZcapacities[i], EBcapacities[i], conflicts))

    def demand(self, prices):
        allocation = np.zeros_like(prices)
        for d in self.dancer_models:
            allocation = np.add(allocation, d.demand(prices, self.choreographers))
        return allocation

    def allocation(self, prices):
        return np.array([d.demand(prices, self.choreographers) for d in self.dancer_models])

    def full(self, ci, prices):
        for d in self.dancer_models:
            d.full(ci, prices, self.choreographers)

    def dancers(self):
        return self.dancer_models


class DancerGUROBI:
    def __init__(self, HZchoreographers, EBchoreographers, utility, budget, HZcapacity, EBcapacity, conflicts):
        self.choreographers = HZchoreographers + EBchoreographers
        # initialize MIP
        self.prob = gb.Model("dancer")
        self.prob.setParam('OutputFlag', 0)
        # add variables
        self.vars = self.prob.addVars(self.choreographers, vtype = gb.GRB.BINARY, name='dance')
        # add objective
        self.prob.setObjective(self.vars.prod(utility), gb.GRB.MAXIMIZE)
        # budget constraint
        self.budget = budget
        self.budgetConstraint = self.prob.addConstr(sum(0.0 * self.vars[a] for a in self.vars), sense=gb.GRB.LESS_EQUAL, rhs=float(budget), name='budget')
        # capacity constraints
        self.prob.addConstr(sum(1.0 * self.vars[x] for x in HZchoreographers), sense=gb.GRB.LESS_EQUAL, rhs=float(HZcapacity),name='HZcapacity')
        self.prob.addConstr(sum(1.0 * self.vars[x] for x in EBchoreographers), sense=gb.GRB.LESS_EQUAL, rhs=float(EBcapacity),name='EBcapacity')
        # scheduling constraints
        for conflict in conflicts:
            self.prob.addConstr(sum(1.0 * self.vars[x] for x in conflict), sense=gb.GRB.LESS_EQUAL, rhs=1.0, name='conflicts')

    # prices is np array
    def demand(self, prices, choreographers):
        for i, p in enumerate(prices):
            self.prob.chgCoeff(self.budgetConstraint, self.vars[choreographers[i]], p)
        self.prob.optimize()
        return np.array([v.x for v in self.prob.getVars()])

    def stage3demand(self, prices, choreographers):
        self.budgetConstraint.rhs = self.budget*1.1
        for i, p in enumerate(prices):
            self.prob.chgCoeff(self.budgetConstraint, self.vars[choreographers[i]], p)
        self.prob.optimize()
        return np.array([v.x for v in self.prob.getVars()])

    def full(self, ci, prices, choreographers):
        if not self.demand(prices, choreographers)[ci] == 1:
            self.prob.chgCoeff(self.budgetConstraint, self.vars[choreographers[ci]], 200.)


def time_trial():
    choreographers = ['arst'+str(i) for i in range(20)]
    conflicts = [('arst1','arst2'),('arst3','arst4'),('arst5','arst6')]
    print('GUROBI')
    start = time.time()
    lst = [DancerGUROBI(choreographers,[random.uniform(0,1) for _ in choreographers],100+random.uniform(0,1),random.randint(1,5), conflicts) for _ in xrange(200)]
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

if __name__ == '__main__':
    time_trial()
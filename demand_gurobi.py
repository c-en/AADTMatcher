import gurobipy as gb
import random
import time
import numpy as np

class DemandGUROBI:
    # choreographers: list of name
    # dancers: list of names
    # utilities: list of lists of utilities, corr. w/ dancers
    # capacities: list of capacities, corr. w/ dancers
    # conflicts: list of tuples of conflicts
    def __init__(self, choreographers, dancers, utilities, capacities, conflicts):
        self.dancer_names = dancers
        self.dancer_models = []
        budgets = np.linspace(start = 100, stop = 101, num = len(dancers))
        for i in range(len(dancers)):
            self.dancer_models.append(DancerGUROBI(choreographers, utilities[i], budgets[i], capacities[i], conflicts))

    def demand(self, prices):
        allocation = np.zeros_like(prices)
        for d in self.dancer_models:
            allocation = np.add(allocation, d.demand(prices))
        return allocation

    def allocation(self, prices):
        return np.array([d.demand(prices) for d in self.dancer_models])


class DancerGUROBI:
    def __init__(self, choreographers, utility, budget, capacity, conflicts):
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
        # budget constraint
        self.budgetConstraint = self.prob.addConstr(sum(0.0 * self.vars[a] for a in self.vars), sense=gb.GRB.LESS_EQUAL, rhs=float(budget), name='budget')
        # capacity constraint
        self.prob.addConstr(sum(1.0 * self.vars[x] for x in self.vars), sense=gb.GRB.LESS_EQUAL, rhs=float(capacity),name='capacity')
        # scheduling constraints
        for conflict in conflicts:
            self.prob.addConstr(sum(1.0 * self.vars[x] for x in conflict), sense=gb.GRB.LESS_EQUAL, rhs=1.0, name='conflicts')

    def demand(self, prices):
        for i in prices:
            self.prob.chgCoeff(self.budgetConstraint, self.vars[i], prices[i])
        self.prob.optimize()
        return np.array([v.x for v in self.prob.getVars()])


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
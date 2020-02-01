import gurobipy as gb
import random
import time
import numpy as np

# generates a given agent's demand MIP
class AgentLinear:
    # objects: array of objects to be allocated
    # capacity: allocation capacity of this agent (integer)
    # budget: budget for this agent (float)
    # value: linear values of objects for this agent (length |object| array)
    # complements: matrix of values for each agent for having 2 objects simultaneously (|agent| by |object|)
    def __init__(self, objects, capacity, budget, value, complements):
        self.objects = objects
        # initialize MIP
        self.prob = gb.Model("agent")
        self.prob.setParam("OutputFlag", 0)
        # add variables
        self.object_vars = self.prob.addVars(self.objects, vtype = gb.GRB.BINARY, name='object')
        complement_vars = []
        complement_coeffs = {}
        for objs, u in np.ndenumerate(complements):
            if not u==0:
                complement_vars.append(objs)
                complement_coeffs[objs] = u
        self.complement_vars = self.prob.addVars(complement_vars, vtype = gb.GRB.BINARY, name = 'complement')
        # budget constraint
        self.budget = budget
        self.budgetConstraint = self.prob.addConstr(sum(0.0 * self.object_vars[a] for a in self.object_vars), sense=gb.GRB.LESS_EQUAL, rhs=float(budget), name='budget')
        # capacity constraints
        self.prob.addConstr(sum(1.0 * self.object_vars[x] for x in objects), sense=gb.GRB.LESS_EQUAL, rhs=float(capacity),name='capacity')
        # complement constraints
        for objs in complement_vars:
            self.prob.addConstr(self.complement_vars[objs] - 1.0*self.object_vars[self.objects[objs[0]]] - 1.0*self.object_vars[self.objects[objs[1]]], sense=gb.GRB.GREATER_EQUAL, rhs=-1.0,name='complement1'+str(objs))
            self.prob.addConstr(self.complement_vars[objs] - 1.0*self.object_vars[self.objects[objs[0]]], sense=gb.GRB.LESS_EQUAL, rhs=0.0,name='complement2'+str(objs))            
            self.prob.addConstr(self.complement_vars[objs] - 1.0*self.object_vars[self.objects[objs[1]]], sense=gb.GRB.LESS_EQUAL, rhs=0.0,name='complement23'+str(objs))  
        # add objective
        self.prob.setObjective(self.object_vars.prod({objects[i]:v for i,v in enumerate(value)}) + self.complement_vars.prod(complement_coeffs), gb.GRB.MAXIMIZE)

    # get this agent's (demand, objective value) when faced with a given price vector
    def demand(self, prices, budgetmult = 1.):
        # set MIP bugdet constraint to reflect to given prices
        for i, p in enumerate(prices):
            self.prob.chgCoeff(self.budgetConstraint, self.object_vars[self.objects[i]], p/budgetmult)
        self.prob.optimize()
        return (np.array([self.object_vars[v].x for v in self.object_vars]), self.prob.objVal)

# generates a set of agent demand MIPs for a given market
class MarketLinear:
    # objects: array of objects to be allocated
    # agents: agents in the market; MUST BE SORTED (or shuffled) IN ORDER OF INCREASING BUDGET
    # values: linear values of objects for each agent (|agent| by |object| array)
    # complements: matrix of values for each agent for having 2 objects simultaneously (|agent| by |object| by |object|)
    # capacities: allocation capacity of each agent (|agent| length array)
    # note: budgets are distributed linearly, with first agent lowest - order agents as desired before initializing
    def __init__(self, agents, objects, capacities, values, complements):
        self.agent_names = agents
        self.agent_models = []
        self.objects = objects
        budgets = np.linspace(start = 100., stop = 107., num = len(agents))
        for i in range(len(agents)):
            self.agent_models.append(AgentLinear(objects, capacities[i], budgets[i], values[i], complements[i]))

    # given price vector, get total demand and total utility
    def demand(self, prices):
        total_demand = np.zeros_like(prices)
        total_utility = 0
        for a in self.agent_models:
            dem, util = a.demand(prices)
            total_demand = np.add(total_demand, dem)
            total_utility += util
        return total_demand, total_utility

    # given price vector, get allocation
    def allocation(self, prices):
        return np.array([a.demand(prices)[0] for a in self.agent_models])

    # aftermarket allocations with increased budgets and restricted allocations
    def aftermarket(self, prices, availabilities):
        allocation = self.allocation(prices)
        demand = np.sum(allocation, axis=0)
        noChanges = False
        while not noChanges:
            noChanges = True
            curPrices = np.array(prices)
            for i in range(len(prices)):
                if demand[i] >= availabilities[0][i]:
                    curPrices[i] = 1000.
            for i, a in enumerate(self.agent_models):
                indPrices = np.array(curPrices)
                curAlloc = allocation[i]
                for j, d in enumerate(curAlloc):
                    if d == 1.:
                        indPrices[j] = prices[j]
                newAlloc = a.demand(indPrices, budgetmult = 1.1)[0]
                if not np.array_equal(newAlloc, curAlloc):
                    noChanges = False
                    allocation[i] = newAlloc
                    break
        return np.sum(allocation, axis=0), allocation


    # return list of agent models
    def agents(self):
        return self.agent_models

def test():
    objects = ['A','B','C']
    value = [1,1,4]
    complements = [[0,3,0],[0,0,0],[0,0,0]]
    capacity = 2
    budget = 100
    agent = AgentLinear(objects, value, complements, capacity, budget)
    print agent.demand([50,50,50])

if __name__ == '__main__':
    test()
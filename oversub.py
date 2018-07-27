import numpy as np
from demand_gurobi import DemandGUROBI
import tabu

def over(D, p, demand, choreographers, choreo_min, choreo_max):
    e = 5./300
    j = np.argmax(demand - choreo_max)
    while np.any(demand - choreo_max>0):
        ds = (demand - choreo_max)[j] / 2
        l = p[j]
        h = 110.
        while h-l > e:
            p[j] = (h+l)/2.
            demand = D.demand(p, choreographers)
            if demand[j] >= ds:
                l = p[j]
            else:
                h = p[j]
        p[j] = h
        demand = D.demand(p, choreographers)
        j = np.argmax(demand - choreo_max)
    return p

def final_allocation(D, p, allocation, choreographers, choreo_min, choreo_max):
    done = False
    while not done:
        done = True
        demand = np.sum(allocation, axis=0)
        undersub = demand - choreo_min
        for i, exd in enumerate(undersub):
            if exd > 0:
                D.full(i, p)
        for i, d in enumerate(D.dancers()):
            newIndDem = d.stage3demand(p, choreographers)
            if not newIndDem == allocation[i]:
                done = False
                allocation[i] = newIndDem
                break
    return allocation
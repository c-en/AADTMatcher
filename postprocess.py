import numpy as np
from demand_gurobi import DemandGUROBI

def oversub(D, p, allocation, choreo_min, choreo_max):
    demand = np.sum(allocation, axis = 0)
    e = 5./300
    j = np.argmax(demand - choreo_max)
    while np.any(demand - choreo_max>0):
        ds = (demand - choreo_max)[j] / 2
        l = p[j]
        h = 110.
        while h-l > e:
            p[j] = (h+l)/2.
            demand = D.demand(p)
            if demand[j] >= ds:
                l = p[j]
            else:
                h = p[j]
        p[j] = h
        demand = D.demand(p)
        j = np.argmax(demand - choreo_max)
    print "STAGE 2 DEMAND"
    print demand
    return p

def undersub(D, p, allocation, choreo_min, choreo_max, choreographers):
    print 'UNDERSUB START'
    print p
    print allocation
    fullC = set([])
    done = False
    while not done:
        done = True
        demand = np.sum(allocation, axis=0)
        excess = demand - choreo_min
        for i, exd in enumerate(excess):
            if exd > 0:
                D.full(i, p)
                fullC.add(i)
        for i, d in enumerate(D.dancers()):
            newIndDem = d.stage3demand(p, choreographers)
            if not np.array_equal(newIndDem, allocation[i]):
                done = False
                allocation[i] = newIndDem
                break
    print "STAGE 3 DEMAND"
    print np.sum(allocation, axis=0)
    return p, allocation

def final_allocation(D, p, allocation, choreo_min, choreo_max, choreographers):
    p = oversub(D, p, allocation, choreo_min, choreo_max)
    allocation = D.allocation(p)
    return undersub(D, p, allocation, choreo_min, choreo_max, choreographers)
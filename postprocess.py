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
            if demand[j] >= choreo_max[j] + ds:
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
        excess = demand - choreo_max
        for i, exd in enumerate(excess):
            if exd > 0:
                fullC.add(i)
        for j, d in enumerate(D.dancers()):
            newIndDem = d.stage3demand(p, choreographers, fullC, allocation[j])
            if not np.array_equal(newIndDem, allocation[j]):
                done = False
                allocation[j] = newIndDem
                break
    print "STAGE 3 DEMAND"
    print np.sum(allocation, axis=0)
    return p, allocation

def final_allocation(D, p, allocation, choreo_min, choreo_max, choreographers):
    p = oversub(D, p, allocation, choreo_min, choreo_max)
    allocation = D.allocation(p)
    return undersub(D, p, allocation, choreo_min, choreo_max, choreographers)
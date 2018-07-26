from demand_gurobi import DemandGUROBI
import math
import random
import csv
import numpy as np
import time
import postprocess

maxTime = 22600# 28800
GradientNeighbors = np.linspace(0.05, 0.5, num=10)

def vector_error(demand, choreo_min, choreo_max):
    under = np.clip(np.subtract(choreo_min, demand),0,float('inf'))
    over = np.clip(np.subtract(demand, choreo_max),0,float('inf'))
    diff = np.maximum(under, over)
    return diff

# calculates clearing error of given choreo capacities and given demand
def clearing_error(demand, choreo_min, choreo_max):
    diff = vector_error(demand, choreo_min, choreo_max)
    return np.sum(np.square(diff))
    
# calculates neighboring price vectors of a given price vector p
# return tuple: list of neighbor prices sorted by clearing error, list of corr. demand vecs, list of corr. error
def N(p, curDemand, choreo_min, choreo_max, D, choreographers):
    neighbors = []
    # gradient neighbors
    demandError = vector_error(curDemand, choreo_min, choreo_max)
    div = max(np.absolute(demandError))
    demandError /= div
    steps = np.outer(GradientNeighbors, demandError)
    for step in steps:
        priceVec = np.multiply(step+1, p)
        demand = D.demand(priceVec, choreographers)
        error = clearing_error(demand, choreo_min, choreo_max)
        neighbors.append((priceVec, demand, error))
    # individual adjustment neighbors
    for i in range(len(p)):
        if random.uniform(0,1) > 0.5:
            if curDemand[i] < choreo_min[i]:
                priceVec = np.copy(p)
                priceVec[i] = 0
                demand = D.demand(priceVec, choreographers)
                error = clearing_error(demand, choreo_min, choreo_max)
                neighbors.append((priceVec, demand, error))
            elif curDemand[i] > choreo_max[i]:
                priceVec = np.copy(p)
                priceVec[i] *= 1.05
                demand = D.demand(priceVec, choreographers)
                while demand[i] >= curDemand[i]:
                    priceVec[i] *= 1.05
                    demand = D.demand(priceVec, choreographers)
                error = clearing_error(demand, choreo_min, choreo_max)
                neighbors.append((priceVec, demand, error))
    # sort list of neighbors by best to worst clearing error
    neighbors.sort(key = lambda x: x[2])
    return zip(*neighbors)

def tabu(HZchoreographers, EBchoreographers, dancers, utilities, HZcapacities, EBcapacities, conflicts, choreo_min, choreo_max):
    choreographers = HZchoreographers + EBchoreographers
    # initialize demand object
    D = DemandGUROBI(HZchoreographers, EBchoreographers, dancers, utilities, HZcapacities, EBcapacities, conflicts)
    # begin random restarts
    bestError = float('inf')
    bestPrice = None
    startTime = time.time()
    restarts = 0
    while time.time() - startTime < maxTime:
        print "RANDOM RESTART "+str(restarts)
        restarts += 1
        # start search from random, reasonable price vector
        p = np.random.uniform(low=0.0, high=100.0, size=len(choreographers))
        curDemand = D.demand(p, choreographers)
        # searchError tracks best error found in this search start
        searchError = clearing_error(curDemand, choreo_min, choreo_max)
        # set of tabu demand locations
        tabu = set([])
        # c tracks number of steps without improving error, t tracks total steps
        c = 0
        t = 0
        # restart search if error has not improved in 5 steps, 
        restartTime = time.time()
        while c < 5 and time.time() - restartTime < 300:
            foundNextStep = False
            # get neighboring price vecs, their demand vecs, and their errors
            nbPrices, nbDemands, nbErrors = N(p, curDemand, choreo_min, choreo_max, D, choreographers)
            # look thru neighbors for non-tabu price vec
            for i in range(len(nbPrices)):
                d = tuple(nbDemands[i])
                if not d in tabu:
                    foundNextStep = True
                    # if non-tabu, add to tabu
                    tabu.add(d)
                    # update current location
                    p = nbPrices[i]
                    curDemand = D.demand(p, choreographers)
                    # update current error and (if needed) best error in current restart
                    # if improved, reset c; if not, increment c
                    currentError = nbErrors[i]
                    if currentError < searchError:
                        searchError = currentError
                        c = 0
                    else:
                        c += 1
                    # update current "high score" if needed, over all restarts
                    if currentError < bestError:
                        bestError = currentError
                        bestPrice = p
                    break
            if not foundNextStep:
                break
        print time.time() - startTime
    print "########################################"
    print "BEST ERROR: " + str(bestError)
    print "########################################"
    allocation =D.allocation(bestPrice, choreographers)
    finalPrice, finalAllocation = postprocess.final_allocation(D, p, allocation, choreographers, choreo_min, choreo_max)
    print "BEST PRICE: "
    print finalPrice
    return finalAllocation
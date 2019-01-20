import math
import random
import csv
import numpy as np
import time

# maximum runtime for tabu
maxTime = 2*60

# parameter for the range of gradient neighbors to calculate
GradientNeighbors = np.linspace(0.05, 0.5, num=10)

def vector_error(demand, avail):
    under = np.clip(np.subtract(avail[0], demand),0,float('inf'))
    over = np.clip(np.subtract(demand, avail[1]),0,float('inf'))
    diff = np.maximum(under, over)
    return diff
# calculates clearing error of given choreo avail and given demand
def clearing_error(demand, avail):
    diff = vector_error(demand, avail)
    return np.sum(np.square(diff))  

# calculates neighboring price vectors of a given price vector p
# return tuple: list of neighbor prices sorted by clearing error, list of corr. demand vecs, list of corr. error
def N(p, curDemand, avail, Market):
    print curDemand
    neighbors = []
    # gradient neighbors
    demandError = vector_error(curDemand, avail)
    div = max(np.absolute(demandError))
    if not div == 0:
        demandError /= div
    steps = np.outer(GradientNeighbors, demandError)
    for step in steps:
        priceVec = np.multiply(step+1, p)
        demand = Market.demand(priceVec)
        error = clearing_error(demand, avail)
        neighbors.append((priceVec, demand, error))
    # individual adjustment neighbors
    for i in range(len(p)):
        if random.uniform(0,1) > 0.5:
            if curDemand[i] < avail[0][i]:
                priceVec = np.copy(p)
                priceVec[i] = 0
                demand = Market.demand(priceVec)
                error = clearing_error(demand, avail)
                neighbors.append((priceVec, demand, error))
            elif curDemand[i] > avail[1][i]:
                priceVec = np.copy(p)
                priceVec[i] *= 1.05
                demand = Market.demand(priceVec)
                while demand[i] >= curDemand[i]:
                    if priceVec[i] == 0:
                        priceVec[i] = 1
                    priceVec[i] *= 1.05
                    demand = Market.demand(priceVec)
                error = clearing_error(demand, avail)
                neighbors.append((priceVec, demand, error))
    # sort list of neighbors by best to worst clearing error
    neighbors.sort(key = lambda x: x[2])
    return zip(*neighbors)
  
# performs Tabu Search for A-CEEI
# agents: list of agents (standard)
# objects: list of objects to be allocated (standard)
# avail: availability of each object (standard) - format [[array of lower bound],[array of upper bound]]
# Market: object with methods demand and allocation
# demand: takes in price vector, returns total demand
# allocation: takes in price vector, returns full allocation
# returns the final allocation, and arrays for time and besterror after each random restart
def tabu(agents, objects, avail, Market):
    times = []
    besterrors = []
    # begin random restarts
    bestError = float('inf')
    bestPrice = None
    startTime = time.time()
    restarts = 0
    while time.time() - startTime < maxTime and bestError>0:
        pricelist = []
        demandlist = []
        print "RANDOM RESTART "+str(restarts)
        restarts += 1
        # start search from random, reasonable price vector
        p = np.random.uniform(low=0.0, high=107.0, size=len(objects))
        curDemand = Market.demand(p)
        # searchError tracks best error found in this search start
        searchError = clearing_error(curDemand, avail)
        # set of tabu demand locations
        taboo = set([])
        # c tracks number of steps without improving error, t tracks total steps
        c = 0
        t = 0
        # restart search if error has not improved in 5 steps, 
        restartTime = time.time()
        while c < 5:
            t += 1
            foundNextStep = False
            # get neighboring price vecs, their demand vecs, and their errors
            nbPrices, nbDemands, nbErrors = N(p, curDemand, avail, Market)
            # look thru neighbors for non-tabu price vec
            for i in range(len(nbPrices)):
                d = tuple(nbDemands[i])
                if not d in taboo:
                    foundNextStep = True
                    # if non-tabu, add to tabu
                    taboo.add(d)
                    # update current location
                    p = nbPrices[i]
                    pricelist.append(p)
                    curDemand = Market.demand(p)
                    demandlist.append(curDemand)
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
        # print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        # for x in pricelist:
        #     print x
        # print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        # for x in demandlist:
        #     print x
        print "STEPS: "+str(t)
        print "ERROR: "+str(currentError)
        times.append(time.time() - startTime)
        besterrors.append(bestError)
        print time.time() - startTime
        print "----------------------------"
    print "########################################"
    print "BEST ERROR: " + str(bestError)
    print "########################################"
    print "STAGE 1 DEMAND"
    print Market.demand(bestPrice)
    allocation = Market.allocation(bestPrice)
    # save initial allocation 
    np.savetxt('preallocation.csv', allocation, delimiter=',')
    print "FINAL PRICE: " + str(bestPrice)
    return allocation, times, besterrors
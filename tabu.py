from demand_gurobi import DemandGUROBI
import math
import random
import csv
import numpy as np


# calculates clearing error of given choreo capacities and given demand
def clearing_error(demand, choreo_min, choreo_max):
    under = np.clip(np.subtract(choreo_min, demand),0,float('inf'))
    over = np.clip(np.subtract(demand, choreo_max),0,float('inf'))
    diff = np.maximum(under, over)
    return np.sum(np.square(diff))
    

# calculates neighboring price vectors of a given price vector p
# return tuple: list of neighbor prices sorted by clearing error, list of corr. demand vecs, list of corr. error
def N(p):
    return [], [], []

def tabu(HZchoreographers, EBchoreographers, dancers, utilities, HZcapacities, EBcapacities, conflicts, choreo_min, choreo_max):
    choreographers = HZchoreographers + EBchoreographers
    # initialize demand object
    D = DemandGUROBI(HZchoreographers, EBchoreographers, dancers, utilities, HZcapacities, EBcapacities, conflicts)
    # begin random restarts
    bestError = float('inf')
    bestPrice = None
    for _ in range(100):
        # start search from random, reasonable price vector
        p = {c: random.uniform(0,100) for c in choreographers}
        # searchError tracks best error found in this search start
        searchError = clearing_error(D.demand(p), choreo_min, choreo_max)
        # set of tabu demand locations
        tabu = set([])
        # c tracks number of steps without improving error
        c = 0
        # restart search if error has not improved in 5 steps
        while c < 5:
            foundNextStep = False
            # get neighboring price vecs, their demand vecs, and their errors
            nbPrices, nbDemands, nbErrors = N(p)
            # look thru neighbors for non-tabu price vec
            for i in range(len(nbPrices)):
                d = tuple(nbDemands[i])
                if not d in tabu:
                    foundNextStep = True
                    # if non-tabu, add to tabu
                    tabu.add(d)
                    # update current location
                    p = nbPrices[i]
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
    return D.allocation(bestPrice)


        
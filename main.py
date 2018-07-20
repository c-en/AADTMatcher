from demand_gurobi import DemandGUROBI
import random
import numpy as np
import pandas as pd

# calculates clearing error of given choreo capacities and given demand
def clearing_error(choreo_cap, demand):
    return np.sum(np.square(np.subtract(choreo_cap, demand)))

# calculates neighboring price vectors of a given price vector p
def N(p):
    return [p]

def main(choreographers, dancers, utilities, dancer_cap, conflicts, choreo_cap):
    # choreographers = []
    # dancers = []
    # utilities = []
    # dancer_cap = []
    # conflicts = []
    # choreo_cap = np.array([])
    # initialize demand object
    D = DemandGUROBI(choreographers, dancers, utilities, dancer_cap, conflicts)
    # begin random restarts
    bestError = float('inf')
    bestPrices = None
    for _ in range(10):
        # start search from random, reasonable price vector
        p = {}
        for c in choreographers:
            p[c] = random.uniform(0,100)
        # searchError tracks best error found in this search start
        d = D.demand(p)
        searchError = clearing_error(choreo_cap, curDemand)
        # set of tabu demand locations
        tabu = set([])
        # c tracks number of steps without improving error
        c = 0
        # restart search if error has not improved in 5 steps
        while c < 5:
            neighbors = N(p, d)
            visited = 0
            for prices in neighbors:
                d = D.demand(prices)
                if not tuple(d) in tabu:
                    break
                visited += 1
            if visited == len(neighbors):
                c = 5
            else:
                p = prices
                tabu.add(tuple(d))
                currentError = clearing_error(choreo_cap, d)
                if currentError < searchError:
                    searchError = currentError
                    c = 0
                else:
                    c += 1
                if currentError < bestError:
                    bestError = currentError
                    bestPrices = p
    return D.allocation(bestPrices)

if __name__ == '__main__':
    choreographers = ['c'+str(i) for i in range(20)]
    dancers = ['d'+str(i) for i in range(200)]
    utilities = [[random.uniform(0,1) for _ in choreographers] for _ in dancers]
    caps = [1,2,3]
    dancer_cap = [random.choice(caps) for _ in dancers]
    conflicts = []
    choreo_cap = [20] * len(choreographers)
    allocations = main(choreographers, dancers, utilities, dancer_cap, conflicts, choreo_cap)
    df = pd.DataFrame(allocations, index=dancers, columns=choreographers)
    df.to_csv('allocation.csv',index=True,header=True,sep=',')
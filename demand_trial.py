from demand_gurobi import *
import random
import time
import numpy as np

def test():
    choreographers = ['c'+str(i) for i in range(20)]
    dancers = ['d'+str(i) for i in range(200)]
    utilities = [[random.uniform(0,1) for _ in choreographers] for _ in dancers]
    capacities = [random.randint(1,5) for _ in dancers]
    conflicts = [('c1','c2'),('c1','c5'),('c10','c7')]
    start = time.time()
    troupe = DemandGUROBI(choreographers, dancers, utilities, capacities, conflicts)
    print(time.time() - start)
    prices = {}
    start = time.time()
    for _ in range(1000):
        for c in choreographers:
            prices[c] = random.uniform(0,1)
        a = troupe.demand(prices)
    print(time.time() - start)

if __name__ == '__main__':
    test()
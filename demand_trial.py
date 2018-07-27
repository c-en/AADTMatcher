from demand_gurobi import *
import random
import time
import numpy as np

def test():
    HZchoreographers = ['c'+str(i) for i in range(10)]
    EBchoreographers = ['c'+str(i) for i in range(10,20)]
    choreographers = HZchoreographers + EBchoreographers
    dancers = ['d'+str(i) for i in range(200)]
    utilities = [{c: random.uniform(0,1) for c in HZchoreographers+EBchoreographers} for _ in dancers]
    HZcapacities = [random.randint(1,3) for _ in dancers]
    EBcapacities = [random.randint(1,3) for _ in dancers]
    conflicts = [('c1','c2'),('c1','c5'),('c10','c7')]
    start = time.time()
    troupe = DemandGUROBI(HZchoreographers, EBchoreographers, dancers, utilities, HZcapacities, EBcapacities, conflicts)
    print(time.time() - start)
    
    start = time.time()
    for _ in range(1):
        prices = np.random.uniform(0,100,len(choreographers))
        a = troupe.allocation(prices, choreographers)
        print a
    print(time.time() - start)

if __name__ == '__main__':
    test()
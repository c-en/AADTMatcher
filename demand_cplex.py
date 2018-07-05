import cplex
import random
import time


# given dances, price vec, utility vec, and budget, solve for individual demand
class DancerCPLEX:
    # list of choreographers, list of utilities, budget
    def __init__(self, choreographers, utility, budget, capacity):
        # initialize MIP
        self.prob = cplex.Cplex()
        self.prob.set_log_stream(None)
        self.prob.set_error_stream(None)
        self.prob.set_warning_stream(None)
        self.prob.set_results_stream(None)
        # set maximization problem
        self.prob.objective.set_sense(self.prob.objective.sense.maximize)
        # add variables and objective to MIP
        var_types = [self.prob.variables.type.binary for _ in choreographers]
        self.prob.variables.add(obj = utility, types=var_types, names = choreographers)
        # add constraints to MIP
        constraint_names = ['budget','capacity']
        budget_constraint = [range(len(choreographers)),[0.0 for _ in choreographers]]
        capacity_constraint = [range(len(choreographers)),[1.0 for _ in choreographers]]
        constraints = [budget_constraint,capacity_constraint]
        rhs = [float(budget), float(capacity)]
        constraint_senses = "LE"
        self.prob.linear_constraints.add(lin_expr=constraints,
                                         senses=constraint_senses,
                                         rhs=rhs,
                                         names=constraint_names)


    # give list of prices
    def demand(self, prices):
        constraints = [0 for _ in prices]
        variables = range(len(prices))
        self.prob.linear_constraints.set_coefficients(zip(constraints, variables, prices))
        self.prob.solve()
        return self.prob.solution.get_values()

def time_trial():
    print("CPLEX")
    start = time.time()
    lst = [DancerCPLEX(choreographers,[random.uniform(0,1) for _ in choreographers],100+random.uniform(0,1),random.randint(1,5)) for _ in range(200)]
    print(time.time()-start)
    start = time.time()
    for _ in range(100):
        prices = {}
        for c in choreographers:
            prices[c] = random.uniform(0,1)
        prices = [random.uniform(0,1) for _ in range(20)]
        for d in lst:
            d.demand(prices)
    print(time.time()-start)

if __name__ == '__main__':
    time_trial()
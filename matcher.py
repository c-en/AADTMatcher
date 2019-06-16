import numpy as np
import random
import csv
import conflicts as cf
import marketLinear
import aceei
import os

ranks = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth']

def test_random():
    # choreographers: list of names
    choreographers = ['c'+str(i) for i in range(20)]
    # dancers: list of names
    dancers = ['d'+str(i) for i in range(200)]
    # values: dancers x choreographers matrix
    values = [[random.uniform(0,1) for _ in choreographers] for _ in dancers]
    caps = [1,2,3]
    # list of dancer capacities
    capacities = [random.choice(caps) for _ in dancers]
    # list of tuples for conflicts
    # complements: complements array for dancers (reflecting schedule conflicts)
    comps = np.zeros((len(choreographers), len(choreographers)))
    for row in comps:
        for col in comps:
            if col > row and random.uniform(0,1) > 0.95:
                comps[row][col] = -100
    # choreographer capacities - arrays for min and max capacities
    choreo_min = np.array([15] * len(choreographers))
    choreo_max = np.array([25] * len(choreographers))
    choreo_avail = [choreo_min, choreo_max]
    allocations = tabu.tabu(HZchoreographers, EBchoreographers, dancers, utilities, HZdancer_cap, EBdancer_cap, conflicts, choreo_min, choreo_max)
    Market = marketLinear.MarketLinear(choreographers, dancers, values, complements, capacities)
    aceei.tabu(dancers, choreographers, choreo_avail, Market)


def main():
    choreographers = []
    choreo_min = []
    choreo_max = []
    c_for_title = {}
    conflicts = cf.scheduleConflicts('schedule.csv')
    # read in dance schedule/information
    with open('schedule.csv', 'r') as f:
        schreader = csv.DictReader(f, delimiter=',')
        for row in schreader:
            choreographers.append(row['Choreographer'])
            choreo_min.append(int(row['MinCap']))
            choreo_max.append(int(row['MaxCap']))
    c_idx = {c:i for i, c in enumerate(choreographers)}
    complements = np.zeros((len(choreographers), len(choreographers)))
    for conflict in conflicts:
        complements[min(c_idx[conflict[0]], c_idx[conflict[1]])][max(c_idx[conflict[0]], c_idx[conflict[1]])] = -1000.
        # complements[c_idx[conflict[1]]][c_idx[conflict[0]]] = -1000.
    # read in dancer preferences, assign utility values arbitrarity
    # NOTE: this only supports ranking up to 6 dances; utility values are set as 10-(rank of dance)
    # - you may update the number of supported ranks at the top of this file, variable "ranks"
    with open("preferences.csv", 'r') as f:
        prefs = csv.DictReader(f)
        dancers = []
        dancerEmails = {}
        capacities = []
        utilities = []
        for dancer in prefs:
            dancers.append(dancer['Name'])
            capacities.append(int(dancer['How many dances do you want to join?']))
            dancerEmails[dancer['Name']] = dancer['Email Address']
            dancer_utility = [0.] * len(choreographers)
            for i, rank in enumerate(ranks):
                c = dancer['Please select your '+ rank +' choice dance.'].split(' (')[0]
                if not c == 'N/A':
                    dancer_utility[c_idx[c]] = 9.-i
            utilities.append(dancer_utility)
    print "TOTAL DEMAND: " + str(sum(capacities))
    print "TOTAL CAPACITY"
    print choreo_min
    print sum(choreo_min)
    print choreo_max
    print sum(choreo_max)
    # randomize dancer priority, and de/prioritize marked dancers
    with open("priority.csv", 'r') as f:
        prio = set()
        for row in f:
            a = row.replace("\r\n", "")
            prio.add(a)
    with open("depriority.csv", 'r') as f:
        deprio = set()
        for row in f:
            a = row.replace("\r\n", "")
            deprio.add(a)
    lottery = np.random.uniform(0,1,len(dancers))
    for i, dancer in enumerate(dancers):
        if dancerEmails[dancer] in deprio:
            lottery[i] -= 1
        elif dancerEmails[dancer] in prio:
            lottery[i] += 1
    info = zip(lottery, dancers, capacities, utilities)
    info.sort()
    _, dancers, capacities, utilities = zip(*info)
    # run A-CEEI to find optimal allocations of dancers to dances
    Market = marketLinear.MarketLinear(dancers, choreographers, capacities, utilities, [complements]*len(dancers))
    allocation, times, besterrors = aceei.tabu(dancers, choreographers, (choreo_min, choreo_max), Market)
    # save final allocation matrix to file
    np.savetxt('allocations.csv', allocation, delimiter=',')
    # organize by dance and output to files
    try:
        os.mkdir('rosters')
    except:
        pass
    rosters = {c:[] for c in choreographers}
    assignments = {d:[] for d in dancers}
    for d in range(len(allocation)):
        for c in range(len(allocation[d])):
            if allocation[d][c]==1:
                rosters[choreographers[c]].append(dancers[d])
                assignments[dancers[d]].append(choreographers[c])
    for c in rosters:
        with open('rosters/'+c+'.csv', 'w+') as f:
            f.write(c+'\n')
            for d in rosters[c]:
                f.write(d + ',' + dancerEmails[d]+ '\n')
    with open("assignments.csv", 'w+') as f:
        for d in dancers:
            f.write(d + ',' + ','.join(assignments[d]) + "\n")

if __name__ == "__main__":
   main()
import numpy as np
import random
import csv
import conflicts as cf
import tabu
import os

def test_random():
    # choreographers: list of names
    HZchoreographers = ['c'+str(i) for i in range(10)]
    EBchoreographers = ['c'+str(i) for i in range(10,20)]
    choreographers = HZchoreographers + EBchoreographers
    # dancers: list of names
    dancers = ['d'+str(i) for i in range(200)]
    # utilities: dancers x choreographers matrix
    utilities = [{c: random.uniform(0,1) for c in choreographers} for _ in dancers]
    caps = [1,2,3]
    # list of dancer capacities
    HZdancer_cap = [random.choice(caps) for _ in dancers]
    EBdancer_cap = [random.choice(caps) for _ in dancers]
    # list of tuples for conflicts
    conflicts = []
    # choreographer capacities - arrays for min and max capacities
    choreo_min = np.array([15] * len(choreographers))
    choreo_max = np.array([25] * len(choreographers))
    allocations = tabu.tabu(HZchoreographers, EBchoreographers, dancers, utilities, HZdancer_cap, EBdancer_cap, conflicts, choreo_min, choreo_max)
    np.savetxt('allocation_test.csv', allocations, delimiter=',')

def main():
    HZchoreographers = []
    HZchoreo_min = []
    HZchoreo_max = []
    EBchoreographers = []
    EBchoreo_min = []
    EBchoreo_max = []
    conflicts = cf.scheduleConflicts('schedule.csv')
    # read in dance schedule/information
    with open('schedule.csv', 'r') as f:
        schreader = csv.reader(f, delimiter=',')
        next(schreader)
        for row in schreader:
            if row[1] == "H":
                HZchoreographers.append(row[0])
                HZchoreo_min.append(int(row[5]))
                HZchoreo_max.append(int(row[6]))
            else:
                EBchoreographers.append(row[0])
                EBchoreo_min.append(int(row[5]))
                EBchoreo_max.append(int(row[6]))
    choreo_min = HZchoreo_min + EBchoreo_min
    choreo_max = HZchoreo_max + EBchoreo_max
    choreographers = HZchoreographers + EBchoreographers
    # read in dancer preferences
    with open("preferences.csv", 'r') as f:
        prefs = csv.DictReader(f)
        dancers = []
        dancerEmails = {}
        HZcapacities = []
        EBcapacities = []
        utilities = []
        for dancer in prefs:
            for key in dancer:
                if key[-8:] == "'s dance":
                    dancer[key[:-8]] = dancer.pop(key)
            dancers.append(dancer['Name'])
            HZcapacities.append(int(dancer['How many Horizon dances do you want to join?']))
            EBcapacities.append(int(dancer['How many Eastbound dances do you want to join?']))
            dancerEmails[dancer['Name']] = dancer['Email Address']
            utilities.append({c: int(dancer[c]) for c in choreographers})
    print "TOTAL DEMAND"
    print "HORIZON: " + str(sum(HZcapacities))
    print "EASTBOUND: "+ str(sum(EBcapacities))
    print "TOTAL CAPACITY"
    print choreo_min
    print choreo_max
    # find optimal allocation of dancers to dances
    allocations = tabu.tabu(HZchoreographers, EBchoreographers, dancers, utilities, 
                                HZcapacities, EBcapacities, conflicts, choreo_min, choreo_max)
    # save final allocation matrix to file
    np.savetxt('allocations.csv', allocations, delimiter=',')
    # organize by dance and output to files
    try:
        os.mkdir('rosters')
    except:
        pass
    rosters = {c:[] for c in choreographers}
    for d in range(len(allocations)):
        for c in range(len(allocations[d])):
            if allocations[d][c]==1:
                rosters[choreographers[c]].append(dancers[d])
    for c in rosters:
        with open('rosters/'+c+'.csv', 'w+') as f:
            f.write(c+'\n')
            for d in rosters[c]:
                f.write(d + ',' + dancerEmails[d]+ '\n')

if __name__ == "__main__":
    main()

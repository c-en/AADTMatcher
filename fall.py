# import numpy as np
import csv
import conflicts as cf
# import tabu

def test_random():
    # choreographers: list of names
    choreographers = ['c'+str(i) for i in range(20)]
    # dancers: list of names
    dancers = ['d'+str(i) for i in range(200)]
    # utilities: dancers x choreographers matrix
    utilities = [[random.uniform(0,1) for _ in choreographers] for _ in dancers]
    caps = [1,2,3]
    # list of dancer capacities
    dancer_cap = [random.choice(caps) for _ in dancers]
    # list of tuples for conflicts
    conflicts = []
    # choreographer capacities - arrays for min and max capacities
    choreo_min = np.array([15] * len(choreographers))
    choreo_max = np.array([25] * len(choreographers))
    allocations = tabu.tabu(choreographers, dancers, utilities, dancer_cap, conflicts, choreo_min, choreo_max)
    np.savetxt('allocation_test.csv', allocations, delimiter=',')

# First, allocate for HORIZON
# Then, make new demand/dancer objects for EASTBOUND
# - For each dancers, set EASTBOUND utilities to -infty if conflict w/ assigned HORIZON dance
def main():
    HZchoreographers = []
    HZchoreo_min = []
    HZchoreo_max = []
    EBchoreographers = []
    EBchoreo_min = []
    EBchoreo_max = []
    HZconflicts, EBconflicts, crossConflicts = cf.scheduleConflicts('fall_schedule.csv')
    with open('fall_schedule.csv', 'r') as f:
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
    with open("fall_dance_preferences.csv", 'r') as f:
        # prefs = [{k: int(v) if v.isdigit() else v for k, v in row.items()} 
        #         for row in csv.DictReader(f, skipinitialspace=True)]
        prefs = csv.DictReader(f)
        dancers = []
        HZdancerCap = []
        HZdancerUtil = []
        EBdancerCap = []
        EBdancerUtil = []
        for dancer in prefs:
            dancers.append(dancer['Name'])
            HZdancerCap.append(dancer['How many Horizon dances?'])
            HZdancerUtil.append([int(dancer[c]) for c in HZchoreographers])
            EBdancerCap.append(dancer['How many Eastbound dances?'])
            EBdancerUtil.append([int(dancer[c]) for c in EBchoreographers])
    HZallocations = tabu.tabu(HZchoreographers, dancers, HZdancerUtil, 
                                HZdancerCap, HZconflicts, HZchoreo_min, HZchoreo_max)
    np.savetxt('HZallocations.csv', HZallocations, delimiter=',')
    EBchoreoIndex = {c: i for i, c in enumerate(EBchoreographers)}
    for i in range(len(dancers)):
        for j in range(len(HZallocations[i])):
            if HZallocations[i][j] == 1:
                for conflictChoreo in crossConflicts[EBchoreographers[j]]:
                    EBdancerUtil[i][EBchoreoIndex[conflictChoreo]] = -float('inf')
    # finally, calc EB allocations
    EBallocations = tabu.tabu(EBchoreographers, dancers, EBdancerUtil, 
                                EBdancerCap, EBconflicts, EBchoreo_min, EBchoreo_max)
    np.savetxt('EBallocations.csv', EBallocations, delimiter=',')




main()

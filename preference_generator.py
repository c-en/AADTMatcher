import csv
import random

def gen_d():
    # choreographers: list of names
    HZchoreographers = ['HC'+str(i) for i in range(10)]
    EBchoreographers = ['EC'+str(i) for i in range(10)]
    # dancers: list of names
    dancers = ['D'+str(i) for i in range(200)]
    # utilities: dancers x choreographers matrix
    ut = list(range(11))
    HZutilities = [{c: random.choice(ut) for c in HZchoreographers} for _ in dancers]
    EButilities = [{c: random.choice(ut) for c in EBchoreographers} for _ in dancers]
    caps = [0,1,2]
    # list of dancer capacities
    HZdancer_cap = [random.choice(caps) for _ in dancers]
    EBdancer_cap = [random.choice(caps) for _ in dancers]
    with open('preferences.csv', 'w+') as f:
        prefwriter = csv.writer(f, delimiter=',')
        header = ['Name', 'Email Address','How many Horizon dances do you want to join?'] + [c + "'s dance" for c in HZchoreographers] + ['How many Eastbound dances do you want to join?'] + [c + "'s dance" for c in EBchoreographers]
        prefwriter.writerow(header)
        for i, dancer in enumerate(dancers):
            row = [dancer, dancer+'@college.harvard.edu', HZdancer_cap[i]] + [HZutilities[i][c] for c in HZchoreographers] + [EBdancer_cap[i]] + [HZutilities[i][c] for c in HZchoreographers]
            prefwriter.writerow(row)
    # choreographer capacities - arrays for min and max capacities
    # choreo_min = np.array([15] * len(choreographers))
    # choreo_max = np.array([25] * len(choreographers))
    # np.savetxt('allocation_test.csv', allocations, delimiter=',')

def gen_c():
    HZchoreographers = ['HC'+str(i) for i in range(10)]
    EBchoreographers = ['EC'+str(i) for i in range(10)]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    start = ['1800', '1830', '1900', '1930', '2000', '2030', '2100', '2130', '2200', '2230', '2300']
    add = [100,200]
    capacities = list(range(10,20))
    with open('schedule.csv', 'w+') as f:
        scwriter = csv.writer(f, delimiter = ',')
        scwriter.writerow(["Choreographer", "Show", "Day", "Start", "End", "MinCap", "MaxCap"])
        for c in HZchoreographers:
            l = random.choice(capacities)
            h = l + 10
            s = random.choice(start)
            row = [c, "H", random.choice(days), s, str(int(s)+random.choice(add)), str(l), str(h)]
            scwriter.writerow(row)
        for c in EBchoreographers:
            l = random.choice(capacities)
            h = l + 10
            s = random.choice(start)
            row = [c, "E", random.choice(days), s, str(int(s)+random.choice(add)), str(l), str(h)]
            scwriter.writerow(row)

gen_d()
gen_c()
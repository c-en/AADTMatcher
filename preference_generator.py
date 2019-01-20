import csv
import random

def gen_d():
    # choreographers: list of names
    choreographers = ['c' +str(i) for i in range(20)]
    # dancers: list of names
    dancers = ['D'+str(i) for i in range(200)]
    # list of dancer capacities
    caps = [1,2,3]
    capacities = [random.choice(caps) for _ in dancers]
    # ranks: top cap+2 choreographers for each dancer
    ranks = []
    for i in range(len(dancers)):
        r = choreographers
        random.shuffle(r)
        r = r[:(capacities[i]+2)]
        while len(r) < 6:
            r.append('N/A')
        ranks.append(r)
    with open('preferences.csv', 'w+') as f:
        places = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth']
        prefwriter = csv.writer(f, delimiter=',')
        header = ['Name', 'Email Address','How many dances do you want to join?'] + ['Please select your '+ place +' choice dance.' for place in places] 
        prefwriter.writerow(header)
        for i, dancer in enumerate(dancers):
            row = [dancer, dancer+'@college.harvard.edu', capacities[i]] + ranks[i]
            prefwriter.writerow(row)
    # choreographer capacities - arrays for min and max capacities
    # choreo_min = np.array([15] * len(choreographers))
    # choreo_max = np.array([25] * len(choreographers))
    # np.savetxt('allocation_test.csv', allocations, delimiter=',')

def gen_c():
    choreographers = ['c'+str(i) for i in range(20)]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    start = ['1800', '1830', '1900', '1930', '2000', '2030', '2100', '2130', '2200', '2230', '2300']
    add = [200]
    capacities = list(range(10,20))
    with open('schedule.csv', 'w+') as f:
        scwriter = csv.writer(f, delimiter = ',')
        scwriter.writerow(["Choreographer", "Day", "Start", "End", "MinCap", "MaxCap"])
        for c in choreographers:
            l = random.choice(capacities)
            h = l + 10
            s = random.choice(start)
            row = [c, random.choice(days), s, str(int(s)+random.choice(add)), str(l), str(h)]
            scwriter.writerow(row)

if __name__ == "__main__":
    gen_d()
    gen_c()
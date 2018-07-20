import csv

def scheduleConflicts(schFile):
    conflicts = []
    dances = {'Sunday': [], 'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': []}
    with open(schFile, 'r') as f:
        schreader = csv.reader(f, delimiter=',')
        next(schreader)
        for row in schreader:
            day = row[2]
            dance = {'c':row[0], 'show': row[1], 'start': int(row[3]), 'end': int(row[4])}
            for otherDance in dances[day]:
                lastStart = max(dance['start'], otherDance['start'])
                firstEnd = min(dance['end'], otherDance['end'])
                # if there's overlap, add to conflicts
                if firstEnd - lastStart > 0:
                    conflicts.append((dance['c'], otherDance['c']))
            dances[day].append(dance)
    return conflicts
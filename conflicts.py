import csv

def scheduleConflicts(schFile):
    conflicts = []
    dances = {'Sunday': [], 'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': []}
    with open(schFile, 'r') as f:
        schreader = csv.DictReader(f, delimiter=',')
        next(schreader)
        for row in schreader:
            day = row['Day']
            dance = {'c':row['Choreographer'], 'start': int(row['Start']), 'end': int(row['End'])}
            for otherDance in dances[day]:
                lastStart = max(dance['start'], otherDance['start'])
                firstEnd = min(dance['end'], otherDance['end'])
                # if there's overlap, add to conflicts
                if firstEnd - lastStart > 0:
                    conflicts.append((dance['c'], otherDance['c']))
            dances[day].append(dance)
    return conflicts
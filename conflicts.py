import csv

def scheduleConflicts(schFile):
    HZconflicts = []
    EBconflicts = []
    crossConflicts = {}
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
                    # cross-conflicts
                    if not dance['show'] == otherDance['show']:
                        if dance['show'] == 'H':
                            try:
                                crossConflicts[dance['c']].append(otherDance['c'])
                            except KeyError:
                                crossConflicts[otherDance['c']].append(dance['c'])
                        else:
                            try:
                                crossConflicts[otherDance['c']].append(dance['c'])
                            except KeyError:
                                crossConflicts[dance['c']].append(otherDance['c'])
                    # HZ or EB conflicts
                    elif dance['show'] == 'H':
                        HZconflicts.append((dance['c'], otherDance['c']))
                    else:
                        EBconflicts.append((dance['c'], otherDance['c']))
            dances[day].append(dance)
    # crossConflicts: H dance is key, list of cross-conflicts is val
    return HZconflicts, EBconflicts, crossConflicts
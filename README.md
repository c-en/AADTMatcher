# AADTMatcher
A dance assignment system for Harvard Asian American Dance Troupe, using an approximate competitive equilibrium from equal incomes ([A-CEEI](http://faculty.chicagobooth.edu/eric.budish/research/CourseMatch.pdf)). Created by Chris En, Secretary '18-'19.
___

## Requirements
AADTMatcher runs on Python2, although it may be compatible with Python3 (I haven't checked - it would probably require minor code adjustments). You must have **Gurobi** for Python2. To get it, [sign up](http://www.gurobi.com/registration/download-reg) for an academic license, then follow the download and install instructions.
___

## Operating Instructions
1. Create the Dance Preferences Google Form for the troupe to fill out. Use [this template](https://drive.google.com/open?id=1q_T8xYxndKK6aVQJ4TMPpFCGnrqIDiPpJclJOwYnMPo) *exactly*; changing the format of questions or question titles will likely break the Matcher. Export and save the results spreadsheet as `preferences.csv`.

2. Update the file `schedule.csv` with the semester's rehearsal information. Each row is for one dance, with columns as follows:
  * Choreographer: the name of the choreographer
  * Show: H or E, for Horizon or Eastbound
  * Day: the day of the week of the rehearsal
  * Start: the start time of the rehearsal, in military time (e.g. 1800 for 6:00pm)
  * End: the end time of the rehearsal, in military time
  * MaxCap: the maximum number of dancers that can be assigned to this dance
  * MinCap: the minimum number of dancers that can be assigned to this dance (soft cap)

3. Run the Matcher from the terminal (Mac or Linux - no Windows, please) with `python2 matcher.py`. 

   With the default settings, this can take up to 8 hours or more on a single machine. To change the amount of time spent per machine, change `maxTime` in `tabu.py` to the maximum time spent calculating (in seconds).

   Because the algorithm is randomized, the more time spent, the more likely it is to find a better solution. As such, it is **highly encouraged** to run the Matcher independently on multiple machines, and select the best result (as determined by the smallest `clearing_error`, which is printed in the terminal once the Matcher has finished).

4. The best allocation found will be exported as a matrix to `allocations.csv`. Each dance's roster and emails will be exported to the folder `rosters/` in the file `[choreographer_name].csv`.
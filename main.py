import sys
from tabulate import tabulate
from schedular import *
import matplotlib.pyplot as plt

filename = sys.argv[1]
f = open(filename, "r")
lines = f.readlines()
f.close()

#algorithm name (HPF, FCFS, RR, SRTN)
algo = str.upper(sys.argv[2])
context_time = int(sys.argv[3])
quantum = 0
if(algo == "RR"):
    quantum = int(sys.argv[4])

n = int(lines[0])
procs = []
for i in range(n):
    params = {}
    line = lines[i+1].split()
    params['num'] = int(line[0])
    params['arrival'] = int(line[1])
    params['burst'] = int(line[2])
    params['priority'] = int(line[3])
    procs.append(params)

procs.sort(key=lambda params: params['arrival'])

if(algo == "FCFS"):
    procs, y = FCFS(procs, context_time)
elif(algo == "RR"):
    procs, y = RR(procs, context_time, quantum)
elif (algo == "HPF"):
    procs, y  = HPF(procs, context_time)
elif (algo == "SRTN"):
    procs, y = SRTN(procs, context_time)
else:
    print("The entered algorithm is unknown")
    exit(-1)

procs.sort(key=lambda params: params['num'])

columns = ["process number", "Waiting-time", "Turnaround-time", "Weighted-Turnaround-time"]
rows = []
turnSum = 0
wTurnSum = 0
for proc in procs:
    info = list(range(4))
    info[0] = proc['num']
    turn = info[2] = proc['end'] - proc['arrival']    #turnaround time
    wturn = info[3] = turn/proc['burst']  #weighted turnaround time
    info[1] = turn - proc['burst'] #waiting time
    rows.append(info)
    turnSum += turn
    wTurnSum += wturn

avgTurn = turnSum/len(procs)
avgwTurn = wTurnSum/len(procs)

output_filename = filename.split('.')[0] + "_" + algo + "_metrics" + ".txt"
of = open(output_filename, "w")
of.write(tabulate(rows, columns))
of.write('\n' + "Average turnaround time: " + str(avgTurn) + '\n') 
of.write("Average weighted turnaround time: " + str(avgwTurn) + '\n')
of.close()

t = np.arange(len(y))
plt.step(t, y, where='pre', label = 'processing')
plt.xticks(t)
plt.yticks(np.arange(n+1))
plt.grid(True)
plt.plot(list(proc['arrival'] for proc in procs), np.arange(1, n+1), 'bo', label = 'arrival')
plt.plot(list(proc['end'] for proc in procs), np.arange(1, n+1), 'ro', label = 'finish')
plt.legend()
plt.xlabel("time")
plt.ylabel("process")
plt.show()
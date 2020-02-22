import sys
import numpy as np


inputfile = sys.argv[1]

fi = open(inputfile, "r")
lines = fi.readlines()

n = int(lines[0])
arrivalparameters = list(map(float, lines[1].split()))
burstparameters = list(map(float, lines[2].split()))
priorityparameters = list(map(float, lines[3].split()))

arrival = np.random.normal(arrivalparameters[0], arrivalparameters[1], n)
burst = np.random.normal(burstparameters[0], burstparameters[1], n)
priority = np.random.poisson(priorityparameters[0], n)

outputfile = sys.argv[2]
f = open(outputfile, "w")

f.write(str(n)+"\n")

for i in range(n):
	f.write(" ".join(map(str, [int(i+1), int(round(abs(arrival[i]))), int(round(abs(burst[i]))), abs(priority[i])]))+"\n")

f.close()
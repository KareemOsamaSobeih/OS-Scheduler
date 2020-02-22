import numpy as np
from heapq import heappush, heappop

def FCFS(processes, contextswitch):
	time = 0
	come = 0
	finish = 0
	n = len(processes)
	q = []
	ret = []
	t = []
	while(finish < n):
		t.append(0)
		if len(q) > 0:
			q[0]["running"] -= 1
			t[len(t)-1] = q[0]["num"]
			if q[0]["running"] == 0: 
				q[0]["end"] = time
				ret.append(q[0])
				finish += 1
				q = q[1:len(q)]
				time += contextswitch
				for i in range(contextswitch):
					t.append(0)
		while(come < n and processes[come]["arrival"] <= time):
			q.append(processes[come])
			q[len(q)-1]["running"] = q[len(q)-1]["burst"]
			come += 1
		time += 1
	return ret, t

def RR(processes, contextswitch, quantum):
	time = 0
	come = 0
	finish = 0
	n = len(processes)
	q = []
	ret = []
	qu = quantum
	t = []
	while(finish < n):
		while(come < n and processes[come]["arrival"] <= time):
			q.append(processes[come])
			q[len(q)-1]["running"] = q[len(q)-1]["burst"]
			come += 1
		t.append(0)
		if len(q) > 0 and q[0]["arrival"] < time:
			q[0]["running"] -= 1
			qu -= 1
			t[len(t)-1] = q[0]["num"]
			if q[0]["running"] == 0: 
				q[0]["end"] = time
				ret.append(q[0])
				qu = quantum
				finish += 1
				q = q[1:len(q)]
				time += contextswitch
				for i in range(contextswitch):
					t.append(0)
			if (qu == 0 and len(q) > 0): 
				qu = quantum
				if(len(q) > 1):
					q.append(q[0])
					q = q[1:len(q)]
					time += contextswitch
					for i in range(contextswitch):
						t.append(0)
		time += 1
	return ret, t

def HPF(procs, contx):
	hp = []
	time = 0
	n = len(procs)
	cnt = 0
	y = [0]
	while (cnt < n or len(hp) > 0):
		if len(hp) > 0:
			p = heappop(hp)[2]
			burst = procs[p]['burst']
			y.extend((burst)*[procs[p]['num']])
			time += burst
			procs[p]['end'] = time
			y.extend((contx)*[0])
			time += contx
			
		if (cnt < n and procs[cnt]['arrival'] > time):
			ntime = procs[cnt]['arrival']
			y.extend((ntime - time) * [0])
			time = ntime
			
		while (cnt < n and procs[cnt]['arrival'] <= time):
			heappush(hp, (-procs[cnt]['priority'], procs[cnt]['num'], cnt))
			cnt += 1
	return procs, y


def SRTN(procs, contx):
	cnt = 0
	n = len(procs)
	time = 0
	hp = []
	finish = 0
	last = -1
	y = [0]
	while finish < n:
		while cnt < n and procs[cnt]['arrival'] <= time :
			heappush(hp, [procs[cnt]['burst'], procs[cnt]['num'], cnt])
			cnt += 1
		time += 1
		y.append(0)
		if (len(hp) > 0):
			if (last != -1 and hp[0][2] != last):
				y.extend((contx)*[0])
				time += contx
			y[time] = procs[hp[0][2]]['num']
			last = hp[0][2]
			hp[0][0] -= 1
			if(hp[0][0] == 0):
				p = heappop(hp)[2]
				procs[p]['end'] = time
				finish += 1
	return procs, y
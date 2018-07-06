import basicfunctions as b
import matplotlib.pyplot as plt
import math
from tabulate import tabulate

methods = ['spec']

#functions = [x**4, ln(1+x), sqrt(x), sin(x)^2, e^(-x)-e^(-x)*(1+x) (needs init of 1)]

results = {}

max_steps = 500
t_step = 0.1

time = []

for i in methods:
    step = 0
    signal = 0
    signal_array = []

    position_array = []
    position_init = 0
    position_val = 0
    
    time = []
    while step <= max_steps:
        #time.append(t_step*step)
        if step == 3:
            t_step = t_step*2
        if step == 0:
            position_val = position_init
            position_array.append(position_val)
            t_step = t_step/2
            time.append(0)
            signal_array.append(signal)
        else:
            time.append(time[-1]+t_step)
            #signal = math.exp(-time[-1])-math.exp(-1*time[-1])*(1+time[-1])
            #signal = math.sin(time[-1])**2
            #signal = math.sqrt(time[-1])
            #signal = math.log1p(time[-1])
            signal = (time[-1])**4
            signal_array.append(signal)
            position_val = b.time_vary_integrate(step, t_step, signal_array, position_val, i, position_init)
            position_array.append(position_val)
        
        step+=1
    results[i] = position_array

actual = []

for t in time:
    #val = (t-(math.sin(2*t)/2))/2#(-1*math.sin(2*t)-2*t)/4
    #val = (t+1)*math.exp(-1*t)
    #val = (2*t**(3/2))/3
    #val = (t+1)*(math.log1p(t))-t
    val = t**5/5
    actual.append(val)

avg_error = []

errors = []

for i in results.values():
    error = [abs(k - j) for k, j in zip(i, actual)]
    errors.append(error)
    avg_error.append(sum(error))

print(list(zip(results.keys(), avg_error)))

#print(tabulate(zip(time, signal_array, results['spec'], actual, errors[0]), headers=['Time', 'signal', 'integrate()', 'actual', 'error']))

plt.plot(time, errors[0], 'r')#, time, errors[1], 'g', time, errors[2], 'k', time, errors[3], 'c', time, errors[4], 'y'
plt.show()

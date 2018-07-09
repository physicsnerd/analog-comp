from analogpack import basicfunctions as b
import matplotlib.pyplot as plt
import math
from tabulate import tabulate

methods = ['trap', 'simp38','timevary']

#functions = [x**4, ln(1+x), sqrt(x), sin(x)^2, e^(-x)-e^(-x)*(1+x) (needs init of 1)]

results = {}

max_steps = 500
t_step = 0.1

times = {}

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
        if step == 0:
            position_val = position_init
            position_array.append(position_val)
            time.append(0)
            signal_array.append(signal)
        else:
            time = b.time_handle(step, t_step, time, i)
            #signal = math.exp(-time[-1])-math.exp(-1*time[-1])*(1+time[-1])
            #signal = math.sin(time[-1])**2
            #signal = math.sqrt(time[-1])
            #signal = math.log1p(time[-1])
            signal = (time[-1])**4
            signal_array.append(signal)
            #print(signal_array, position_val)
            position_val = b.integrate(step, t_step, signal_array, position_val, i, position_init)
            position_array.append(position_val)
        
        step+=1
    results[i] = position_array
    times[i] = time
actual = []
actuals = {}

for i in times:
    for t in times[i]:
        #val = (t-(math.sin(2*t)/2))/2#(-1*math.sin(2*t)-2*t)/4
        #val = (t+1)*math.exp(-1*t)
        #val = (2*t**(3/2))/3
        #val = (t+1)*(math.log1p(t))-t
        val = t**5/5
        actual.append(val)
    actuals[i] = actual

avg_error = []

errors = []

for i in results:
    error = [abs(k - j) for k, j in zip(results[i], actuals[i])]
    errors.append(error)
    avg_error.append(sum(error))

print(list(zip(results.keys(), avg_error)))

#print(tabulate(zip(time, signal_array, results['trap'], actual, errors[0]), headers=['Time', 'signal', 'integrate()', 'actual', 'error']))

plt.plot(times['trap'], errors[0], 'r', times['simp38'], errors[1], 'g', times['timevary'], errors[2], 'k')#, time, errors[3], 'c', time, errors[4], 'y')
plt.show()

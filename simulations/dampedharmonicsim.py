import matplotlib.pyplot as plt
import math
from tabulate import tabulate
from analogpack import basicfunctions as b

k = 78.125
m = 78.125
c = 7
omega = b.sqroot(b.divide(k, m))
zeta = b.divide(c, b.multiply(2, b.sqroot(b.multiply(m,k))))


#omega = 1
#zeta = 1

#methods = ['trap','simp','simp38','boole','5th']
methods = ['simp38']

results = {}

max_steps = 10000
t_step = .01

times = {}
time = []

for i in methods:
    step = 0
    signal = 0
    signal_array = []

    position_array = []
    velocity_array = []

    position_init = 1
    velocity_init = 0

    position_val = 0
    velocity_val = 0
    time = []
    while step <= max_steps:
        #time.append(t_step*step)
        #if step == 3:
           # t_step = t_step*2
        if step == 0:
            velocity_val = velocity_init
            position_val = position_init
            
            position_array.append(position_val)
            velocity_array.append(velocity_val)

            signal = b.subtract(b.multiply(-2,omega,zeta,velocity_val), b.multiply(b.square(omega),position_val))
            signal_array.append(signal)

            #t_step = t_step/2
            time.append(0)
        elif step == 1:
            #time.append(time[-1]+t_step)
            
            position_val = .999988
            velocity_val = -.00499898
            
            signal = b.subtract(b.multiply(-2,omega,zeta,velocity_val), b.multiply(b.square(omega),position_val))
            signal_array.append(signal)
            
            integrate_result_vel = b.integrate(step, t_step, signal_array, velocity_val, i, velocity_init, time)
            velocity_val = integrate_result_vel[0]
            time = integrate_result_vel[1]
            velocity_array.append(velocity_val)
            
            integrate_result_pos = b.integrate(step, t_step, velocity_array, position_val, i, position_init, time)
            position_val = integrate_result_pos[0]
            time = integrate_result_vel[1]
            position_array.append(position_val)
        else:
            #time.append(time[-1]+t_step)
            
            signal = b.subtract(b.multiply(-2,omega,zeta,velocity_val), b.multiply(b.square(omega),position_val))
            signal_array.append(signal)
            
            integrate_result_vel = b.integrate(step, t_step, signal_array, velocity_val, i, velocity_init, time)
            velocity_val = integrate_result_vel[0]
            time = integrate_result_vel[1]
            velocity_array.append(velocity_val)
            
            integrate_result_pos = b.integrate(step, t_step, velocity_array, position_val, i, position_init, time)
            position_val = integrate_result_pos[0]
            time = integrate_result_pos[1]
            position_array.append(position_val)
            
        step+=1
    results[i] = position_array
    times[i] = time

actual = []

for i in times:
    for t in times[i]:
        inval = math.cos((4*math.sqrt(39)*t)/25)
        inval2 = math.sin((4*math.sqrt(39)*t)/25)
        val = math.exp(-1*t/25)/156*(156 * inval + math.sqrt(39) * inval2)
        actual.append(val)

avg_error = []

errors = []

for i in results.values():
    error = [abs(k - j) for k, j in zip(i, actual)]
    errors.append(error)
    avg_error.append(sum(error))#/len(error)

print(list(zip(results.keys(), avg_error)))

#print(tabulate(zip(time, signal_array, results['spec'], actual, errors[0]), headers=['Time', 'signal', 'integrate()', 'actual', 'error']))

plt.plot(times['simp38'], errors[0])#, time, errors[2], 'k', time, errors[3], 'c', time, errors[4], 'y'
plt.show()

import matplotlib.pyplot as plt
from decimal import Decimal

def simp_integrate(tt_step, new_val, integral_val):
    if step == 0:
        return tt_step * new_val
    elif step == max_steps:
        return (tt_step * new_val) + integral_val
    else:
        if step % 2 == 0:
            return (2 * tt_step * new_val) + integral_val
        else:
            return (4 * tt_step * new_val) + integral_val

def true_simp(t_step, new_val, integral_val):
    b_a = new_val[-1] - new_val[-2]
    return t_step/12 * (new_val[-2]**2 + 4*(new_val[-2] + b_a/4)**2 + 2*(new_val[-2] + 2*b_a/4)**2 + 4*(new_val[-2] + 3*b_a/4)**2 + new_val[-1]**2) + integral_val

def control(val,c):
    return float((Decimal(str(val))**Decimal(3))/Decimal(3))

def trap_integrate(t_step, val_array, integral_val):
    return (t_step/2)* (val_array[-1] + val_array[-2]) + integral_val

t_step = 1
tt_step = t_step/3
time = []

step = 0
max_steps = int(input('how many steps do you want it to go: '))
max_steps = max_steps

def trap_simp(step, t_step, new_val, integral_val):
    if step == 1:
        return (t_step/2) * (new_val[-2]**2 + new_val[-1]**2) + integral_val
    else:
        return (t_step/3) * (-.25 * (new_val[-3]**2) + 2 * (new_val[-2]**2) + 1.25 * (new_val[-1]**2)) + integral_val

x_array = []
signal_array = []
signal = 0

simp_integral = 0
simp_integral_array = []

simp_integral2 = 0
simp_integral_array2 = []

trap_integral = 0
trap_integral_array = []

trap_simp_integral = 0
trap_simp_array = []

while step <= max_steps:
    x = step*t_step
    signal = (step*t_step)**2
    x_array.append(x)
    signal_array.append(signal)
    time.append(step * t_step)
    if step >= 1:
        simp_integral = simp_integrate(tt_step, signal, simp_integral)
        trap_integral = trap_integrate(t_step, signal_array, trap_integral)
        simp_integral2 = true_simp(t_step, x_array, simp_integral2)
        trap_simp_integral = trap_simp(step, t_step, x_array, trap_simp_integral)
        
        simp_integral_array.append(simp_integral)
        trap_integral_array.append(trap_integral)
        simp_integral_array2.append(simp_integral2)
        trap_simp_array.append(trap_simp_integral)
    else:
        simp_integral_array.append(0)
        trap_integral_array.append(0)
        simp_integral_array2.append(0)
        trap_simp_array.append(0)
    step+=1

control_vals = []

for i in x_array:
    x = control(i, 0)
    control_vals.append(x)

error = []
error2 = []
error3 = []
error4 = []

error_sum = 0
error2_sum = 0
error3_sum = 0
error4_sum = 0

for i in control_vals:
    for k in simp_integral_array:
        error.append(k-i)
        error_sum+=(k-i)

for i in control_vals:
    for k in trap_integral_array:
        error2.append(k-i)
        error2_sum+=(k-i)

for i in control_vals:
    for k in simp_integral_array2:
        error3.append(k-i)
        error3_sum+=(k-i)

for i in control_vals:
    for k in trap_simp_array:
        error4.append(k-i)
        error4_sum+=(k-i)

for i in control_vals:
    if control_vals.index(i) % 25 == 0:
        print('control', i)

for i in trap_integral_array:
    if trap_integral_array.index(i) % 25 == 0:
        print('trap', i)

for i in simp_integral_array:
    if simp_integral_array.index(i) % 25 == 0:
        print('simp', i)

for i in simp_integral_array2:
    if simp_integral_array2.index(i) % 25 == 0:
        print('true simp', i)

for i in trap_simp_array:
    if trap_simp_array.index(i) % 25 == 0:
        print('trap simp', i)

print('avg error simpson', error_sum/len(error))
print('avg error trapezoidal', error2_sum/len(error))
print('avg error simpson2', error3_sum/len(error))
print('avg error trap simp', error4_sum/len(error))
plt.plot(time, control_vals, 'b', time, simp_integral_array2, 'r')
plt.show()

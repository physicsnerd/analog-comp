import matplotlib.pyplot as plt

step = 0
t_step = 10**(-3)

integral_val = 0
integral_array = []

signal_array = []
signal = -1

time = []

def integrate(step, t_step, new_val, integral_val, init_val):
    if step == 1:
        return t_step/2*(new_val[-2] + new_val[-1]) + init_val
    elif step == 2:
        return t_step/2*(new_val[-3] + 4ew_val[-2] + new_val[-1]) + integral_val
    else:
        return t_step/24*(new_val[-4] - 5*new_val[-3] + 19*new_val[-2] + 9*new_val[-1]) + integral_val

while step <= 4000:
    if step % 1000 == 0:
        signal *= -1
    signal_array.append(signal)
    time.append(step*t_step)
    if step >= 1:
        integral_val = integrate(step, t_step, signal_array, integral_val, 0)
        integral_array.append(integral_val)
    else:
        integral_array.append(0)
    step+=1

plt.plot(time, integral_array)
plt.show()

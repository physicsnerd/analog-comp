import basicfunctions as b
import matplotlib.pyplot as plt

mu = 1

signal = 0
signal_array = []

x_pos = 0
x_init = 3
x_array = []

v_pos = 0
v_init = 0
v_array = []

time = []
step = 0
t_step = .01
max_steps = 4000

method = 'simp38'

while step <= max_steps:
    time.append(t_step*step)

    if step == 0:
        v_pos = v_init
        x_pos = x_init

        x_array.append(x_pos)
        v_array.append(v_pos)

        signal_array.append(signal)
    else:
        signal = (mu*(1-x_pos**2))*v_pos + x_pos
        signal_array.append(signal)

        v_pos = b.integrate(step, t_step, signal_array, v_pos, method, v_init)
        v_array.append(v_pos)
        
        x_pos = b.integrate(step, t_step, v_array, x_pos, method, x_init)
        x_array.append(x_pos)

    step+=1

plt.plot(time, x_array)
plt.show()

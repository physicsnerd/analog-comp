import math
import matplotlib.pyplot as plt
from scipy import integrate

t_step = 10**(-3)
time = []

step = 0
max_steps = int(input('how many steps do you want it to go: '))

signal_array = []
signal = -1 #0 for sine/-1 for square

integral = []

while step <= max_steps:
    #signal = math.sin(math.pi*step*t_step + (math.pi/2))
    if step%1000 == 0:
        signal*=-1
    signal_array.append(signal)
    time.append(step * t_step)
    integral = integrate.cumtrapz(signal_array,dx=t_step,initial=0)
    step+=1

plt.plot(time, signal_array, 'r--', time, integral, 'bs')
plt.show()

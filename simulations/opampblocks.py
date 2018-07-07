import math
import matplotlib.pyplot as plt
import pigpio
import time as ti

#to run, beforehand, make sure sudo pigpiod has been run
pi = pigpio.pi()
pi.set_mode(27, pigpio.OUTPUT)
pi.set_PWM_frequency(27, 100)

def integrate(t_step, val_array, integral_val):
    return (t_step/2)* (val_array[-1] + val_array[-2]) + integral_val

def pwm_map(val, mini, maxi, pwm_res):
    scale_fac = (2**pwm_res)-1
    if mini < 0:
        x = val + (0 - mini)
        return round(x/(maxi-mini)*scale_fac)
    else:
        x = val - mini
        return round(x/(maxi-mini)*scale_fac)

t_step = 10**(-3)
tt_step = t_step/3
time = []

step = 0
max_steps = int(input('how many steps do you want it to go: '))
max_steps = max_steps

signal_array = []
signal = 0 #0 for sine/-1 for square

integral = 0
integral_array = []
integral2_array = []

def simp_integrate(tt_step, new_val, integral_val):
    if step == 0:
        return tt_step*new_val
    elif step == max_steps:
        return (tt_step * new_val) + integral_val
    else:
        if step % 2 == 0:
            return (2 * new_val *tt_step) + integral_val
        else:
            return (tt_step*4*new_val) + integral_val

while step <= max_steps:
    signal = math.sin(math.pi*step*t_step + (math.pi/2))
    #if step % 1000 == 0:
    #    signal*=-1
    signal_array.append(signal)
    time.append(step * t_step)
    if step >= 1:
        integral = simp_integrate(tt_step, signal, integral)
        integral2 = integrate(t_step, signal_array, integral)
        integral_array.append(integral)
        integral2_array.append(integral2)
        pi.set_PWM_dutycycle(27,pwm_map(integral,-.325,.325,8))
        #pi.set_PWM_dutycycle(27, pwm_map(integral, 0, 1,8))
        ti.sleep(.01)
    else:
        integral_array.append(0)
        integral2_array.append(0)
        pi.set_PWM_dutycycle(27,0)
    step+=1
plt.plot(time, integral_array, 'bs', time, integral2_array, 'r--')
plt.show()

pi.stop()

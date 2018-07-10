#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import sys
sys.path = ['/usr/lib/python35.zip', '/usr/lib/python3.5', '/usr/lib/python3.5/plat-arm-linux-gnueabihf', '/usr/lib/python3.5/lib-dynload', '/home/pi/.local/lib/python3.5/site-packages', '/usr/local/lib/python3.5/dist-packages', '/usr/local/lib/python3.5/dist-packages/RPIO-0.10.0-py3.5-linux-armv7l.egg', '/usr/local/lib/python3.5/dist-packages/analogpack-0.0-py3.5.egg', '/usr/lib/python3/dist-packages']

from analogpack import basicfunctions as b

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from MCP4922 import MCP4922
dac = MCP4922(spibus=0,spidevice=0,cs=8)

#fig = plt.figure()
#ax = Axes3D(fig)

signal_x = 0
signal_x_array = []

signal_y = 0
signal_y_array = []

signal_z = 0
signal_z_array = []

x_pos = 0
y_pos = 0
z_pos = 0

x_init = 1
y_init = 0
z_init = 2

x_pos_array = []
y_pos_array = []
z_pos_array = []

step = 0
t_step = .01
max_steps = 40000000
time = []

method = 'simp38'

while step <= max_steps:
    if step == 0:
        x_pos = x_init
        y_pos = y_init
        z_pos = z_init

        dac.setVoltage(1, b.pwm_map(x_pos, -25, 25, 12))
        dac.setVoltage(0, b.pwm_map(y_pos, -32, 32, 12))

        x_pos_array.append(x_pos)
        y_pos_array.append(y_pos)
        z_pos_array.append(z_pos)

        signal_x_array.append(signal_x)
        signal_y_array.append(signal_y)
        signal_z_array.append(signal_z)
        time.append(0)
    else:
        time_vals = b.time_handle(step, t_step, time, method)
        time = time_vals[0]
        t_step = time_vals[1]
        signal_x = b.multiply(10, b.subtract(y_pos, x_pos))
        signal_y = b.subtract(b.subtract(b.multiply(28, x_pos), y_pos), b.multiply(x_pos, z_pos))
        signal_z = b.subtract(b.multiply(x_pos, y_pos), b.multiply(8/3, z_pos))

        signal_x_array.append(signal_x)
        signal_y_array.append(signal_y)
        signal_z_array.append(signal_z)

        x_pos = b.integrate(step, t_step, signal_x_array, x_pos, method, x_init)
        y_pos = b.integrate(step, t_step, signal_y_array, y_pos, method, y_init)
        z_pos = b.integrate(step, t_step, signal_z_array, z_pos, method, z_init)

        x_pos_array.append(x_pos)
        y_pos_array.append(y_pos)
        z_pos_array.append(z_pos)

        dac.setVoltage(0, b.pwm_map(y_pos, -32, 32, 12))
        dac.setVoltage(1, b.pwm_map(x_pos, -25, 25, 12))

    step += 1

#ax.plot(x_pos_array, y_pos_array, z_pos_array)
#plt.show()
    
dac.shutdown(0)
dac.shutdown(1)
GPIO.cleanup()

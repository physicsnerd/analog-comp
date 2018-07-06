import pigpio
import matplotlib.pyplot as plt

pi = pigpio.pi()

pi.set_mode(27,pigpio.OUTPUT)
pi.set_mode(4, pigpio.OUTPUT)

pi.set_PWM_frequency(27, 100)
pi.set_PWM_frequency(4, 100)

def integrate(ht_step, val_array, integral_val):
    return ht_step * (val_array[-1] + val_array[-2]) + integral_val

def pwm_map(val, mini, maxi, pwm_res):
    scale_fac = (2**pwm_res)-1
    if mini < 0:
        x = val + (0 - mini)
        return round(x/(maxi-mini)*scale_fac)
    else:
        x = val - mini
        return round(x/(maxi-mini)*scale_fac)

x_pos = .01
y_pos = 0
axial_mag = .1
elect_pot = 1
max_steps = 10000000

e_m = -1*47917945.3739

x_position_integral = x_pos
y_position_integral = y_pos

x_position_array = []
y_position_array = []

x_velocity_integral = 0
x_velocity_array = []

y_velocity_integral = 0
y_velocity_array = []

x_acceleration = 0
x_acceleration_array = []

y_acceleration = 0
y_acceleration_array = []

t_step = 10**(-12)
ht_step = t_step/2
step = 0

while step <= max_steps:
    electric_denominator = (x_position_integral**2 + y_position_integral**2)**(3/2)
    x_electric = elect_pot*x_position_integral/electric_denominator
    y_electric = elect_pot*y_position_integral/electric_denominator

    x_acceleration = e_m*(x_electric + (axial_mag*y_velocity_integral))
    y_acceleration = e_m*(y_electric - (axial_mag*x_velocity_integral))
    x_acceleration_array.append(x_acceleration)
    x_acceleration_array = x_acceleration_array[-2:]
    y_acceleration_array.append(y_acceleration)
    y_acceleration_array = y_acceleration_array[-2:]

    if step >= 1:
        x_velocity_integral = integrate(ht_step, x_acceleration_array, x_velocity_integral)
        y_velocity_integral = integrate(ht_step, y_acceleration_array, y_velocity_integral)
        x_velocity_array.append(x_velocity_integral)
        y_velocity_array.append(y_velocity_integral)
        x_velocity_array = x_velocity_array[-2:]
        y_velocity_array = y_velocity_array[-2:]

        x_position_integral = integrate(ht_step, x_velocity_array, x_position_integral)
        y_position_integral = integrate(ht_step, y_velocity_array, y_position_integral)

        if step % 10000 == 0:
            x_position_array.append(x_position_integral)
            y_position_array.append(y_position_integral)

    else:
        x_velocity_array.append(0)
        y_velocity_array.append(0)
        x_position_array.append(x_pos)
        y_position_array.append(y_pos)

    pi.set_PWM_dutycycle(27, pwm_map(x_position_integral,-.015,.015,8))
    pi.set_PWM_dutycycle(4,pwm_map(y_position_integral,-.015,.015,8))

    step+=1

pi.stop()
plt.plot(x_position_array, y_position_array)
plt.xlabel('x position')
plt.ylabel('y position')
plt.show()

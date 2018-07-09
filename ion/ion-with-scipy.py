from scipy.constants import physical_constants
import matplotlib.pyplot as plt
from scipy import integrate

#warning: this is slower than slow.

x_pos = float(input("initial x position of the ion: "))
y_pos = float(input("initial y position of the ion: "))
axial_mag = float(input("axial magnetic field strength: "))
elect_pot = float(input("electric field scalar: "))
max_steps = int(input("max simulation time: "))

e_m = physical_constants['elementary charge'][0]/physical_constants['deuteron mass'][0]

x_acceleration_array = []
y_acceleration_array = []

t_step = 10**(-12)
step = 0

while step <= max_steps:
    if step == 0:
        x_electric = elect_pot*x_pos/((x_pos**2 + y_pos**2)**(3/2))
        y_electric = elect_pot*y_pos/((x_pos**2 + y_pos**2)**(3/2))

        x_acceleration = -1*e_m*(x_electric)
        y_acceleration = -1*e_m*(y_electric)
    else:
        x_electric = elect_pot*x_position_integral[-1]/((x_position_integral[-1]**2 + y_position_integral[-1]**2)**(3/2))
        y_electric = elect_pot*y_position_integral[-1]/((x_position_integral[-1]**2 + y_position_integral[-1]**2)**(3/2))

    x_acceleration_array.append(x_acceleration)
    y_acceleration_array.append(y_acceleration)

    x_velocity_integral = integrate.cumtrapz(x_acceleration_array, dx=t_step, initial=0)
    y_velocity_integral = integrate.cumtrapz(y_acceleration_array, dx=t_step, initial=0)

    x_position_integral = integrate.cumtrapz(x_velocity_integral, dx=t_step, initial=x_pos)
    y_position_integral = integrate.cumtrapz(y_velocity_integral, dx=t_step, initial=y_pos)

    print(x_position_integral[-1])
    print(y_position_integral[-1])

    step += 1

plt.plot(x_position_integral, y_position_integral)
plt.xlabel('x position')
plt.ylabel('y position')
plt.show()

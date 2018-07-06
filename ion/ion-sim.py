from scipy.constants import physical_constants
import matplotlib.pyplot as plt
from collections import deque
from decimal import Decimal

def integrate(ht_step, val_array, integral_val):
    return ht_step * (Decimal(str(val_array[-1])) + Decimal(str(val_array[-2]))) + Decimal(str(integral_val))

x_pos = Decimal(input("initial x position of the ion: "))
y_pos = Decimal(input("initial y position of the ion: "))
axial_mag = Decimal(input("axial magnetic field strength: "))
elect_pot = Decimal(input("electric field scalar: "))
max_steps = int(input("max simulation time: "))

e_m = Decimal(-1)*Decimal(str(physical_constants['elementary charge'][0]))/Decimal(str(physical_constants['deuteron mass'][0]))

x_position_integral = x_pos
x_position_array = []

y_position_integral = y_pos
y_position_array = []

x_velocity_integral = 0
x_velocity_array = deque(maxlen=2)

y_velocity_integral = 0
y_velocity_array = deque(maxlen=2)

x_acceleration = 0
x_acceleration_array = deque(maxlen=2)

y_acceleration = 0
y_acceleration_array = deque(maxlen=2)

t_step = 10**(-12)
ht_step = Decimal(str(t_step/2))
step = 0

while step <= max_steps:
    electric_denominator = (x_position_integral**Decimal(2) + y_position_integral**Decimal(2))**(Decimal(3/2))
    x_electric = elect_pot*x_position_integral/electric_denominator
    y_electric = elect_pot*y_position_integral/electric_denominator

    x_acceleration = e_m*(x_electric + (axial_mag*y_velocity_integral))
    y_acceleration = e_m*(y_electric - (axial_mag*x_velocity_integral))
    x_acceleration_array.append(x_acceleration)
    y_acceleration_array.append(y_acceleration)

    if step >= 1:
        x_velocity_integral = integrate(ht_step, x_acceleration_array, x_velocity_integral)
        y_velocity_integral = integrate(ht_step, y_acceleration_array, y_velocity_integral)
        x_velocity_array.append(x_velocity_integral)
        y_velocity_array.append(y_velocity_integral)

        x_position_integral = integrate(ht_step, x_velocity_array, x_position_integral)
        y_position_integral = integrate(ht_step, y_velocity_array, y_position_integral)
        if step % 10000 == 0:
            x_position_array.append(x_position_integral)
            y_position_array.append(y_position_integral)
    else:
        x_velocity_array.append(0)
        y_velocity_array.append(0)        
        x_position_array.append(x_position_integral)
        y_position_array.append(y_position_integral)

    step+=1

plt.plot(x_position_array, y_position_array)
plt.xlabel('x position')
plt.ylabel('y position')
plt.show()

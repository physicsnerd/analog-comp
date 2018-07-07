from scipy.constants import physical_constants
import matplotlib.pyplot as plt

x_pos = float(input("initial x position of the ion: "))
y_pos = float(input("initial y position of the ion: "))
axial_mag = float(input("axial magnetic field strength: "))
electric_scalar = float(input("electric field scalar: "))
max_time = int(input("max simulation time: "))

e_m = physical_constants['elementary charge'][0]/physical_constants['deuteron mass'][0]

x_velocity = 0
y_velocity = 0

x_positions = []
y_positions = []
x_velocity_sum = 0
y_velocity_sum = 0
x_acceleration_sum = 0
y_acceleration_sum = 0

t=0
while t <= max_time: 
    x_electric = electric_scalar*x_pos/((x_pos**2 + y_pos**2)**(3/2))
    y_electric = electric_scalar*y_pos/((x_pos**2 + y_pos**2)**(3/2))

    x_acceleration = -1*e_m*((axial_mag*y_velocity) - x_electric)
    y_acceleration = e_m*((axial_mag*x_velocity) - y_electric)

    x_acceleration_sum+=x_acceleration*(10**(-9))
    y_acceleration_sum+=y_acceleration*(10**(-9))
    x_velocity = x_acceleration_sum
    y_velocity = y_acceleration_sum

    x_velocity_sum+=x_velocity*(10**(-9))
    y_velocity_sum+=y_velocity*(10**(-9))
    x_pos = (x_velocity_sum)
    y_pos = (y_velocity_sum)
    x_positions.append(x_pos)
    y_positions.append(y_pos)
    
    t+=1

plt.plot(x_positions,y_positions)
plt.xlabel('x positions')
plt.ylabel('y positions')
plt.show()

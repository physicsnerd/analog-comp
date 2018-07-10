import matplotlib.pyplot as plt
from analogpack import basicfunctions as b

x_pos = .01
y_pos = 0
axial_mag = .1
elect_pot = 1
max_steps = 2500000

e_m = -1*47917945.397795496

x_position_integral = x_pos
y_position_integral = y_pos

x_position_array = []
y_position_array = []

x_velocity_integral = 0
y_velocity_integral = 0

x_velocity_array = []
y_velocity_array = []

x_acceleration = 0
y_acceleration = 0

x_acceleration_array = []
y_acceleration_array = []

t_step = 10**(-12)
step = 0

pos_mini = -.015
pos_maxi = .015
pwm_res = 8

integral_type = 'simp38'

while step <= max_steps:
    electric_denominator = b.power(b.add(b.square(x_position_integral), b.square(y_position_integral)), 1.5)
    x_electric = b.divide(b.multiply(elect_pot,x_position_integral),electric_denominator)
    y_electric = b.divide(b.multiply(elect_pot,y_position_integral),electric_denominator)

    x_acceleration = b.multiply(e_m,b.add(x_electric,b.multiply(axial_mag,y_velocity_integral)))
    y_acceleration = b.multiply(e_m,b.subtract(y_electric, b.multiply(axial_mag,x_velocity_integral)))

    x_acceleration_array.append(x_acceleration)
    y_acceleration_array.append(y_acceleration)

    x_acceleration_array = x_acceleration_array[-4:]
    y_acceleration_array = y_acceleration_array[-4:]

    if step != 0:
        x_velocity_integral = b.integrate(step, t_step, x_acceleration_array, x_velocity_integral, integral_type,0)
        y_velocity_integral = b.integrate(step, t_step, y_acceleration_array, y_velocity_integral, integral_type,0)

        x_velocity_array.append(x_velocity_integral)
        y_velocity_array.append(y_velocity_integral)

        x_velocity_array = x_velocity_array[-4:]
        y_velocity_array = y_velocity_array[-4:]

        x_position_integral = b.integrate(step, t_step, x_velocity_array, x_position_integral, integral_type, x_pos)
        y_position_integral = b.integrate(step, t_step, y_velocity_array, y_position_integral, integral_type, y_pos)

        #t_step = b.step_vary(x_velocity_array, y_velocity_array, x_acceleration_array, y_acceleration_array,.000075)
        #time = []
        #t_step = b.time_handle(step, t_step, time, integral_type)[1]

    else:
        x_position_array.append(x_pos)
        y_position_array.append(y_pos)
        y_velocity_array.append(0)
        x_velocity_array.append(0)

    if step % 1000 == 0:
        x_position_array.append(x_position_integral)
        y_position_array.append(y_position_integral)
  
    if step % 1000000 == 0:
        print(step)

    step+=1

plt.plot(x_position_array, y_position_array)
plt.xlabel('x position')
plt.ylabel('y position')
plt.show()

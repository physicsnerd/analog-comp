import matplotlib.pyplot as plt
#import pigpio

#to run, beforehand, make sure sudo pigpiod has been run
#pi = pigpio.pi()

#pi.set_mode(27,pigpio.OUTPUT)
#pi.set_mode(4, pigpio.OUTPUT)

#pi.set_PWM_frequency(27, 100)
#pi.set_PWM_frequency(4, 100)

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
      
def integrate(step, t_step, new_val, integral_val, init_val):
    if step == 1:
        return t_step/2*(new_val[-2] + new_val[-1]) + init_val
    else:
        return t_step/2*(new_val[-2] + new_val[-1]) + t_step**2/12*((new_val[-2]-new_val[-3])/t_step - (new_val[-1] - new_val[-2])/t_step) + integral_val
    #elif step == 2:
     #   return 2*t_step/6*(new_val[-3]+4*new_val[-2]+new_val[-1]) + init_val
    #elif step == 3:
     #   return 3*t_step/8*(new_val[-4]+3*new_val[-3]+3*new_val[-2]+new_val[-1]) + init_val
    #elif step == 4:
     #   return 4*t_step/90*(7*new_val[-5]+32*new_val[-4]+12*new_val[-3]+32*new_val[-2]+7*new_val[-1]) + init_val
    #else:
     #   return t_step/720*(-19*new_val[-5]+106*new_val[-4]-264*new_val[-3]+646*new_val[-2]+251*new_val[-1]) + integral_val
    
def pwm_map(val, mini, maxi, pwm_res):
    scale_fac = (2**pwm_res)-1
    if mini < 0:
        x = val + (0 - mini)
        return round(x/(maxi-mini)*scale_fac)
    else:
        x = val - mini
        return round(x/(maxi-mini)*scale_fac)

while step <= max_steps:
    electric_denominator = (x_position_integral**2 + y_position_integral**2)**(3/2)
    x_electric = elect_pot*x_position_integral/electric_denominator
    y_electric = elect_pot*y_position_integral/electric_denominator

    x_acceleration = e_m*(x_electric + (axial_mag*y_velocity_integral))
    y_acceleration = e_m*(y_electric - (axial_mag*x_velocity_integral))
    x_acceleration_array.append(x_acceleration)
    y_acceleration_array.append(y_acceleration)
    x_acceleration_array = x_acceleration_array[-5:]
    y_acceleration_array = y_acceleration_array[-5:]

    if step != 0:
        x_velocity_integral = integrate(step, t_step, x_acceleration_array, x_velocity_integral,0)
        y_velocity_integral = integrate(step, t_step, y_acceleration_array, y_velocity_integral,0)

        x_velocity_array.append(x_velocity_integral)
        y_velocity_array.append(y_velocity_integral)

        x_velocity_array = x_velocity_array[-5:]
        y_velocity_array = y_velocity_array[-5:]

        x_position_integral = integrate(step, t_step, x_velocity_array, x_position_integral,x_pos)
        y_position_integral = integrate(step, t_step, y_velocity_array, y_position_integral,y_pos)

    else:
        #pi.set_PWM_dutycycle(27, pwm_map(x_pos,pos_mini,pos_maxi,pwm_res))
        #pi.set_PWM_dutycycle(4, pwm_map(x_pos,pos_mini,pos_maxi,pwm_res))
        x_position_array.append(x_pos)
        y_position_array.append(y_pos)
        y_velocity_array.append(0)
        x_velocity_array.append(0)
    
    #if step % 500 == 0:
        #pi.set_PWM_dutycycle(27, pwm_map(x_position_integral,pos_mini,pos_maxi,pwm_res))
        #pi.set_PWM_dutycycle(4, pwm_map(y_position_integral,pos_mini,pos_maxi,pwm_res))

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
#pi.stop()

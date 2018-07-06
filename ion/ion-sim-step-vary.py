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
max_steps = 5000000

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

t_step = 10**(-13)
step = 0

pos_mini = -.015
pos_maxi = .015
pwm_res = 8
      
def integrate(step, t_step, new_val, integral_val):
    #if step == 1:
    return t_step/2*(new_val[-2] + new_val[-1]) + integral_val
    #else:
    #    return t_step/3*(-.25*new_val[-3]+2*new_val[-2]+1.25*new_val[-1]) + integral_val

def pwm_map(val, mini, maxi, pwm_res):
    scale_fac = (2**pwm_res)-1
    if mini < 0:
        x = val + (0 - mini)
        return round(x/(maxi-mini)*scale_fac)
    else:
        x = val - mini
        return round(x/(maxi-mini)*scale_fac)

def step_vary(xv_array, yv_array, xa_array, ya_array, tolerance):
    t_step_type = 'normal'
    try:
        dxa = abs(xa_array[-1]/xa_array[-2])
        dya = abs(ya_array[-1]/ya_array[-2])
        dxv = abs(xv_array[-1]/xv_array[-2])
        dyv = abs(yv_array[-1]/yv_array[-2])
        if (dxv > (1 + tolerance)) or (dyv > (1+tolerance)) or (dxa > (1+tolerance)) or (dya > (1 + tolerance)):
            t_step_type = 'fine'
        elif dxv < (1-tolerance) or dyv < (1-tolerance) or dxa < (1-tolerance) or dya < (1-tolerance):
            t_step_type = 'fine'
        else:
            t_step_type = 'normal'
    except ZeroDivisionError:
        t_step_type = 'normal'
    if t_step_type == 'normal':
        return 10**(-12)
    else:
        return 10**(-15)

while step <= max_steps:
    electric_denominator = (x_position_integral**2 + y_position_integral**2)**(3/2)
    x_electric = elect_pot*x_position_integral/electric_denominator
    y_electric = elect_pot*y_position_integral/electric_denominator

    x_acceleration = e_m*(x_electric + (axial_mag*y_velocity_integral))
    y_acceleration = e_m*(y_electric - (axial_mag*x_velocity_integral))
    x_acceleration_array.append(x_acceleration)
    y_acceleration_array.append(y_acceleration)
    x_acceleration_array = x_acceleration_array[-3:]
    y_acceleration_array = y_acceleration_array[-3:]

    if step != 0:
        x_velocity_integral = integrate(step, t_step, x_acceleration_array, x_velocity_integral)
        y_velocity_integral = integrate(step, t_step, y_acceleration_array, y_velocity_integral)

        x_velocity_array.append(x_velocity_integral)
        y_velocity_array.append(y_velocity_integral)

        x_velocity_array = x_velocity_array[-3:]
        y_velocity_array = y_velocity_array[-3:]

        x_position_integral = integrate(step, t_step, x_velocity_array, x_position_integral)
        y_position_integral = integrate(step, t_step, y_velocity_array, y_position_integral)

        t_step = step_vary(x_velocity_array, y_velocity_array, x_acceleration_array, y_acceleration_array,.000075)

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

import pigpio
import math
import time

pi = pigpio.pi()
pi.set_mode(27, pigpio.OUTPUT)
pi.set_mode(4, pigpio.OUTPUT)
pi.set_PWM_frequency(27, 500)
pi.set_PWM_frequency(4, 500)

def pwm_map(val, mini, maxi, pwm_res):
    scale_fac = (2**pwm_res)-1
    if mini < 0:
        x = val + (0 - mini)
        return round(x/(maxi-mini)*scale_fac)
    else:
        x = val - mini
        return round(x/(maxi-mini)*scale_fac)

x = 0

while x < 200000:
    n = math.cos(x)
    n2 = math.sin(x)
    pi.set_PWM_dutycycle(27, pwm_map(n,-1,1,8))
    pi.set_PWM_dutycycle(4, pwm_map(n2,-1,1,8))
    time.sleep(.01)
    x+=(2*math.pi)/256

pi.stop()
    

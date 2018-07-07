import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)

test_pwm = GPIO.PWM(27, 100)
test_pwm.start(0)

step = 1
d = 0
while 1 == 1:
    while d < 100:
        d+=1
        test_pwm.ChangeDutyCycle(d)
        time.sleep(.1)
    while d > 0:
        d-=1
        test_pwm.ChangeDutyCycle(d)
        time.sleep(.1)

test_pwm.stop()
GPIO.cleanup()

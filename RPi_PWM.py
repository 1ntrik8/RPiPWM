# Leigh Rowell
# ID: 219309149
# SIT210 - 7.3D
# RPi PWM

# Ref: Blind spot monitoring script SIT210 Trimester 1, week 3 2020.

# Import libraries and set up GPIO mode
import RPi.GPIO as GPIO
import time
import _thread
from gpiozero import LED

GPIO.setmode(GPIO.BCM)

# Define pins and hardware
TRIG = 4
ECHO = 18
LED = 12
BUZZER = 26

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

# Create PWM instance with frequency of 2500 (2500 seems to work best for this)
LED_PWM = GPIO.PWM(LED, 2500)
BUZZ_PWM = GPIO.PWM(BUZZER, 2500)
LED_PWM.start(0)
BUZZ_PWM.start(0)

def action(distance):
    # Calculate a duty cycle between 0 and 100 in 5 increments
    dc = 100 - distance
    if dc < 0: dc = 0
    elif dc < 20: dc = 20
    elif dc < 40: dc = 40
    elif dc < 80: dc = 80
    elif dc < 100: dc = 100
    print('Duty cycle: {}'.format(dc))
    
    LED_PWM.ChangeDutyCycle(dc)
    BUZZ_PWM.ChangeDutyCycle(dc)

def check_dist():
    # Fire the sensor and time the response, return the distance in cm.
    GPIO.output(TRIG, True)
    time.sleep (0.0001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == False:
        start = time.time()

    while GPIO.input(ECHO) == True:
        end = time.time()

    sig_time = end-start

    # calculate distance in cm: 
    distance = sig_time / 0.000058
    
    # return the distance result.
    print('Distance: {} cm'.format(distance))
    return distance
	
def monitor_distance():
    # Continually check the distance from the sensor.
    while True:
        distance = check_dist()
        time.sleep(0.4)
        
        # If the distance is less than 2m call the action function.
        if distance < 200:
            action(distance)

# Create a new thread to monitor the sensor input.
try:
   _thread.start_new_thread( monitor_distance, ())
except:
   print ("Error: unable to start thread")

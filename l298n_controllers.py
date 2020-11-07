import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM) 

GPIO.setup(21, GPIO.OUT)  # ENB
GPIO.setup(20, GPIO.OUT)  # IN 4
GPIO.setup(16, GPIO.OUT)  # IN 3

GPIO.setup(17, GPIO.OUT)  # ENA
GPIO.setup(27, GPIO.OUT)  # IN 1
GPIO.setup(22, GPIO.OUT)  # IN 2
 
direction = input('Please define the direction (Reverse=1 or Forward=2): ')
dc = input('Please define the Motor PWM Duty Cycle (0-100): ')
hz = input ('HZ: ')
pwm_a = GPIO.PWM(17, hz)
pwm_b = GPIO.PWM(21, hz)
 
if direction == 1: # Reverse
    GPIO.output(27, 1)
    GPIO.output(22, 0)

    GPIO.output(16, 0)
    GPIO.output(20, 1)
elif direction == 2: # Forward
    GPIO.output(27, 0)
    GPIO.output(22, 1)
 
    GPIO.output(16, 1)
    GPIO.output(20, 0)
try:
    while True:
        pwm_a.start(dc)
        pwm_b.start(dc)
 
except KeyboardInterrupt:
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()

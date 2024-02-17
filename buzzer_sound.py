import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO_PIN = 18
GPIO.setup(GPIO_PIN, GPIO.OUT)

# Start PWM
GPFrequency = 50
pwm = GPIO.PWM(GPIO_PIN, GPFrequency)
pwm.start(0)

def buzz(duration):
    pwm.ChangeDutyCycle(50)  # Turn buzzer on
    time.sleep(duration)     # Keep buzzer on for duration seconds
    pwm.ChangeDutyCycle(0)   # Turn buzzer off

# Example usage:
buzz(10)  # Buzzer will turn on for 2 seconds

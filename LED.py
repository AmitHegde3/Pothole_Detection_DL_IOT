from gpiozero import LED
from time import sleep

led = LED(17)  # GPIO pin number
led_blue = LED(27)

def ledStart():
	led.on()  # LED on
	sleep(5)  # delay for 1 second
	led.off()  # LED off
	sleep(1)  # delay for 1 second
    
def ledBlink():
	led.on()  # LED on
	sleep(1)  # delay for 1 second
	led.off()  # LED off
	sleep(1)  # delay for 1 second
	
def ledBlue():
	led_blue.on()  # LED on
	sleep(1)  # delay for 1 second
	led_blue.off()  # LED off
	sleep(1)  # delay for 1 second
	
def shut_blink():
	led_blue.on()
	led.on()
	sleep(2)
	led_blue.off()
	led.off()
	sleep(2)

#shut_blink()
#ledStart()
#ledBlink()
#ledBlue()

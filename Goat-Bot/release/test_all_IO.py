###
import RPi.GPIO
from gopigo import *

RPi.GPIO.setmode(RPi.GPIO.BCM)
### IR Flame detection pin 20, pin 21
RPi.GPIO.setup(20, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(21, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_DOWN)

### Red LED light
RPi.GPIO.setup(16,RPi.GPIO.OUT)

### Relay for Fan/Water
RPi.GPIO.setup(12,RPi.GPIO.OUT)



'''
### Read IR Flame detection
if RPi.GPIO.input(21) == RPi.GPIO.HIGH:
	print("flame detected.")
'''
	
### Button reading from GoPiGo shield D11 part	
pin =10
mode = "OUTPUT"
a = pinMode(pin, mode)
time.sleep(0.1)
button = digitalRead(pin)
print int(button)
#print "Button Reading: " + str(button)


print "Button Reading: " + str(button)
while True:
	button = digitalRead(pin)
	print "Button Reading: " + str(button)
	if button==1:
		break
#test flame sensor A pin 20
while True:
	if RPi.GPIO.input(20) == RPi.GPIO.LOW:
		print("flame detected A")
		break;
#test flame sensor B pin 21
while True:
	if RPi.GPIO.input(21) == RPi.GPIO.LOW:
		print("flame detected B")
		break;
		
	
### Turn on Red LED
RPi.GPIO.output(16,True)
time.sleep(2)

### Turn off Red LED
RPi.GPIO.output(16,False)

### Turn On Relay for Fan/Water
RPi.GPIO.output(12,True)
time.sleep(2)

### Turn Off Relay for Fan/Water
RPi.GPIO.output(12,False)

RPi.GPIO.cleanup()
'''
### Turn On Relay for Fan/Water
RPi.GPIO.output(12,True)

### Turn Off Relay for Fan/Water
RPi.GPIO.output(12,False)

### Turn on Green LED
RPi.GPIO.output(21,True)

### Turn off Green LED
RPi.GPIO.output(21,False)

### Turn on Red LED
RPi.GPIO.output(20,True)

### Turn on Red LED
RPi.GPIO.output(20,False)
'''


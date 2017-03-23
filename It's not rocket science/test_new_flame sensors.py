import RPi.GPIO
import time
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(20,RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_DOWN)
###IR FLAME DETECTION
if RPi.GPIO.input(20) == RPi.GPIO.HIGH:
	print("FLAME DETECTED")
	flame=1
else:
	flame=0
print flame
		

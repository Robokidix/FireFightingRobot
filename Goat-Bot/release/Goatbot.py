
from gopigo import *
from control import *
import RPi.GPIO
import math
import time
import sys
### setup I/O
import RPi.GPIO
RPi.GPIO.setmode(RPi.GPIO.BCM)
### IR Flame detection pin 20, pin 21
RPi.GPIO.setup(20, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(21, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_DOWN)
### Red LED light pin 16
RPi.GPIO.setup(16,RPi.GPIO.OUT)
### Relay for Fan/Water pin 12
RPi.GPIO.setup(12,RPi.GPIO.OUT)
### Button reading from GoPiGo shield D11 part	
pin =10
mode = "OUTPUT"
a = pinMode(pin, mode)

### room searching parameters
REPEAT=40
DIST_2_R_WALL_CLOSE=10 #cm
DIST_2_R_WALL_FAR=15 #cm
DIST_2_F_WALL_CLOSE=15 #cm
SERVOR_FRONT=90
SERVOR_RIGHT=10
DELAY=0.5

Candle=0 #No flame: 0, Find flame: 1, Put off Candle: 2

def main():
    #Reset the robot: task 0
    servo(SERVOR_FRONT) #aim distance sensor to front
    red_led_off()    
    turn_off_fan()
    
    #Wait Start Button Pressed: task 1
    print("Task 1 Start: waiting for button pressed")
    while True:
        if check_button()==1:
            break
    print("Task 1 Done: button pressed")
    
    #Correct Heading: task 2
    correct_heading() #not done yet
    for x in range(REPEAT):
        #Read Flame Senor: task 3
        if check_flame_sensor_A()==1:
            break
        #Searing Room: task 4
        room_searching()
    #Flame search: task 5
    stop()#stop robot
    if search_candle()==1:
        #Extinguish Candle: task 6
        if put_off_candle()==1:
            print("Candle is put off!")
            stop()#stop robot


 #Searing Room: task 4
def room_searching():
    print("Task 4 Start: searching room..")    
    for x in range(1):
        time.sleep(1)
        servo(SERVOR_FRONT)
        time.sleep(DELAY)
        dist_front=us_dist(15)
        print( "Distance to Front  Wall: {}cm".format(dist_front))
        servo(SERVOR_RIGHT)
        time.sleep(DELAY)
        dist_right=us_dist(15)
        print( "Distance to right Wall: {}cm".format(dist_right))
        if dist_front > DIST_2_F_WALL_CLOSE:
		if dist_right < DIST_2_R_WALL_FAR and dist_right > DIST_2_R_WALL_CLOSE:
			set_speed(50)
			#Move fwd one turn
			enc_tgt(1,1,9)
			fwd()
			#time.sleep(1)
		else:
			if dist_right > DIST_2_R_WALL_FAR:
				set_left_speed(60)
				set_right_speed(30)
				#Move fwd slightly right one turn
				enc_tgt(1,1,9)
				fwd()
				#time.sleep(1)
			else: 
				set_left_speed(40)
				set_right_speed(60)
				#Move fwd slightly left one turn
				enc_tgt(1,1,9)
				fwd()
				#time.sleep(1)
	else:
		#turn left 90 degree to avoid the front wall
		stop()
		set_speed(50)
		left_deg(90)
		time.sleep(2)
print("Task 4 Done: searching room DONE")
     
#Correct Heading: task 2				
def correct_heading():
    print("Task 2 Start: Correct heading..")
    time.sleep(1)
    servo(SERVOR_FRONT)
    time.sleep(DELAY)
    dist_front=us_dist(15)
    print( "Distance to Front  Wall: {}cm".format(dist_front))
    servo(SERVOR_RIGHT)
    time.sleep(DELAY)
    dist_right=us_dist(15)
    print( "Distance to right Wall: {}cm".format(dist_right))
    if dist_front > DIST_2_F_WALL_CLOSE:
		if dist_right < DIST_2_R_WALL_FAR and dist_right > DIST_2_R_WALL_CLOSE:
			set_speed(50)
			#Move fwd one turn
			enc_tgt(1,1,9)
			fwd()
			#time.sleep(1)
		else:
			if dist_right > DIST_2_R_WALL_FAR:
				set_left_speed(60)
				set_right_speed(30)
				#Move fwd slightly right one turn
				enc_tgt(1,1,9)
				fwd()
				#time.sleep(1)
			else: 
				set_left_speed(40)
				set_right_speed(60)
				#Move fwd slightly left one turn
				enc_tgt(1,1,9)
				fwd()
				#time.sleep(1)
    else:
		#turn left 90 degree to avoid the front wall
		stop()
		set_speed(50)
		left_deg(90)
		time.sleep(2)
print("Task 2 Done: Correct heading DONE")

#Read Start Button: task 1
def wait_start_button():
    print("Task 1 Start: Wait start button press..")
    print("Task 1 Done: Start button pressed. ..")


#Read Flame Senor: task 3    
def check_flame_sensor():
    print("Task 3 Start: Check flame sensor...")
    print("Task 3 Done: Check flame sensor DONE")

#Flame search: task 5
def search_candle():
    print("Task 5 Start: searching candle..")
    #if confirme
    return 1
    #if not confirm
    return 0
    print("Task 5 Done: searching candle done")

#extinguish Candle: task 6  
def put_off_candle():
    print("Task 6 Start: Putting off candle..")
    #if confirm candle is off
    Candle=2
    return Candle
    print("Task 6 Done: Putting off candle DONE")

#track robot position in the field    
def where_is_my_robot():
    print("Where is my robot..")

#Turn on ReD LED for finding Candle pin 16
def red_led_on(): 
    print("Turn on Red LED")
    RPi.GPIO.output(16,True)

#Turn off Red LED pin 16
def red_led_off():
    print("Turn off Red LED")
    RPi.GPIO.output(16,False)
    
#Turn on the Fan to put off Candle fire pin 12
def turn_on_fan():
    print("Turn on the Fan to put off candle")
    RPi.GPIO.output(12,True)

#Turn off the Fan pin 12
def turn_off_fan():
    print("Turn off the Fan")
    RPi.GPIO.output(12,False)
    
#Check Flame Sensor A pin 20
def check_flame_sensor_A():
    print("checking flame senor A")
    if RPi.GPIO.input(20) == RPi.GPIO.LOW:
        print("flame A detected.")
        return 1
    else:
        print("No flame A")
        return 0

#Check Flame Sensor B pin 21
def check_flame_sensor_B():
    print("checking flame senor B")
    if RPi.GPIO.input(21) == RPi.GPIO.LOW:
        print("flame B detected.")
        return 1
    else:
        print("No flame B")
        return 0

#Check Button Pressed D11(10)
def check_button():
    print("checking button pressed")
    button = digitalRead(pin)
    print( "Button Reading: " + str(button))
    return button
    
 
if __name__ == '__main__':
    main()         
		
			

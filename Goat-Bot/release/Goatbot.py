
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
REPEAT=5
DIST_2_R_WALL_CLOSE=10 #cm
DIST_2_R_WALL_FAR=15 #cm
DIST_2_F_WALL_CLOSE=15 #cm
DIST_2_F_WALL_FAR=20 #cm
DIST_2_L_WALL_FAR=20 #cm
DIST_2_R_WALL_CLOSER=7 #this is new
SERVOR_FRONT=90
SERVOR_RIGHT=10
DELAY=0.5
HIGHTSPEED=100
LOWSPEED=50

CANDLE=0 #No flame: 0, Find flame: 1, Put off Candle: 2 :state machine

def main():
    #Reset the robot: task 0
    servo(SERVOR_FRONT) #aim distance sensor to front
    red_led_off()    
    turn_off_fan()
    
    #Wait Start Button Pressed: task 1
    wait_start_button()
    
    #Correct Heading: task 2
    correct_heading() #not done yet
    CANDLE=0
    while CANDLE!=2:
        for x in range(REPEAT):
            #Read Flame Senor: task 3
            if check_flame_sensor_A()==1:
                print("Flame Sensor A see a Candle")
                print("Turn on the Red LED")
                red_led_on()
                break
            #Searing Room: task 4: not done yet for 4th room
            room_searching()
            #Flame search: task 5
            stop()#stop robot
            if search_candle()==1:
                CANDLE=1
                #Extinguish Candle: task 6
                if put_off_candle()==1:
                    print("Candle is put off!")
                    stop()#stop robot
                    CANDLE=2
                else:
                     print("Candle is still ON.")
            else:
                CANDLE=0

#Wait Start Button Pressed: task 1
def wait_start_button():
    print("Task 1 Start: waiting for button pressed")
    while True:
        if check_button()==1:
            break
    print("Task 1 Done: button pressed")

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
			goatbot_fwd()
		else:
			if dist_right > DIST_2_R_WALL_FAR:
				goatbot_fwd_right()
			else: 
				goatbot_fwd_left()
	else:
		#turn left 90 degree to avoid the front wall
		stop()
		goatbot_left_rot()
		
print("Task 4 Done: searching room DONE")
     
#Correct Heading: task 2				
def correct_heading():
    print("Task 2 Start: Correct heading..")
    time.sleep(1)
    servo(SERVOR_LEFT)
    time.sleep(DELAY)
    dist_left=us_dist(15)
    print( "Distance to Front  Wall: {}cm".format(dist_left))
    servo(SERVOR_RIGHT)
    time.sleep(DELAY)
    dist_right=us_dist(15)
    print( "Distance to right Wall: {}cm".format(dist_right))
    
    if dist_right < DIST_2_R_WALL_CLOSER and dist_left > DIST_2_L_WALL_FAR:
        print("Task 2 : Orietation B. Rotation right 90 Degree")
        goatbot_right_rot(90)
    
    else:
        print("Task 2 : Orietation A.")
    print("Task 2 Done: Correct heading DONE")

#Read Flame Senor: task 3    
def check_flame_sensor():
    print("Task 3 Start: Check flame sensor...")
    if check_flame_sensor_A()==1:
        print("Flame Sensor A see a Candle")
        print("Turn on the Red LED")
        red_led_on()
    else:
        pass
    print("Task 3 Done: Check flame sensor DONE")

#Flame search: task 5
def search_candle():
    print("Task 5 Start: searching candle..")
    time.sleep(1)
    if check_flame_sensor_A()==1 and check_flame_sensor_AB()==1:
        print("Task 5: confirmed the candle is found")
        print("Turn on the Red LED")
        red_led_on()
        pass
    else:
        print("Task 5: The candle is NOT found")
        print("Task 5: Searching candle, rotating right 15")
        goatbot_right_rot(15)
        if check_flame_sensor_A()==1 and check_flame_sensor_AB()==1:
            stop()
            print("Task 5: confirmed the candle is found")
            pass
        else:
            goatbot_left_rot(30)
            print("Task 5: The candle is NOT found")
            print("Task 5: Searching candle, rotating left 30")
            if check_flame_sensor_A()==1 and check_flame_sensor_AB()==1:
                stop()
                print("Task 5: confirmed the candle is found")
                pass
            else:
                print("Task 5: The candle is NOT found")
                return 0
    return 1
    print("Task 5 Done: searching candle done")

#extinguish Candle: task 6  
def put_off_candle():
    distance_to_stop=10 #10cm
    print("Task 6 Start: Putting off candle..")
    print("Task 6 : Fan is ON")
    turn_on_fan()
    print("Task 6 : Robot is approaching to candle")
    while True:
        dist=us_dist(15)			#Find the distance of the object in front
        print "Dist:",dist,'cm'
        if dist<distance_to_stop:	#If the object is closer than the "distance_to_stop" distance, stop the GoPiGo
		print "Stopping"
		stop()					#Stop the GoPiGo
		break
        time.sleep(.1)
        goatbot_fwd()
    time.sleep(5)    
    turn_off_fan()
    print("Task 6 : Fan is off")
    if check_flame_sensor_A()==1 and check_flame_sensor_AB()==1:
        print("Task 6: Candle is STILL ON after 1st try")
        print("Task 6 : Fan is ON")
        turn_on_fan()
        print("Task 6: Rotating robot")
        goatbot_right_rot(5)
        time.sleep(1)
        goatbot_right_rot(5)
        time.sleep(1)
        goatbot_right_rot(5)
        time.sleep(1)
        goatbot_left_rot(15)
        time.sleep(1)
        goatbot_left_rot(5)
        time.sleep(1)
        goatbot_left_rot(5)
        time.sleep(1)
        goatbot_left_rot(5)
        time.sleep(1)
        turn_off_fan()
        print("Task 6 : Fan is off")
        if check_flame_sensor_A()==1 and check_flame_sensor_AB()==1:
            print("Task 6: Candle is STILL ON after 2nd try")
            print("Task 6 : Fan is ON")
            turn_on_fan()
            print("Task 6: Closing to Candel")
            goatbot_right_rot(15)
            time.sleep(1)
            goatbot_fwd()
            time.sleep(5)
            turn_off_fan()
            print("Task 6 : Fan is off")
            if check_flame_sensor_A()==1 and check_flame_sensor_AB()==1:
                print("Task 6: Candle is STILL ON after 3rd try")
                return 0
            else:
                pass
        else:
            pass            
    else:
        pass
    return 1
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

#GoatBot special mvoing cmd
#Because the wiring of motor is differnt to GoPiGo
#left motor controlled by right motor signal
def goatbot_fwd():
    set_speed(HIGHSPEED)
    #Move fwd half turn
    enc_tgt(1,1,9)
    fwd()
    time.sleep(1)

def goatbot_fwd_right():
    set_left_speed(HIGHSPEED+50)
    set_right_speed(HIGHSPEED)
    #Move fwd slightly right one turn
    enc_tgt(1,1,9)
    fwd()
    time.sleep(1)

def goatbot_fwd_left():
    set_left_speed(HIGHSPEED)
    set_right_speed(HIGHSPEED+50)
    #Move fwd slightly left one turn
    enc_tgt(1,1,9)
    fwd()
    time.sleep(1)

def goatbot_left(degree):
    set_speed(HIGHSPEED)
    #Rotate left
    left_deg(90)
    time.sleep(2)

def goatbot_right(degree):
    set_speed(HIGHSPEED)
    #Rotate right
    right_deg(90)
    time.sleep(2)

def goatbot_left_rot(degree):
    set_speed(HIGHSPEED)
    #Rotate left both wheel
    left_rot_deg(90)
    time.sleep(2)

def goatbot_right_rot(degree):
    set_speed(HIGHSPEED)
    #Rotate right both wheel
    right_rot_deg(90)
    time.sleep(2)
    
 
if __name__ == '__main__':
    main()         
		
			

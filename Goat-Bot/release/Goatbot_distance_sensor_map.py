
from gopigo import *
from control import *
import RPi.GPIO
import math
import time
import sys
import scan_room
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
REPEAT=100
DIST_2_R_WALL_CLOSE=15 #cm
DIST_2_R_WALL_FAR=35 #cm
DIST_2_R_WALL_TOO_FAR=60 #cm

DIST_2_F_WALL_CLOSE=15 #cm

DIST_2_R_WALL_CLOSER=7 #this is new

DIST_2_R_WALL_HEADING=20
DIST_2_L_WALL_HEADING=20


DIST_2_F_WALL_FAR=20 #cm

SERVOR_FRONT=90 #Teddybot 70
SERVOR_RIGHT=160 #Teddybot 0
SERVOR_LEFT=20 #Teddybot 140
DELAY=1
HIGHSPEED=80 #Teddybot 50; Goatbot 100
LOWSPEED=50

CANDLE=0 #No flame: 0, Find flame: 1, Put off Candle: 2 :state machine
ROBOT_X=0
ROBOT_Y=0
ROBOT_HEADING=0

def main():
   
    
    #Wait Start Button Pressed: task 1
    wait_start_button()
    
    #Correct Heading: task 2
    #correct_heading() #not done yet
    CANDLE=0
    for x in range(REPEAT):
		#Read Flame Senor: task 3
		#if check_flame_sensor_A()==1:
		if 0==1:
			print("Flame Sensor A see a Candle")
			print("Turn on the Red LED")
			red_led_on()
			break
		else:
			#Searing Room: task 4: not done yet for 4th room
			room_searching()
		

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
        
        dist_front=correct_dist()
        print( "Distance to Front  Wall: {}cm".format(dist_front))
        servo(SERVOR_RIGHT)
        time.sleep(DELAY)
        
        dist_right=correct_dist()
        print( "Distance to right Wall: {}cm".format(dist_right))
        if dist_front > DIST_2_F_WALL_CLOSE:
            if dist_right<DIST_2_R_WALL_TOO_FAR:
                follow_wall(dist_front,dist_right)
            else:
                print("Find Cross, turn 60")
                goatbot_right_rot(60)
        else:
            if dist_right>DIST_2_R_WALL_CLOSE:
                print("Find left corner or top: turn right")
                goatbot_right_rot(60)
            else:
                print("find right corner: turn left 60")
                goatbot_left_rot(60)
    print("Task 4 Done: searching room DONE")   

def follow_wall(dist_front,dist_right):
    if dist_right < DIST_2_R_WALL_FAR and dist_right > DIST_2_R_WALL_CLOSE:
        print("Robot in the mddile of hallway: move forward")
        goatbot_fwd(10)
    else:
        if dist_right > DIST_2_R_WALL_FAR:
            print("Too Close to Right Wall: move slightly right")
            goatbot_fwd_right()
        else:
            print("Too Far to Right Wall: move slight left")
            goatbot_fwd_left()
        
        

def correct_dist():
	dist=us_dist(15)
	#while dist>300:
		#print("error in distance sensor reading, re-read")
		#time.sleep(0.1)
		#dist=us_dist(15)
	return dist	




#Check Button Pressed D11(10)
def check_button():
    print("checking button pressed")
    button = digitalRead(pin)
    print( "Button Reading: " + str(button))
    return button

def update_robot_location(left_enc,right_enc):
    global ROBOT_X
    global ROBOT_Y
    global ROBOT_HEADING
    WHEEL_RAD = 3.25 # Wheels are ~6.5 cm diameter. 
    CHASS_WID = 11.55 # Chassis is ~13.5 cm wide.
    DL=left_enc/18*math.pi*2*WHEEL_RAD
    DR=right_enc/18*math.pi*2*WHEEL_RAD
    DT=(DL+DR)/2
    theta=(DR-DL)/CHASS_WID
    ROBOT_HEADING=ROBOT_HEADING+theta
    DX=DT*math.sin(ROBOT_HEADING)
    DY=DT*math.cos(ROBOT_HEADING)
    DHEADING=math.degrees(theta)
    ROBOT_X=ROBOT_X+DX
    ROBOT_Y=ROBOT_Y+DY
    print(DX,DY,DHEADING)
    print(ROBOT_X,ROBOT_Y,math.degrees(ROBOT_HEADING))
        
#GoatBot special mvoing cmd
#Because the wiring of motor is differnt to GoPiGo
#left motor controlled by right motor signal
def goatbot_fwd(dist):
    set_speed(HIGHSPEED)
    #Move fwd half turn
    
    fwd_cm_wait(dist)
    #time.sleep(1)
    

def goatbot_fwd_right():
    set_speed(HIGHSPEED+20)
    stop()
    time.sleep(0.2)
    #right_deg_wait(30)
    pulse=4
    enc_tgt(1,0,pulse+1)
    right()
    while enc_read(0) < pulse:
		pass
    #Move fwd slightly right one turn
    set_speed(HIGHSPEED)
    fwd_cm_wait(5)
    stop()
    time.sleep(0.2)
    enc_tgt(0,1,pulse)
    set_speed(HIGHSPEED+20)
    left()
    while enc_read(1) < pulse:
		pass
    #left_deg_wait(30)
    #time.sleep(1)

def goatbot_fwd_left():
    set_speed(HIGHSPEED+20)
    stop()
    time.sleep(0.2)
    #right_deg_wait(30)
    pulse=4
    enc_tgt(0,1,pulse+1)
    left()
    while enc_read(1) < pulse:
		pass
    #Move fwd slightly right one turn
    set_speed(HIGHSPEED)
    fwd_cm_wait(5)
    stop()
    time.sleep(0.2)
    enc_tgt(1,0,pulse)
    set_speed(HIGHSPEED+20)
    right()
    while enc_read(0) < pulse:
		pass

def goatbot_left(degree):
    set_speed(HIGHSPEED)
    if degree<10:
		degree=10
    #Rotate left
    left_deg_wait(degree)
    #time.sleep(2)

def goatbot_right(degree):
    set_speed(HIGHSPEED)
    if degree<10:
		degree=10
    #Rotate right
    right_deg_wait(degree)
    #time.sleep(2)

def goatbot_left_rot(degree):
    set_speed(HIGHSPEED)
    if degree<12:
		degree=12
    #Rotate left both wheel
    left_rot_deg_wait(degree)
    #time.sleep(2)

def goatbot_right_rot(degree):
    set_speed(HIGHSPEED)
    if degree<12:
		degree=12
    #Rotate right both wheel
    right_rot_deg_wait(degree)
    #time.sleep(2)
 
 #def goatbot_fwd_cm_wait(dist):
	 #set_speed(HIGHSPEED)
	 #fwd_cm_wait(dist)
	
    
 
if __name__ == '__main__':
    #main()
    print (scan_room.us_map(40))
    print (scan_room.us_map(8))
    
 
    
   
			

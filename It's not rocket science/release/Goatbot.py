
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
REPEAT=40
DIST_2_R_WALL_CLOSE=15 #cm
DIST_2_R_WALL_FAR=35-10 #cm
DIST_2_R_WALL_TOO_FAR=50 #cm detect the cross can turn right

DIST_2_F_WALL_CLOSE=28 #cm

DIST_2_R_WALL_CLOSER=7 #this is new

DIST_2_R_WALL_HEADING=20
DIST_2_L_WALL_HEADING=20


DIST_2_F_WALL_FAR=20 #cm

SERVOR_FRONT=90 #Teddybot 70
SERVOR_RIGHT=155 #Teddybot 0
SERVOR_LEFT=20 #Teddybot 140
DELAY=0.5
HIGHSPEED=80 #Teddybot 50; Goatbot 100
LOWSPEED=50

CANDLE=0 #No flame: 0, Find flame: 1, Put off Candle: 2 :state machine
ROBOT_X=0
ROBOT_Y=0
ROBOT_HEADING=0

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
			else:
				#Searing Room: task 4: not done yet for 4th room
				room_searching_v2()
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
        
        dist_front=correct_dist(SERVOR_FRONT)
        print( "Distance to Front  Wall: {}cm".format(dist_front))
        servo(SERVOR_RIGHT)
        time.sleep(DELAY)
        
        dist_right=correct_dist(SERVOR_RIGHT)
        print( "Distance to right Wall: {}cm".format(dist_right))
        rotation_angel=90
        if dist_front > DIST_2_F_WALL_CLOSE:
            if dist_right<DIST_2_R_WALL_TOO_FAR:
                follow_wall(dist_front,dist_right)
            else:
                print("Find Cross, turn 60")
                #follow_wall(dist_front,dist_right)
                goatbot_fwd(15)
                goatbot_right_rot(rotation_angel)
        else:
			 servo(SERVOR_LEFT)
			 time.sleep(DELAY)
			 dist_left=correct_dist(SERVOR_LEFT)
			 if dist_right > dist_left:
				print("Find left corner or top: turn right")
				goatbot_right_rot(rotation_angel)
			 else:
				 print("find right corner: turn left 60")
				 goatbot_left_rot(rotation_angel)
    print("Task 4 Done: searching room DONE")

def follow_wall(dist_front,dist_right):
    if dist_right < DIST_2_R_WALL_FAR and dist_right > DIST_2_R_WALL_CLOSE:
        print("Robot in the mddile of hallway: move forward")
        goatbot_fwd(15)
    else:
        if dist_right > DIST_2_R_WALL_FAR:
            print("Too FAR to Right Wall: move slightly right")
            goatbot_fwd_right()
        else:
            print("Too Close to Right Wall: move slight left")
            goatbot_fwd_left()
 
def room_searching_v2():
    
    print("Task 4 Start: searching room..")
    for x in range(1):        
        servo(SERVOR_RIGHT)
        time.sleep(DELAY)        
        dist_right=correct_dist(SERVOR_RIGHT)
        print( "Distance to right Wall: {}cm".format(dist_right))
        time.sleep(1)
        servo(SERVOR_FRONT)
        time.sleep(DELAY)        
        dist_front=correct_dist(SERVOR_FRONT)
        print( "Distance to Front  Wall: {}cm".format(dist_front))
        
        rotation_angel=90
        if dist_front > DIST_2_F_WALL_CLOSE:
            if dist_right<DIST_2_R_WALL_TOO_FAR:
                follow_wall_v2(dist_front,dist_right)
            else:
                print("Find Cross, turn 60")
                #follow_wall(dist_front,dist_right)
                servo(SERVOR_FRONT)
                time.sleep(0.2)
                fwd_cm_wait_avoid(20,10)
                #goatbot_fwd(20)
                goatbot_right_rot(rotation_angel)
                fwd_cm_wait_avoid(25,10)
        else:
			 servo(SERVOR_LEFT)
			 time.sleep(DELAY)
			 dist_left=correct_dist(SERVOR_LEFT)
			 if dist_right > dist_left:
				print("Find left corner or top: turn right")
				goatbot_right_rot(rotation_angel-45)
			 else:
				 print("find right corner: turn left 60")
				 goatbot_left_rot(rotation_angel-45)
    print("Task 4 Done: searching room DONE")   
    
def follow_wall_v2(dist_front,dist_right):
    if dist_right < DIST_2_R_WALL_FAR and dist_right > DIST_2_R_WALL_CLOSE:
        print("Robot in the mddile of hallway: move forward")
        set_speed(HIGHSPEED)
        servo(SERVOR_FRONT)
        time.sleep(0.2)
        fwd_cm_wait_avoid(15,10)
        #time.sleep(2)
    else:
        if dist_right > DIST_2_R_WALL_FAR:
            print("Too FAR to Right Wall: move slightly right")
            goatbot_fwd_right()
        else:
            print("Too Close to Right Wall: move slight left")
            goatbot_fwd_left()
           
        
        

def correct_dist(last_servo_position=None):
	
    dist=us_dist(15)
    start_time=time.time();#if over 5 seconds getting invalid reading from us, move servor
    if last_servo_position is None:
		last_servo_position=90
    while dist>300:
		print("error in distance sensor reading, re-read")
		time.sleep(0.1)
		dist=us_dist(15)
		if time.time()-start_time>5:
			servo(last_servo_position-5)
			time.sleep(0.1)
			dist_1=us_dist(15)
			servo(last_servo_position+5)
			time.sleep(0.1)
			dist_2=us_dist(15)
			if dist_1<300:
				dist=dist_1
			else:
				if dist_2<300:
					dist=dist_2
    return dist	

     
#Correct Heading: task 2				
def correct_heading():
    global ROBOT_X
    global ROBOT_Y
    global ROBOT_HEADING
    print("Task 2 Start: Correct heading..")
    time.sleep(1)
    servo(SERVOR_LEFT)
    time.sleep(DELAY)
    dist_left=us_dist(15)
    print( "Distance to Front  Wall: {}cm".format(dist_left))
    servo(SERVOR_RIGHT)
    time.sleep(DELAY+2)
    dist_right=us_dist(15)
    print( "Distance to right Wall: {}cm".format(dist_right))
    
    if dist_right >DIST_2_R_WALL_HEADING and dist_left < DIST_2_L_WALL_HEADING:
        print("Task 2 : Orietation B. Rotation right 90 Degree")
        goatbot_right_rot(90)
    
    else:
        print("Task 2 : Orietation A.")
    #reset Robot heading, X, Y position
    ROBOT_X=0
    ROBOT_Y=0
    ROBOT_HEADING=0    
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
    if check_flame_sensor_A()==1 and check_flame_sensor_B()==1:
        print("Task 5: confirmed the candle is found")
        print("Turn on the Red LED")
        red_led_on()
        pass
    else:
        print("Task 5: The candle is NOT found")
        print("Turn on the Red LED")
        red_led_off()
        print("Task 5: Searching candle, rotating right 15")
        goatbot_right_rot(15)
        if check_flame_sensor_A()==1 and check_flame_sensor_A()==1:
            stop()
            print("Task 5: confirmed the candle is found")
            pass
        else:
            goatbot_left_rot(30)
            print("Task 5: The candle is NOT found")
            print("Task 5: Searching candle, rotating left 30")
            if check_flame_sensor_A()==1 and check_flame_sensor_A()==1:
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
    servo(SERVOR_FRONT) #aim distance sensor to front
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
        fwd_cm_wait_avoid(15,10)
    time.sleep(5)    
    turn_off_fan()
    print("Task 6 : Fan is off")
    if check_flame_sensor_A()==1 and check_flame_sensor_A()==1:
        print("Task 6: Candle is STILL ON after 1st try")
        print("Task 6 : Fan is ON")
        turn_on_fan()
        print("Task 6: Rotating robot")
        goatbot_right_rot(15)
        time.sleep(1)        
        goatbot_left_rot(15)
        time.sleep(1)
        goatbot_left_rot(15)        
        turn_off_fan()
        print("Task 6 : Fan is off")
        if check_flame_sensor_A()==1 and check_flame_sensor_A()==1:
            print("Task 6: Candle is STILL ON after 2nd try")
            print("Task 6 : Fan is ON")
            turn_on_fan()
            print("Task 6: Closing to Candel")
            goatbot_right_rot(15)
            time.sleep(1)
            fwd_cm_wait_avoid(15,5)
            time.sleep(5)
            turn_off_fan()
            print("Task 6 : Fan is off")
            if check_flame_sensor_A()==1 and check_flame_sensor_A()==1:
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
    enc_tgt(1,0,pulse+2)
    right()
    start_time=time.time()
    
    while enc_read(0) < pulse and time.time()-start_time<5:
		pass
    #Move fwd slightly right one turn
    set_speed(HIGHSPEED)
    servo(SERVOR_FRONT)
    time.sleep(0.2)
    fwd_cm_wait_avoid(5,10)
    #fwd_cm_wait(5)
    stop()
    time.sleep(0.2)
    enc_tgt(0,1,pulse)
    set_speed(HIGHSPEED+20)
    left()
    start_time=time.time()
    while enc_read(1) < pulse and time.time()-start_time<5:
		pass
    #left_deg_wait(30)
    #time.sleep(1)

def goatbot_fwd_left():
    set_speed(HIGHSPEED+20)
    stop()
    time.sleep(0.2)
    #right_deg_wait(30)
    pulse=4
    enc_tgt(0,1,pulse)
    left()
    start_time=time.time()  #if take more than 10 (TIME_LIMIT) seconds
    
    while enc_read(1) < pulse and time.time()-start_time<5:
		pass
    #Move fwd slightly right one turn
    set_speed(HIGHSPEED)
    servo(SERVOR_FRONT)
    time.sleep(0.2)
    fwd_cm_wait_avoid(5,10)
    #fwd_cm_wait(5)
    stop()
    time.sleep(0.2)
    enc_tgt(1,0,pulse)
    set_speed(HIGHSPEED+20)
    right()
    start_time=time.time()
    while enc_read(0) < pulse and time.time()-start_time<5:
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
    stop()
    main()
    stop()
    #set_speed(50)
    #left_deg_wait(45)
    #print("fwd")
    #fwd()
    #right_deg_wait(45)
    #print("fwd")
    #fwd()
    #fwd_cm_wait(20)
    #print("fwd")
    #fwd()
    #fwd_cm_wait_avoid(20, 20)
    #print("fwd")
    #fwd()
    #left_rot_deg_wait(45)
    #print("fwd")
    #fwd()
    #right_rot_deg_wait(45)
    #print("fwd")
    #fwd()
    #stop()
    #fwd_cm_wait_avoid(50,15)
    #print(correct_dist(90))
    #stop()
    #for x in range(80):
		#room_searching_v2()
    #stop()
    #print (scan_room.us_map(8))         
		
			

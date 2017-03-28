
from gopigo import *
from control import *
import math
import time
import sys
#import RPi.GPIO
#RPi.GPIO.setmode(RPi.GPIO.BCM)

#RPi.GPIO.setup(20, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_DOWN)

REPEAT=5
DIST_2_R_WALL_CLOSE=10 #cm
DIST_2_R_WALL_FAR=15 #cm
DIST_2_F_WALL_CLOSE=20 #cm
SERVOR_FRONT=90
SERVOR_RIGHT=140
DELAY=0.5

disable_servo()

servo(SERVOR_FRONT)

'''
for i in range(2):
	servo(SERVOR_FRONT)
	print( i)
	time.sleep(.02)
	time.sleep(DELAY)
	dist_front=us_dist(15)
	print( "Distance to Front Wall:{}cm".format(dist_front))
	servo(SERVOR_RIGHT)
	time.sleep(DELAY)
	dist_right=us_dist(15)
	print( "Distance to Front Wall:{}cm".format(dist_right))

'''
for x in range(REPEAT):
	time.sleep(1)
	servo(SERVOR_FRONT)
	time.sleep(DELAY)
	dist_front=us_dist(15)
	print( "Distance to Front Wall: {}cm".format(dist_front))
	servo(SERVOR_RIGHT)
	time.sleep(DELAY)
	dist_right=us_dist(15)
	print( "Distance to right Wall: {}cm".format(dist_right))
	if dist_front > DIST_2_F_WALL_CLOSE:
		if dist_right < DIST_2_R_WALL_FAR and dist_right > DIST_2_R_WALL_CLOSE:
			set_speed(50)
			#Move fwd one turn
			print ("move forward")
			enc_tgt(1,1,9)
			fwd()
			#time.sleep(1)
		else:
			if dist_right > DIST_2_R_WALL_FAR:
				set_left_speed(100)
				set_right_speed(40)
				#Move fwd slightly right one turn
				print ("move right")
				enc_tgt(1,1,9)
				fwd()
				#time.sleep(1)
			else: 
				set_left_speed(40)
				set_right_speed(100)
				#Move fwd slightly left one turn
				print("move left")
				enc_tgt(1,1,9)
				fwd()
				#time.sleep(1)
	else:
		#turn left 90 degree to avoid the front wall
		stop()
		set_speed(100)
		print("turn left 90")
		right_deg(90)
		time.sleep(2)
stop()
				
			

#!/usr/bin/env python
############################################################################################                                                                
# This example creates LIDAR like map using an ultrasonic sensor and a servo with the GoPiGo
#                                
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     	Date      		Comments
# Karan		  	13 June 14  	Initial Authoring           
# Biao			01 April 17     Fix bug and simpilfy                                      
'''
## License
 GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 Copyright (C) 2015  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''      
#
############################################################################################
#
# ! Attach Ultrasonic sensor to A1 Port.
#
############################################################################################
from gopigo import *
import sys
from collections import Counter
import math

def us_map(num_read):
	delay=.5*2/num_read # 0.02
	debug =1					#True to print all raw values
	num_of_readings=num_read			#Number of readings to take 
	incr=140/num_of_readings	#increment of angle in servo
	ang_l=[0]*(num_of_readings+1)	#list to hold the angle's of readings
	dist_l=[0]*(num_of_readings+1)	#list to hold the distance at each angle
	x=[0]*(num_of_readings+1)	#list to hold the x coordinate of each point
	y=[0]*(num_of_readings+1)	#list to hold the y coordinate of each point

	buf=[0]*40
	ang=20
	lim=250		#maximum limit of distance measurement (any value over this which be initialized to the limit value)
	index=0
	sample=2	#Number of samples for each angle (more the samples, better the data but more the time taken)
	print "Getting the data"
	servo(ang)
	while True:
		#Take the readings from the Ultrasonic sensor and process them to get the correct values
		for i in range(sample):
			dist=us_dist(15)
			if dist<lim and dist>=0:
				buf[i]=dist
			else:
				buf[i]=lim
		
		#Find the sample that is most common among all the samples for a particular angle
		max=Counter(buf).most_common()	
		rm=-1
		for i in range (len(max)):
			if max[i][0] <> lim and max[i][0] <> 0:
				rm=max[i][0]
				break
		if rm==-1:
			rm=lim
		
		if debug==1:
			print index,ang,rm
		ang_l[index]=ang
		dist_l[index]=rm
		index+=1

		#Move the servo to the next angle
		ang+=incr
		servo(ang)	
		time.sleep(delay)
		#print ang
		#if ang>=160:
		if index>num_of_readings:
			break
	
	print (dist_l)
	print (ang_l)
	return min(dist_l) #Return the closest distance in all directions
	


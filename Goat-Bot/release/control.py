#!/usr/bin/python
'''
IMPORTANT:this is for Goatbot only!!!
This module contains convenience functions to simplify
the coding of FireFighting contest tasks.

This really needs to be moved to a GoPiGo package
e.g. from gopigo.control import *
'''

from gopigo import *
import time
import GoatbotV3


en_debug=1

## 360 roation is ~64 encoder pulses or 5 deg/pulse
## DPR is the Deg:Pulse Ratio or the # of degrees per
##  encoder pulse.
DPR = 360.0/50 #360.0/64 goatbot
WHEEL_RAD = 3 #3.25 # Wheels are ~6.5 cm diameter. 
CHASS_WID = 9#13.5 # Chassis is ~13.5 cm wide.
SAFE_DIST = 10 #Defaut safe front distance to the object. Set to avoid collision
TIME_LIMIT = 5 #limit maximum time on move robot in wait function: solving robot stuck at a location.

def left_deg(deg=None):
    '''
    Turn chassis left by a specified number of degrees.
    DPR is the #deg/pulse (Deg:Pulse ratio)
    This function sets the encoder to the correct number
     of pulses and then invokes left().
    '''
    if deg is not None:
        pulse= int(deg/DPR)
        enc_tgt(0,1,pulse)
    left()

def left_deg_wait(deg=None):
    '''
    Turn chassis left by a specified number of degrees.
    DPR is the #deg/pulse (Deg:Pulse ratio)
    This function sets the encoder to the correct number
     of pulses and then invokes left().
     Block the program until movement finish
    '''
    if deg is not None:
        pulse= int(deg/DPR)
        enc_tgt(0,1,pulse)
	#print(enc_read(1))
    left()
    start_time=time.time()  #if take more than 10 (TIME_LIMIT) seconds 
    while enc_read(1) < pulse and time.time()-start_time<TIME_LIMIT and GoatbotV3.check_flame_sensor_A()!=1:
		pass
	


def right_deg(deg=None):
    '''
    Turn chassis right by a specified number of degrees.
    DPR is the #deg/pulse (Deg:Pulse ratio)
    This function sets the encoder to the correct number
     of pulses and then invokes right().
    '''
    if deg is not None:
        pulse= int(deg/DPR)
        enc_tgt(1,0,pulse)
    right()

def right_deg_wait(deg=None):
    '''
    Turn chassis right by a specified number of degrees.
    DPR is the #deg/pulse (Deg:Pulse ratio)
    This function sets the encoder to the correct number
     of pulses and then invokes right().
     Block the program until movement finish
    '''
    if deg is not None:
        pulse= int(deg/DPR)
        enc_tgt(1,0,pulse)
    right()
    start_time=time.time()  #if take more than 10 (TIME_LIMIT) seconds
    while enc_read(0) < pulse and time.time()-start_time<TIME_LIMIT and GoatbotV3.check_flame_sensor_A()!=1:
		pass

def right_rot_deg(deg=None):
    '''
    Turn chassis right by a specified number of degrees.
    DPR is the #deg/pulse (Deg:Pulse ratio)
    This function sets the encoder to the correct number
     of pulses and then invokes right().
    '''
    if deg is not None:
        pulse= int(deg/DPR)/2
        enc_tgt(1,1,pulse)
    right_rot()

def right_rot_deg_wait(deg=None,no_flame_sensor=None):
    '''
    Turn chassis right by a specified number of degrees.
    DPR is the #deg/pulse (Deg:Pulse ratio)
    This function sets the encoder to the correct number
     of pulses and then invokes right().
     Block the program until movement finish
    '''
    if deg is not None:
        pulse= int(deg/DPR)/2
        enc_tgt(1,1,pulse)
    right_rot()
    flame_sensor_reading=GoatbotV3.check_flame_sensor_A()
    if no_flame_sensor is not None:
		flame_sensor_reading=0
    start_time=time.time()  #if take more than 10 (TIME_LIMIT) seconds
    while enc_read(0) < pulse and time.time()-start_time<TIME_LIMIT and flame_sensor_reading!=1:
		pass

def left_rot_deg(deg=None):
    '''
    Turn chassis right by a specified number of degrees.
    DPR is the #deg/pulse (Deg:Pulse ratio)
    This function sets the encoder to the correct number
     of pulses and then invokes right().
    '''
    if deg is not None:
        pulse= int(deg/DPR)/2
        enc_tgt(1,1,pulse)
    left_rot()

def left_rot_deg_wait(deg=None, no_flame_sensor=None):
    '''
    Turn chassis right by a specified number of degrees.
    DPR is the #deg/pulse (Deg:Pulse ratio)
    This function sets the encoder to the correct number
     of pulses and then invokes right().
     Block the program until movement finish
    '''
    if deg is not None:
        pulse= int(deg/DPR)/2
        enc_tgt(1,1,pulse)
    left_rot()
    flame_sensor_reading=GoatbotV3.check_flame_sensor_A()
    if no_flame_sensor is not None:
		flame_sensor_reading=0
    start_time=time.time()  #if take more than 10 (TIME_LIMIT) seconds
    while enc_read(1) < pulse and time.time()-start_time<TIME_LIMIT and flame_sensor_reading!=1:
		pass

def fwd_cm(dist=None):
    '''
    Move chassis fwd by a specified number of cm.
    This function sets the encoder to the correct number
     of pulses and then invokes fwd().
    '''
    if dist is not None:
        pulse = int(cm2pulse(dist))
        enc_tgt(1,1,pulse)
    fwd()
    

def fwd_cm_wait(dist=None):
    '''
    Move chassis fwd by a specified number of cm.
    This function sets the encoder to the correct number
     of pulses and then invokes fwd().
     Block the program until movement finish
    '''
    if dist is not None:
        pulse = int(cm2pulse(dist))
        enc_tgt(1,1,pulse)
    fwd()
    start_time=time.time()  #if take more than 10 (TIME_LIMIT) seconds
    while (enc_read(0) < pulse or enc_read(1) < pulse) and time.time()-start_time<TIME_LIMIT and GoatbotV3.check_flame_sensor_A()!=1 :
		pass
    #print(enc_read(0))
    #print(enc_read(1))
  
def fwd_cm_wait_avoid(dist=None,distance_to_stop=None, no_flame_sensor=None):
    '''
    Move chassis fwd by a specified number of cm.
    This function sets the encoder to the correct number
     of pulses and then invokes fwd().
     Block the program until movement finish
    '''
    if dist is not None:
        pulse = int(cm2pulse(dist))
        enc_tgt(1,1,pulse)
    fwd()
    if distance_to_stop is None:
        distance_to_stop=SAFE_DIST
    else:
        pass
    flame_sensor_reading=GoatbotV3.check_flame_sensor_A()
    if no_flame_sensor is not None:
		flame_sensor_reading=0
    start_time=time.time()  #if take more than 10 (TIME_LIMIT) seconds
    while (enc_read(0) < pulse or enc_read(1) < pulse) and time.time()-start_time<TIME_LIMIT and flame_sensor_reading!=1 :
        dist=us_dist(15)
        if dist<distance_to_stop:
            stop()
            break
        pass
    #print(enc_read(0))
    #print(enc_read(1))

def fwd_time_avoid(time_to_move,distance_to_stop=None):
   
    fwd()
    if distance_to_stop is None:
        distance_to_stop=SAFE_DIST
    start_time=time.time()
    while time.time()-start_time<time_to_move:   
		if dist<distance_to_stop:
			stop()
	
   
	

def bwd_cm(dist=None):
    '''
    Move chassis bwd by a specified number of cm.
    This function sets the encoder to the correct number
     of pulses and then invokes bwd().
    '''
    if dist is not None:
        pulse = int(cm2pulse(dist))
        enc_tgt(1,1,pulse)
    bwd()
    
def bwd_cm_wait(dist=None):
    '''
    Move chassis bwd by a specified number of cm.
    This function sets the encoder to the correct number
     of pulses and then invokes bwd().
     Block the program until movement finish
    '''
    if dist is not None:
        pulse = int(cm2pulse(dist))
        enc_tgt(1,1,pulse)
    bwd()
    while enc_read(0) < pulse or enc_read(1) < pulse and GoatbotV3.check_flame_sensor_A()!=1 :
		pass

def cm2pulse(dist):
    '''
    Calculate the number of pulses to move the chassis dist cm.
    pulses = dist * [pulses/revolution]/[dist/revolution]
    '''
    wheel_circ = 2*math.pi*WHEEL_RAD # [cm/rev] cm traveled per revolution of wheel
    revs = dist/wheel_circ
    PPR = 18 # [p/rev] encoder Pulses Per wheel Revolution
    pulses = PPR*revs # [p] encoder pulses required to move dist cm.
    if en_debug:
        print 'WHEEL_RAD',WHEEL_RAD
        print 'revs',revs
        print 'pulses',pulses
    return pulses

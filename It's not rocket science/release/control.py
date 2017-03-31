#!/usr/bin/python
'''
IMPORTANT: this version is for rocketbot
This module contains convenience functions to simplify
the coding of FireFighting contest tasks.

This really needs to be moved to a GoPiGo package
e.g. from gopigo.control import *
'''


from gopigo import *

en_debug=1

## 360 roation is ~64 encoder pulses or 5 deg/pulse
## DPR is the Deg:Pulse Ratio or the # of degrees per
##  encoder pulse.
DPR = 360.0/310 #360.0/64 goatbot 360.0/50 . Rocketbot 
WHEEL_RAD = 3.0/2 #3.25 # Wheels are ~6.5 cm diameter. Rocketbot is 3 cm diameter
CHASS_WID = 18#13.5 # Chassis is ~13.5 cm wide. Goatbot 9. Rocketbo 18

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
    while enc_read(1) < pulse:
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
    while enc_read(0) < pulse:
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

def right_rot_deg_wait(deg=None):
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
    while enc_read(0) < pulse:
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

def left_rot_deg_wait(deg=None):
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
    while enc_read(1) < pulse:
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
    while enc_read(0) < pulse or enc_read(1) < pulse :
		pass
    #print(enc_read(0))
    #print(enc_read(1))
    
	

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
    while enc_read(0) < pulse or enc_read(1) < pulse :
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

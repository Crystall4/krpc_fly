# -*- coding: utf-8 -*-

import engine
aircraft_status = {0:"Off",1:"warm-up",2:"TakeOff mode",3:"Cruise mode",4:"Landing mode",5:"Forsage maneur mode"}
		
class Aircraft:
	name                = ""
	krpc_disp           = None
	maxAtDeg            = 5.0
	minAtDeg            = -7.0
	minVERTICALSPEED    = -10.0
	maxVERTICALSPEED    = 15.0
	workVERTICALSPEED   = 15
	maxRoll             = 45
	maxDeg              = 180
	dVERTICALSPEED      = 1.2
	KVERTSPEED          = 60 
	MaxTakeoffMass      = 15000
	mass0               = 12230
	landingspeed0       = 120
	Klandingspeed       = 1.8
	TrottleKp           = 0.35 #0.220
	TrottleKi           = 0.0003
	TrottleKd           = 0.4
	headingKp           = 0.075
	headingKi           = 0.000001
	headingKd           = 0.150
	KRazogrevTrust      = 0.1
	preRunwayHill       = 10
	preRunwayMinTrottle = 0.1
	preRunwayminAtDeg   = -3.0
	RunwayHill          = 10
	CruiseSpeed         = 140
	ClimbMaxPitch       = 5.0
	ClimbMinPitch       = 1.0
	ClimbTrottle        = 0.75
	engines             = None
	
	def __init__(self):
		self.name = ""
		
	def landingspeed(self):
		return self.landingspeed0+(self.landingspeed0*(((vessel.mass-self.mass0)/self.mass0)/self.Klandingspeed))
	
	def pre_fly(self):
		return True
		
	def pre_take_off(self,VPP,First_dot):
		return True
		
	def start_engines(status):
		return False
		


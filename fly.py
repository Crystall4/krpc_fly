#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
sys.path.append("./lib")
import importlib
from tools import *

import math
import krpc
import time
import pid

#airc_str='Aeris_4A_atmos'
sys.path.append("./aircrafts")
#globals().update(importlib.import_module(airc_str).__dict__)


#======================================================================================================================
#импорт модулей ВПП
vpp_str='KSC'
sys.path.append("./runways")
globals().update(importlib.import_module(vpp_str).__dict__)
vpp_str='iceland'
globals().update(importlib.import_module(vpp_str).__dict__)


type_flight={0:"TakeOff and Landing", 1:"Landing to", 2:"TakeOff From", 3:"Cruise and Landing", 4:"TakeOff and Cruise"}
type_point ={0:"VPP", 1:"unequipped runway", 2:"Water", 3:"Space", 4:"Waypoint", 5:"Point", 6:"Zone"}


class route_stage:
	stage_type = None
	stage_data = None

class fly_plan:
	name=''
	aircraft_name = None
	begin_name    = None
	end_name      = None
	flight_name   = ''
	aircraft      = None
	begin         = None
	end           = None
	SID           = None
	STAR          = None
	route         = []
	compiled      = False
	def plan_compile(self):
		result=False
		if self.aircraft_name != None:
			try:
				#======================================================================================================================
				# импорт модуля ЛА
				globals().update(importlib.import_module(self.aircraft_name).__dict__)
				if basic_aircraft != None :
					self.aircraft = basic_aircraft
					log("Аппарат "+self.aircraft_name+" подключен успешно")
					result = True
			except:
				log("подключение эиркрафта неудачно")
			finally:
				pass
		if self.begin_name != None:
			
				
			pass
		#=============================================================================================================
		# Построение пути полета
		
		if self.begin.stage_type == 0:
			if len(self.route) > 0:
				pass
			elif self.flplan.end.stage_type == 0:
				tp = self.flplan.end.stage_data
		
		self.compiled = result
		return result

class fly_ap:
	
	def __init__(self, flplan):
		self.status = "PreInit"
		self.flplan   = flplan
		if self.flplan.compiled:
			self.name     = flplan.flight_name
			self.aircraft = flplan.aircraft
			self.AtDeg    = 0.0
			self.maxAtDeg = self.aircraft.maxAtDeg
			self.minAtDeg = self.aircraft.minAtDeg
			self.minVERTICALSPEED  = self.aircraft.minVERTICALSPEED
			self.maxVERTICALSPEED  = self.aircraft.maxVERTICALSPEED
			self.workVERTICALSPEED = self.aircraft.workVERTICALSPEED
			self.tALTITUDE = 1000.0
			self.tsleep    = 0.3
			self.CruiseSpeed = self.aircraft.CruiseSpeed
			self.TrottlePid  = pid.AviaPID(self.aircraft.TrottleKp,self.aircraft.TrottleKi,self.aircraft.TrottleKd)
			self.headingPid  = pid.AviaPID(self.aircraft.headingKp,self.aircraft.headingKi,self.aircraft.headingKd, -7, 7)
			self.krpc_connection()
			self.file_log    = False
			self.console_log = True
			self.old_met     = self.vessel.met
			self.status = "Ok"
		else:
			self.status = "Failed"
	
	def krpc_connection(self):
		result = False
		try:
			#-------------------------------------------------------------------------------------------------------------
			# Connect to the server with the default settings
			# (IP address 127.0.0.1 and port 50000)
			log('Connecting to server...')
			self.ksp = krpc.connect(name=self.name)
			#-------------------------------------------------------------------------------------------------------------
		except:
			log("Ошибка подключения к KRPC")
		else:
			print 'Connected to server, version', self.ksp.krpc.get_status().version
			self.space_center = self.ksp.space_center
			self.vessel       = self.space_center.active_vessel
			self.orbit        = self.vessel.orbit
			self.ap           = self.vessel.auto_pilot
			self.control      = self.vessel.control
			self.flight       = self.vessel.flight()
			self.surf_flight  = self.vessel.flight(self.orbit.body.reference_frame)
			self.resources    = self.vessel.resources
			result = True
		return result			
	def pre_fly(self):
		self.aircraft.pre_fly(self.vessel)
		self.ap.max_roll_speed = 0.5
		self.ap.roll_speed_multiplier = 0.5
		#self.ap.set_pid_parameters(75,50,25)
		self.ap.max_rotation_speed = 1
		self.ap.rotation_speed_multiplier = 1
		self.ap.engage()
	def calc_VerticalSpeed(self):
		self.TVertSpeed=(self.tALTITUDE-self.flight.mean_altitude)/abs((self.tLATLONG.dist_line(self.aircraft.curr_position())-(self.tLATLONG.dist_line(self.aircraft.curr_position())*0.1))/self.surf_flight.horizontal_speed)
		return self.TVertSpeed
	def calc_AtDeg(self):
		self.AtDeg = self.AtDeg + (((self.TVertSpeed*self.aircraft.dVERTICALSPEED) - self.surf_flight.vertical_speed)/self.aircraft.KVERTSPEED)
		if self.AtDeg > self.maxAtDeg:
			self.AtDeg = self.maxAtDeg
		if self.AtDeg < self.minAtDeg:
			self.AtDeg = self.minAtDeg
	def calc_Heading_and_Roll(self):
		 t=self.tLATLONG.bearing_line(self.aircraft.curr_position())-self.flight.heading
		 self.tHeading = self.flight.heading
		 if t>360:
		   t=t-360
		 if t>180 or (t<0 and t>-180):
		   self.AtRoll = max(0-self.aircraft.maxRoll, 0-abs(t))
		   self.tHeading =  self.tHeading + max(0-self.aircraft.maxDeg,0-abs(t))
		 else:
		   self.AtRoll = min(self.aircraft.maxRoll,abs(t))
		   self.tHeading = self.tHeading + min(self.aircraft.maxDeg,abs(t))
		 if self.surf_flight.surface_altitude <= 90:
			self.AtRoll = 0	
	def calc_Trottle(self):
		self.TTrottle = self.TrottlePid.update(self.surf_flight.horizontal_speed,self.vessel.met)
		if self.TTrottle > self.maxTrottle:
			self.TTrottle = self.maxTrottle
		if self.TTrottle < self.minTrottle:
			self.TTrottle = self.minTrottle
	def pre_take_off(self,VPP,First_dot):
		self.aircraft.pre_take_off()
		self.pre_fly()
		self.control.throttle = 0
		#-------------------------------------------------
		self.control.sas = False
		self.control.rcs = False
		self.control.gear = True
		self.control.brakes = True
		self.control.wheel_steering = 0
		self.SID=VPP.get_SID(First_dot)
		self.tLATLONG = self.SID[0]
		self.ap.target_pitch_and_heading(0.45, self.tLATLONG.bearing_line(self.aircraft.curr_position()))
	def take_off(self,VPP,First_dot):
		self.pre_take_off(VPP)
		self.aircraft.start_engines()
		#print 'Razogrev'
		#self.control.throttle = 0
		#if self.vessel.available_thrust == 0.0 :
			#self.control.activate_next_stage()
			#time.sleep(0.2)
		#self.control.throttle = 1
		self.control.lights = True
		while ((self.vessel.thrust) < (self.vessel.available_thrust * self.aircraft.KRazogrevTrust)) and self.surf_flight.speed < 5:
		 time.sleep(0.5)
		#print 'Probeg'
		self.control.brakes = False
		while self.surf_flight.speed < self.aircraft.landingspeed() and self.surf_flight.surface_altitude < 10:
			self.ap.target_pitch_and_heading(0.45, self.tLATLONG.bearing_line(self.aircraft.curr_position()))
			self.vessel.auto_pilot.target_roll = 0
			time.sleep(0.1)
		#print 'Otrblv'
		self.control.toggle_action_group(9)
		while surf_flight.surface_altitude < 15:
			self.ap.target_pitch_and_heading(3.0, self.tLATLONG.bearing_line(self.aircraft.curr_position()))
			self.vessel.auto_pilot.target_roll = 0
			time.sleep(0.1)
		self.control.gear = False
		self.control.lights = False
		for d in self.SID[1:]:
			self.climb(d.alt,d)
	def climb(self,alt=1000,targetDot=''):
		state = "Climb up to "+alt
		self.maxTrottle = self.aircraft.ClimbTrottle
		self.minTrottle = self.aircraft.ClimbTrottle
		self.maxAtDeg = self.aircraft.ClimbMaxPitch
		self.minAtDeg = self.aircraft.ClimbMinPitch
		while self.flight.mean_altitude < tALTITUDE:
			self.run(state,"estimated climb times: {}".format(sec_to_time((alt-self.flight.mean_altitude)/(self.surf_flight.vertical_speed+0.0000000000001))))
	def landing(self,VPP):
		#Select direction
		
		curr_glis_point = glis_point(beg_r,end_r,12000)
		#"Razvorot"
		turn(curr_glis_point)
		state = 'preRunway' 
		self.minTrottle = self.aircraft.preRunwayMinTrottle
		self.minAtDeg   = self.aircraft.preRunwayminAtDeg
		curr_glis_point.alt=beg_r.alt+self.aircraft.preRunwayHill
		self.Cruise(curr_glis_point,1000)
		state = 'Runway'
		self.tLATLONG = beg_r
		self.tALTITUDE = beg_r.alt+self.aircraft.RunwayHill
		self.minAtDeg = -7.0
		self.TrottlePid.setPoint(self.aircraft.landingspeed())
		self.maxTrottle = 1.0
		self.minTrottle = 0.1
		self.control.gear = True
		self.control.lights = True
		while state != 'END':
			if state == 'Runway' and self.tLATLONG.dist_line(self.aircraft.curr_position()) < 150:
				state = 'Glissada'
				self.tLATLONG = end_r
				self.tALTITUDE = beg_r.alt+((self.aircraft.RunwayHill/2)*self.tLATLONG.dist_line(self.aircraft.curr_position())/150)
				self.TrottlePid.setPoint(0.1)
				self.maxTrottle = 0.1
				self.minTrottle = 0.1
				self.minAtDeg = -3.0
				self.control.brakes = True
			if state == 'Glissada' and surf_flight.surface_altitude < 5:
				self.tALTITUDE = beg_r.alt-20
				#print 'Kasanie', tLATLONG.dist_line(self.aircraft.curr_position()) 
				self.TrottlePid.setPoint(20)
				self.maxTrottle = 0.000000000000000
				self.minTrottle = 0.000000000000000
				self.control.brakes = True
			if state == 'Glissada' and surf_flight.horizontal_speed < 0.5:
				state = 'END'
				self.tLATLONG = end_r
				self.tALTITUDE = beg_r.alt-20
				self.TrottlePid.setPoint(0)
				self.maxTrottle = 0.0
				self.minTrottle = 0.0
				self.control.throttle = 0
				self.control.brakes = True	
			self.run(state,memo)
			memo =""
	def turn(self,targetDot):
		self.maxTrottle = 1.0
		state = "Turn from {}".format(targetDot.name)
		while abs(self.targetDot.bearing_line(self.aircraft.curr_position())-self.flight.heading)>10.0:
			memo = str(self.targetDot.bearing_line(self.aircraft.curr_position())-self.flight.heading)
			self.run(state,memo)
	def Cruise(self,targetDot,dist=500):
		state = "Cruise to {}".format(targetDot.name)
		self.tLATLONG = targetDot
		self.tALTITUDE = targetDot.alt
		self.TrottlePid.setPoint(self.aircraft.CruiseSpeed)
		while targetDot.dist_line(self.aircraft.curr_position()) < dist :
			self.run(state,"estimated flight times: {}".format(sec_to_time(targetDot.dist_line(self.aircraft.curr_position())/(self.surf_flight.horizontal_speed+0.0000000000001))))
	def log(self):
		self.log_file = open(self.log_fileName, 'a') 
		self.log_file.writeln(self.name +" "+ self.vessel.met)
		self.log_file.close()		
	def set_log_to_file(self,fileName="default"):
		self.file_log = True
		self.log_fileName=fileName+".log"
		self.log_file = open(self.log_fileName, 'w') 
		self.log_file.writeln(self.name +" "+ self.vessel.met)
		self.log_file.close()
		self.log_file.writeln("Mass: "+vessel.mass)
		self.log_file.writeln("Fuel: "+vessel.mass)
	def state_log(self,state, memo=""):
		log_string = state+";{met};{trottle};{horizontal_speed};{AtDeg};{pitch};{TVertSpeed};{vertical_speed};{AtRoll};{bearing};{tHeading};{tALTITUDE};{dist_line};{landingspeed};".format(\
			met				=format(self.vessel.met,'.2f'),\
			trottle			=format(self.TTrottle,'.3f'),\
			horizontal_speed=format(self.surf_flight.horizontal_speed,'.1f'), \
			AtDeg			=format(self.AtDeg,'+.3f'),\
			pitch			=format(self.flight.pitch,'+.3f'),\
			TVertSpeed  	=format(self.TVertSpeed,'+.3f'),\
			vertical_speed	=format( self.surf_flight.vertical_speed,'+.3f'),\
			AtRoll			=format( self.AtRoll,'+.3f'),\
			bearing			=format(self.tLATLONG.bearing_line(self.aircraft.curr_position()),'.3f'),\
			tHeading		=format( self.tHeading,'.3f'),\
			tALTITUDE		=format( self.tALTITUDE,'.1f'),\
			dist_line		=format(  self.tLATLONG.dist_line(self.aircraft.curr_position()),'.1f'),\
			landingspeed	=format( self.aircraft.landingspeed(),'.3f'))\
			+memo
		if self.file_log:
			self.log_file = open(self.log_fileName, 'a')
			self.log_file.writeln(log_string)		
			self.log_file.close()
		if self.console_log:
			print log_string
	def run(self,state,memo=""):
		self.calc_Trottle()
		self.calc_VerticalSpeed()
		self.calc_AtDeg()
		self.calc_Heading_and_Roll()
		if surf_flight.horizontal_speed<(self.aircraft.landingspeed()*1.05):
			control.toggle_action_group(9)
		else:
			control.toggle_action_group(0)
		if abs(self.tHeading-flight.heading)>0.3:
			ap.target_pitch_and_heading(self.AtDeg, self.tHeading)
		else:
			ap.target_pitch_and_heading(self.AtDeg, flight.heading)
		vessel.auto_pilot.target_roll = self.AtRoll
		control.throttle = self.TTrottle
		self.state_log(state,memo)
		time.sleep(self.tsleep)
	def Go(self):
		if self.status != 'Ok': return 'Error'
		if len(self.route) > 0:
			self.take_off(self.flplan.begin.stage_data,self.flplan.route[0].stage_data)



import math
import krpc
import time
import pid

# Connect to the server with the default settings
# (IP address 127.0.0.1 and port 50000)
print 'Connecting to server...'
ksp = krpc.connect(name='Fly_heavy')
print 'Connected to server, version', ksp.krpc.get_status().version

space_center = ksp.space_center
vessel = space_center.active_vessel
orbit = vessel.orbit
ap = vessel.auto_pilot
control = vessel.control
flight = vessel.flight()
surf_flight = vessel.flight(orbit.body.reference_frame)
resources = vessel.resources

control.throttle = 0
ap.max_roll_speed = 0.5
ap.roll_speed_multiplier = 0.5
#ap.set_pid_parameters(75,50,25)
ap.max_rotation_speed = 1
ap.rotation_speed_multiplier = 1

class coordinates:
 lat=0.0
 lng=0.0
 alt=0.0
 name=''
 def get(self):
  return dict(name=self.name, lat=self.lat, lng=self.lng, alt=self.alt)
 def set(self, lat, lng, alt=0, name=''):
  self.lat=lat
  self.lng=lng
  self.name=name
  self.alt=alt
 def __repr__(self):
  return dict(name=self.name, lat=self.lat, lng=self.lng, alt=self.alt)
 def __str__(self):
  return 'Coordinates {}: {}, {}, {}'.format(self.name, self.lat, self.lng, self.alt)
 def __init__(self, lat=0.0, lng=0.0, alt=0, name=''):
  self.lat=lat
  self.lng=lng
  self.name=name
  self.alt=alt
 def dist_deg(self):
  return math.sqrt(((self.lat - flight.latitude)**2)+((self.lng - flight.longitude)**2))
 def dist_line(self):
  return math.sqrt(((self.lat - flight.latitude)**2)+((self.lng - flight.longitude)**2))*10471.97333333
 def dist_gc(self):
  rad = 600000
  lat1 = flight.latitude*math.pi/180.
  lat2 = self.lat*math.pi/180.
  long1 = flight.longitude*math.pi/180.
  long2 = self.lng*math.pi/180.
  cl1 = math.cos(lat1)
  cl2 = math.cos(lat2)
  sl1 = math.sin(lat1)
  sl2 = math.sin(lat2)
  delta = long2 - long1 
  cdelta = math.cos(delta)
  sdelta = math.sin(delta)
  y = math.sqrt(math.pow(cl2*sdelta,2)+math.pow(cl1*sl2-sl1*cl2*cdelta,2))
  x = sl1*sl2+cl1*cl2*cdelta
  ad = math.atan2(y,x)
  return ad*rad 
 def bearing_gc(self):
  rad = 600000
  lat1 = flight.latitude*math.pi/180.
  lat2 = self.lat*math.pi/180.
  long1 = flight.longitude*math.pi/180.
  long2 = self.lng*math.pi/180.
  cl1 = math.cos(lat1)
  cl2 = math.cos(lat2)
  sl1 = math.sin(lat1)
  sl2 = math.sin(lat2)
  delta = long2 - long1 
  cdelta = math.cos(delta)
  sdelta = math.sin(delta)
  x = (cl1*sl2) - (sl1*cl2*cdelta)
  y = sdelta*cl2
  z = math.degrees(math.atan(-y/x))
  if (x < 0):
    z = z+180.
  z2 = (z+180.) % 360. - 180.
  z2 = - math.radians(z2)
  anglerad2 = z2 - ((2*math.pi)*math.floor((z2/(2*math.pi))) )  
  return (anglerad2*180.)/math.pi
 def bearing_line(self):
	dX = (flight.longitude) - (self.lng) 
	dY = (flight.latitude)  - (self.lat)
	dist = math.sqrt((dX**2) + (dY**2))
	dXa = abs(dX)
	beta = math.degrees(math.acos(dXa / dist))
	if dX > 0:
		if dY < 0:
			angle = 270 + beta
		else:
			angle = 270 - beta
	else:
		if dY < 0:
			angle = 90 - beta
		else:
			angle = 90 + beta
	return angle

def glis_point(runway_beg, runway_stop, dist):
  dist_t = dist/(math.sqrt(((runway_beg.lat - runway_stop.lat)**2)+((runway_beg.lng - runway_stop.lng)**2))*10471.97333333)
  glis_dot = coordinates(name='glis_point', lat=(runway_beg.lat+dist_t*(runway_beg.lat-runway_stop.lat)), lng=(runway_beg.lng+dist_t*(runway_beg.lng-runway_stop.lng)), alt=(dist*0.1)+70.0)
  return glis_dot

def dist_to_line(runway_beg, runway_stop, curr_point):
  point_dist=((runway_beg.lng-runway_stop.lng)*curr_point.lat+(runway_stop.lat-runway_beg.lat)*curr_point.lng+(runway_beg.lat*runway_stop.lng-runway_stop.lat*runway_beg.lng))/math.sqrt(((runway_beg.lng-runway_stop.lng)**2)+((runway_stop.lat-runway_beg.lat)**2))
  return point_dist*10471.97333333

def dist_from_line(runway_beg, runway_stop, curr_point):
  cf=((curr_point.lat-runway_beg.lat)*(runway_stop.lat-runway_beg.lat)+(curr_point.lng-runway_beg.lng)*(runway_stop.lng-runway_beg.lng))/((runway_beg.lat-runway_stop.lat)**2+(runway_beg.lng-runway_stop.lng)**2)
  pp_x=runway_beg.lat+cf*(runway_stop.lat-runway_beg.lat)
  pp_y=runway_beg.lng+cf*(runway_stop.lng-runway_beg.lng)
  return math.sqrt(((runway_beg.lat - pp_x)**2)+((runway_beg.lng - pp_y)**2))*10471.97333333

def dist_from_line_deg(runway_beg, runway_stop, curr_point):
  cf=((curr_point.lat-runway_beg.lat)*(runway_stop.lat-runway_beg.lat)+(curr_point.lng-runway_beg.lng)*(runway_stop.lng-runway_beg.lng))/((runway_beg.lat-runway_stop.lat)**2+(runway_beg.lng-runway_stop.lng)**2)
  pp_x=runway_beg.lat+cf*(runway_stop.lat-runway_beg.lat)
  pp_y=runway_beg.lng+cf*(runway_stop.lng-runway_beg.lng)
  return math.sqrt(((runway_beg.lat - pp_x)**2)+((runway_beg.lng - pp_y)**2))

def dog_curves_point(runway_beg, runway_stop, curr_point):
  d=dist_from_line(runway_beg, runway_stop, curr_point)/2
  res = glis_point(runway_beg, runway_stop, d)
  return res

#=====================================================================================================================  
runwayWest    = coordinates(name='runwayWest',   lat=-0.04855056049336841, lng=-74.72449313835466000,  alt=70.0 )
runwayEast    = coordinates(name='runwayEast',   lat=-0.05025878770915180, lng=-74.48951284451766242,  alt=70.0 )
icelandEast   = coordinates(name='icelandEast',  lat=-1.51671773150452880,  lng=-71.88368709972201000, alt=135.2)
icelandWest   = coordinates(name='icelandWest',  lat=-1.51772268480006560,  lng=-71.96820722802198000, alt=135.2)
#---------------------------------------------------------------------------------------------------------------------
recursive_dot  = coordinates(name='recursive_dot', lat=-0.02022509861205912, lng=-72.18951284451766242, alt=1000.0)
recursive_dot1 = coordinates(name='recursive_dot', lat=-0.02022509861205912, lng=-76.18951284451766242, alt=600.0)
two_dot =       coordinates(name='two_dot',        lat=1.35022509861205912, lng=-70.48951284451766242, alt=1000.0)
#======================================================================================================================
class VPP:
	edge1 = ''
	edge2 = ''
	def __init__(self, edge1, edge2):
		self.edge1=edge1
		self.edge2=edge2
	
KSP_VPP =VPP(runwayWest,runwayEast)
iceland_VPP= VPP(icelandEast,icelandWest)

class Aircraft:
	name =""
	maxAtDeg = 5.0
	minAtDeg = -7.0
	minVERTICALSPEED = -10.0
	maxVERTICALSPEED = 15.0
	workVERTICALSPEED = 15
	maxRoll = 45
	maxDeg = 180
	dVERTICALSPEED = 1.2
	KVERTSPEED = 60 
	MaxTakeoffMass=15000
	mass0=12230
	landingspeed0 = 120
	Klandingspeed = 1.8
	TrottleKp = 0.35#0.220
	TrottleKi = 0.0003
	TrottleKd = 0.4
	headingKp = 0.075
	headingKi = 0.000001
	headingKd = 0.150
	KRazogrevTrust = 0.1
	def __init__(self):
		name =""
		landingspeed0 = 70
		
	def landingspeed(self):
		return self.landingspeed0+(self.landingspeed0*(((vessel.mass-self.mass0)/self.mass0)/self.Klandingspeed))
	
class fly:
	aircraft=Aircraft()
	def __init__(self):
		self.AtDeg = 0.0
		self.maxAtDeg = self.aircraft.maxAtDeg
		self.minAtDeg = self.aircraft.minAtDeg
		self.minVERTICALSPEED = self.aircraft.minVERTICALSPEED
		self.maxVERTICALSPEED = self.aircraft.maxVERTICALSPEED
		self.workVERTICALSPEED = self.aircraft.workVERTICALSPEED
		self.tALTITUDE = 1000.0
		self.tsleep = 0.3
		self.TrottlePid=pid.AviaPID(self.aircraft.TrottleKp,self.aircraft.TrottleKi,self.aircraft.TrottleKd) 
		self.headingPid=pid.AviaPID(self.aircraft.headingKp,self.aircraft.headingKi,self.aircraft.headingKd, -7, 7)
		self.old_met=vessel.met
	def pre_fly(self):
		ap.engage()
	def pre_take_off(self,VPP):
		self.pre_fly()
		ap.target_pitch_and_heading(0.45, 90.40)
		control.sas = False
		control.rcs = False
		control.gear = True
		control.brakes = True
		control.wheel_steering = 0
		if  VPP.edge1.dist_line() > VPP.edge2.dist_line():
			self.tLATLONG = VPP.edge1
		else:
			self.tLATLONG = VPP.edge2
		ap.target_pitch_and_heading(0.45, self.tLATLONG.bearing_line())
	def take_off(self,VPP):
		self.pre_take_off(VPP)
		#print 'Razogrev'
		control.throttle = 0
		if vessel.available_thrust == 0.0 :
			control.activate_next_stage()
			time.sleep(0.2)
		control.throttle = 1
		control.lights = True
		while ((vessel.thrust) < (vessel.available_thrust * self.aircraft.KRazogrevTrust)) and surf_flight.speed < 5:
		 time.sleep(0.5)
		#print 'Probeg'
		control.brakes = False	
		while surf_flight.speed < self.aircraft.landingspeed() and surf_flight.surface_altitude < 10:
			ap.target_pitch_and_heading(0.45, self.tLATLONG.bearing_line())
			vessel.auto_pilot.target_roll = 0
			time.sleep(0.1)
		#print 'Otrblv'
		control.toggle_action_group(9)
		while surf_flight.surface_altitude < 15:
			ap.target_pitch_and_heading(3.0, self.tLATLONG.bearing_line())
			vessel.auto_pilot.target_roll = 0
			time.sleep(0.1)
		control.gear = False
		control.lights = False
	def calc_VerticalSpeed(self):
		self.TVertSpeed=(self.tALTITUDE-flight.mean_altitude)/abs((self.tLATLONG.dist_line()-(self.tLATLONG.dist_line()*0.1))/surf_flight.horizontal_speed)
		return self.TVertSpeed
	def calc_AtDeg(self):
		self.AtDeg = self.AtDeg + (((self.TVertSpeed*self.aircraft.dVERTICALSPEED) - surf_flight.vertical_speed)/self.aircraft.KVERTSPEED)
		if self.AtDeg > self.maxAtDeg:
			self.AtDeg = self.maxAtDeg
		if self.AtDeg < self.minAtDeg:
			self.AtDeg = self.minAtDeg
	def calc_Heading_and_Roll(self):
		 t=self.tLATLONG.bearing_line()-flight.heading
		 self.tHeading = flight.heading
		 if t>360:
		   t=t-360
		 if t>180 or (t<0 and t>-180):
		   self.AtRoll = max(0-self.aircraft.maxRoll, 0-abs(t))
		   self.tHeading =  self.tHeading + max(0-self.aircraft.maxDeg,0-abs(t))
		 else:
		   self.AtRoll = min(self.aircraft.maxRoll,abs(t))
		   self.tHeading = self.tHeading + min(self.aircraft.maxDeg,abs(t))	 
		 if surf_flight.surface_altitude <= 90:
			self.AtRoll = 0	
	def calc_Trottle(self):
		self.TTrottle = self.TrottlePid.update(surf_flight.horizontal_speed,vessel.met)
		if self.TTrottle > self.maxTrottle:
			self.TTrottle = self.maxTrottle
		if self.TTrottle < self.minTrottle:
			self.TTrottle = self.minTrottle
	def landing(self,VPP):
		
		state = "Razvorot"
		#Select direction
		if VPP.edge1.dist_line() < VPP.edge2.dist_line():
			beg_r = VPP.edge1
			end_r = VPP.edge2
			print "Sit to East direction runway"  
		else:
			beg_r = VPP.edge2
			end_r = VPP.edge1
		print "Sit to", beg_r.name," direction runway"
		self.tLATLONG = glis_point(beg_r,end_r,12000)
		self.maxTrottle = 1.0
		self.minTrottle = 0.1
		while state != 'END':
			self.run()
			if (state == "Razvorot" and abs(self.tLATLONG.bearing_line()-flight.heading)<10.0):
				state = 'preRunway' 
				self.TrottlePid.setPoint(160)
				self.tALTITUDE = beg_r.alt+10
				self.minTrottle = 0.1
				self.minAtDeg =-7.5
			if state == 'preRunway' and self.tLATLONG.dist_line() < 1000:
				state = 'Runway'
				self.tLATLONG = beg_r
				self.tALTITUDE = beg_r.alt+10
				self.minAtDeg = -7.0
				self.TrottlePid.setPoint(self.aircraft.landingspeed())
				self.maxTrottle = 1.0
				self.minTrottle = 0.1
				#control.throttle = 0.3
				control.gear = True
				control.lights = True
			if state == 'Runway' and self.tLATLONG.dist_line() < 150:
				state = 'Glissada'
				self.tLATLONG = end_r
				self.tALTITUDE = beg_r.alt+5
				self.TrottlePid.setPoint(0.1)
				self.maxTrottle = 0.1
				self.minTrottle = 0.1
				self.minAtDeg = -3.0
				control.brakes = True
			if state == 'Glissada' and surf_flight.surface_altitude < 5:
				self.tALTITUDE = beg_r.alt-20
				#print 'Kasanie', tLATLONG.dist_line() 
				self.TrottlePid.setPoint(20)
				self.maxTrottle = 0.000000000000000
				self.minTrottle = 0.000000000000000
				control.brakes = True
			if state == 'Glissada' and surf_flight.horizontal_speed < 0.5:
				state = 'END'
				self.tLATLONG = end_r
				self.tALTITUDE = beg_r.alt-20
				self.TrottlePid.setPoint(0)
				self.maxTrottle = 0.0
				self.minTrottle = 0.0
				control.throttle = 0
				control.brakes = True	
			print state, ";%.3f;%.1f;%+.3f;%+.3f;%+.3f;%+.3f;%+.3f;%.3f;%.3f;%.1f;%.1f;%.3f;" % (self.TTrottle, surf_flight.horizontal_speed, self.AtDeg, flight.pitch, self.TVertSpeed, surf_flight.vertical_speed, self.AtRoll,self.tLATLONG.bearing_line(), self.tHeading, self.tALTITUDE,  self.tLATLONG.dist_line(),  self.aircraft.landingspeed())
	def run(self):
		self.calc_Trottle()
		self.calc_VerticalSpeed()
		self.calc_AtDeg()
		self.calc_Heading_and_Roll()
		if surf_flight.horizontal_speed<(self.aircraft.landingspeed()*1.05) :
			control.toggle_action_group(9)
		else:
			control.toggle_action_group(0)
		if abs(self.tHeading-flight.heading)>0.3:
			ap.target_pitch_and_heading(self.AtDeg, self.tHeading)
		else:
			ap.target_pitch_and_heading(self.AtDeg, flight.heading)
		vessel.auto_pilot.target_roll = self.AtRoll
		control.throttle = self.TTrottle
		time.sleep(self.tsleep)
		
#=====================================================================================================================			
Stearwing_A300 = Aircraft()
Stearwing_A300.name = "Stearwing A300"
Stearwing_A300.maxAtDeg = 7.0
Stearwing_A300.minAtDeg = -7.0
Stearwing_A300.minVERTICALSPEED = -10.0
Stearwing_A300.maxVERTICALSPEED = 15.0
Stearwing_A300.maxRoll = 30
Stearwing_A300.maxDeg = 45
Stearwing_A300.dVERTICALSPEED = 1.2
Stearwing_A300.KVERTSPEED = 90 
Stearwing_A300.MaxTakeoffMass=89100
Stearwing_A300.mass0=48600
Stearwing_A300.landingspeed0 = 70
Stearwing_A300.Klandingspeed = 1.8
Stearwing_A300.TrottleKp = 0.35#0.220
Stearwing_A300.TrottleKi = 0.0003
Stearwing_A300.TrottleKd = 0.4
Stearwing_A300.headingKp = 0.075
Stearwing_A300.headingKi = 0.000001
Stearwing_A300.headingKd = 0.150			
#---------------------------------------------------------------------------------------------------------------------
#=====================================================================================================================

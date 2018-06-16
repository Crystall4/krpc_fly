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
runwayWest    = coordinates(name='runwayWest',   lat=-0.04855056049336841, lng=-74.72449313835466000, alt=70.0)
runwayEast    = coordinates(name='runwayEast',   lat=-0.05025878770915180, lng=-74.48951284451766242, alt=70.0)
preRunwayEast = coordinates(name='preRunwayEast',lat=-0.07022509861205912, lng=-73.50451284451766242, alt=150.0)

recursive_dot = coordinates(name='recursive_dot', lat=-0.02022509861205912, lng=-70.18951284451766242, alt=1000.0)
two_dot =       coordinates(name='two_dot',        lat=1.35022509861205912, lng=-70.48951284451766242, alt=1000.0)
#======================================================================================================================


class fly:
	def __init__(self):
		self.AtDeg = 7.0
		self.maxAtDeg = 7.0
		self.minAtDeg = -7.0
		self.minVERTICALSPEED = -10.0
		self.maxVERTICALSPEED = 15.0
		self.workVERTICALSPEED = 15
		self.maxRoll = 30
		self.maxDeg = 45
		self.tALTITUDE = 1000.0
		self.tsleep = 0.3
		self.dVERTICALSPEED = 1.2
		self.KVERTSPEED = 60
		self.MaxTakeoffMass=89100
		self.mass0=48600
		self.landingspeed0 = 70
		self.Klandingspeed = 1.8
		self.TrottleKp = 0.35#0.220
		self.TrottleKi = 0.0003
		self.TrottleKd = 0.4
		self.TrottlePid=pid.AviaPID(self.TrottleKp,self.TrottleKi,self.TrottleKd) 
		self.headingKp = 0.075
		self.headingKi = 0.000001
		self.headingKd = 0.150
		self.headingPid=pid.AviaPID(self.headingKp,self.headingKi,self.headingKd, -7, 7)
		self.old_met=vessel.met
	def landingspeed(self):
		return self.landingspeed0+(self.landingspeed0*(((vessel.mass-self.mass0)/self.mass0)/self.Klandingspeed))
	def pre_fly(self):
		ap.engage()
	def pre_take_off(self):
		self.pre_fly()
		ap.target_pitch_and_heading(0.45, 90.40)
		#control.speed_mode = surface
		control.sas = False
		#control.sas = True
		control.rcs = False
		control.gear = True
		control.brakes = True
		control.wheel_steering = 0
		if  runwayEast.dist_line() > runwayWest.dist_line():
			#print "elevation to East direction runway"
			#print 'Distance line >> ', self.tLATLONG.dist_line(), ' [meters]'
			#print 'Distance >> ', self.tLATLONG.dist_line(), ' [meters]'
			self.tLATLONG = runwayEast
		else:
			#print "elevation to West direction runway"
			#print 'Distance line >> ', tLATLONG.dist_line(), ' [meters]'
			#print 'Distance >> ', tLATLONG.dist_line(), ' [meters]'
			self.tLATLONG = runwayWest
	def take_off(self):
		self.pre_take_off()
		#surf_flight.speed, surf_flight.vertical_speed, surf_flight.horizontal_speed
		#print 'Razogrev'
		control.throttle = 0
		if vessel.available_thrust == 0.0 :
			control.activate_next_stage()
			time.sleep(0.2)
		control.throttle = 1
		control.lights = True
		while ((vessel.thrust) < (vessel.available_thrust * 0.7)) and surf_flight.speed < 5:
		 time.sleep(0.5)
		#print 'Probeg'
		control.brakes = False	
		while surf_flight.speed < self.landingspeed() and surf_flight.surface_altitude < 10:
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
		self.AtDeg = self.AtDeg + (((self.TVertSpeed*self.dVERTICALSPEED) - surf_flight.vertical_speed)/self.KVERTSPEED)
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
		   self.AtRoll = max(0-self.maxRoll, 0-abs(t))
		   self.tHeading =  self.tHeading + max(0-self.maxDeg,0-abs(t))
		 else:
		   self.AtRoll = min(self.maxRoll,abs(t))
		   self.tHeading = self.tHeading + min(self.maxDeg,abs(t))	 
		 if surf_flight.surface_altitude <= 90:
			self.AtRoll = 0	
	def calc_Trottle(self):
		self.TTrottle = self.TrottlePid.update(surf_flight.horizontal_speed,vessel.met)
		if self.TTrottle > self.maxTrottle:
			self.TTrottle = self.maxTrottle
		if self.TTrottle < self.minTrottle:
			self.TTrottle = self.minTrottle
	def run(self):
		self.calc_Trottle()
		self.calc_VerticalSpeed()
		self.calc_AtDeg()
		self.calc_Heading_and_Roll()
		if surf_flight.horizontal_speed<(self.landingspeed()*1.05) :
			control.toggle_action_group(9)
		if abs(self.tHeading-flight.heading)>0.3:
			ap.target_pitch_and_heading(self.AtDeg, self.tHeading)
		else:
			ap.target_pitch_and_heading(self.AtDeg, flight.heading)
		vessel.auto_pilot.target_roll = self.AtRoll
		control.throttle = self.TTrottle
		time.sleep(self.tsleep)
		
			
			
			
testap = fly()
testap.take_off()
testap.tLATLONG = recursive_dot
state = 'Nabor Vblcotbl'
dDist = testap.tLATLONG.dist_line() /10
testap.TrottlePid.setPoint(160)
testap.maxTrottle = 1.0
testap.minTrottle = 1.0
testap.tALTITUDE = 1000
testap.minAtDeg =7.0
old_met=0

print "State; Trottle; HS; AtDeg; Pitch; AtRoll; tHeading;tAlt; tVertSp; dist_line; bearing; landingspeed;" 
while state != 'END':
 testap.run()
 

 if state == 'Nabor Vblcotbl' and surf_flight.speed < 120:
	control.toggle_action_group(0)

 if state == 'Nabor Vblcotbl' and surf_flight.surface_altitude >= testap.tALTITUDE:
	state = 'Recursive dot'
	testap.tALTITUDE =  testap.tLATLONG.alt
	testap.tALTITUDE = 2500
	testap.TrottlePid.setPoint(160)
	testap.maxTrottle = 1.0
	testap.minTrottle = 0.3
	testap.minAtDeg   =-2.0
	
 #if state == 'Recursive dot' and tLATLONG.dist_line() < 500:
	#state = 'Two dot'
	#tLATLONG = two_dot 
	#tALTITUDE = two_dot.alt
	#maxTrottle = 0.9
	#minTrottle = 0.3
		 
 if state == 'Two dot' and testap.tLATLONG.dist_line() < 500:
 	state = 'Revers to recursive_dot'
 	testap.tLATLONG = recursive_dot
 	testap.tALTITUDE = testap.tLATLONG.alt
 if state == 'Recursive dot' and testap.tLATLONG.dist_line() < 500:
	state = "Razvorot"
	#Select direction
	if runwayEast.dist_line() < runwayWest.dist_line():
		beg_r = runwayEast
		end_r = runwayWest
		print "Sit to East direction runway"  
	else:
		beg_r = runwayWest
		end_r = runwayEast
		print "Sit to West direction runway"
	testap.tLATLONG = glis_point(beg_r,end_r,12000)
	testap.maxTrottle = 1.0
	testap.minTrottle = 0.8
 if (state == "Razvorot" and abs(testap.tLATLONG.bearing_line()-flight.heading)<10.0):
	state = 'preRunway' 
	testap.tLATLONG.alt = 200
	testap.tALTITUDE = 200
	testap.TrottlePid.setPoint(150)
	testap.tALTITUDE = 80
	testap.minTrottle = 0.5
	testap.minAtDeg =-1.5
 if state == 'preRunway' and testap.tLATLONG.dist_line() < 1000:
	state = 'Runway'
	testap.tLATLONG = beg_r
	testap.tALTITUDE = 78
	testap.minAtDeg = -2
	testap.TrottlePid.setPoint(testap.landingspeed())
	testap.maxTrottle = 1.0
	testap.minTrottle = 0.65
	#control.throttle = 0.3
	control.gear = True
	control.lights = True
 if state == 'Runway' and testap.tLATLONG.dist_line() < 150:
	state = 'Glissada'
	testap.tLATLONG = end_r
	testap.tALTITUDE = 75
	testap.TrottlePid.setPoint(0.1)
	testap.maxTrottle = 0.1
	testap.minTrottle = 0.1
	control.brakes = True
 if state == 'Glissada' and surf_flight.surface_altitude < 5:
	testap.tALTITUDE = 50
	#print 'Kasanie', tLATLONG.dist_line() 
	testap.TrottlePid.setPoint(20)
	testap.maxTrottle = 0.5
	testap.minTrottle = 0.5
	control.set_action_group(6, True)
	control.brakes = True
 if state == 'Glissada' and surf_flight.horizontal_speed < 0.5:
	state = 'END'
	testap.tLATLONG = runwayWest
	testap.tALTITUDE = 50
	testap.TrottlePid.setPoint(0)
	testap.maxTrottle = 0.0
	testap.minTrottle = 0.0
	control.throttle = 0
	control.brakes = True	
 
 testap.dmet=vessel.met - testap.old_met
 testap.old_met=vessel.met
 print state, ";%.3f;%.1f;%.3f;%.3f;%.3f;%.3f;%.1f;%.3f;%.1f;%.3f;%.3f;" % (testap.TTrottle, surf_flight.horizontal_speed, testap.AtDeg, flight.pitch,testap.AtRoll, testap.tHeading, testap.tALTITUDE, testap.TVertSpeed, testap.tLATLONG.dist_line(), testap.tLATLONG.bearing_line(), testap.landingspeed())




#end
print 'Distance >> ', tLATLONG.dist_line(), ' [meters]'
print 'Initial bearing >> ', tLATLONG.bearing_line(), '[degrees]'
print 'Horizontal speed >> ', surf_flight.horizontal_speed, 'm/s'
print ""
control.sas = True

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



	
#=====================================================================================================================  
runwayWest    = coordinates(name='runwayWest',   lat=-0.04855056049336841, lng=-74.72449313835466000, alt=70.0)
runwayEast    = coordinates(name='runwayEast',   lat=-0.05022509861205912, lng=-74.48951284451766242, alt=70.0)
preRunwayEast = coordinates(name='preRunwayEast',lat=-0.06022509861205912, lng=-73.50451284451766242, alt=150.0)

recursive_dot = coordinates(name='recursive_dot', lat=-0.02022509861205912, lng=-71.18951284451766242, alt=1000.0)
two_dot =       coordinates(name='two_dot',        lat=0.35022509861205912, lng=-70.48951284451766242, alt=1000.0)
#======================================================================================================================

maxAtDeg = 7.0
minAtDeg = -7.0
minVERTICALSPEED = -10.0
maxVERTICALSPEED = 15.0
workVERTICALSPEED = 15
maxRoll = 20
maxDeg = 25
tALTITUDE = 1000.0
tsleep = 0.3
dVERTICALSPEED = 1.2
KVERTSPEED = 13
#==========================================================================================================================


ap.engage()

ap.target_pitch_and_heading(0.45, 90.40)
#control.speed_mode = surface
control.sas = False
#control.sas = True
control.rcs = False
control.gear = True
control.brakes = True
control.wheel_steering = 0

TrottleKp = 0.075
TrottleKi = 0.000001
TrottleKd = 0.150
TrottlePid=pid.PID(TrottleKp,TrottleKi,TrottleKd)

headingKp = 0.075
headingKi = 0.000001
headingKd 0.150
headingPid=pid.PID(headingKp,headingKi,headingKd, -7, 7)

if  runwayEast.dist_line() > runwayWest.dist_line():
  tLATLONG = runwayEast
  print "elevation to East direction runway"
  print 'Distance line >> ', tLATLONG.dist_line(), ' [meters]'
  print 'Distance >> ', tLATLONG.dist_line(), ' [meters]'
else:
  tLATLONG = runwayWest
  print "elevation to West direction runway"
  print 'Distance line >> ', tLATLONG.dist_line(), ' [meters]'
  print 'Distance >> ', tLATLONG.dist_line(), ' [meters]'
 

#surf_flight.speed, surf_flight.vertical_speed, surf_flight.horizontal_speed
print 'Razogrev'
control.throttle = 0
if vessel.available_thrust == 0.0 :
	control.activate_next_stage()
	time.sleep(0.2)
control.set_action_group(0, False)
control.set_action_group(9, True)
control.throttle = 1
while ((vessel.thrust) < (vessel.available_thrust * 0.7)) or surf_flight.speed < 1:
 time.sleep(0.5)

	
print 'Probeg'
control.brakes = False	
while surf_flight.speed < 50 or surf_flight.surface_altitude < 10:
	ap.target_pitch_and_heading(0.45, tLATLONG.bearing_line())
	vessel.auto_pilot.target_roll = 0
	time.sleep(0.1)


print 'Otrblv'
while surf_flight.surface_altitude < 15:
	ap.target_pitch_and_heading(4.0, tLATLONG.bearing_line())
	vessel.auto_pilot.target_roll = 0
	time.sleep(0.1)

tLATLONG = recursive_dot
state = 'Nabor Vblcotbl'
print 'Nabor Vblcotbl'
control.gear = False
dDist = tLATLONG.dist_line() /10
TrottlePid.setPoint(200)
maxTrottle = 0.9
minTrottle = 0.5
tALTITUDE = 1000
AtDeg = 10
old_met=0

print 'Distance line >> ', tLATLONG.dist_line(), ' [meters]'	
print 'Distance >> ', tLATLONG.dist_line(), ' [meters]'
print 'Initial bearing >> ', tLATLONG.bearing_line(), '[degrees]'
print ""
 
while state != 'END':

 if state == 'Nabor Vblcotbl':
	TVertSpeed = workVERTICALSPEED
 else:
	TVertSpeed=(tALTITUDE-flight.mean_altitude)/abs((tLATLONG.dist_line()-(tLATLONG.dist_line()*0.1))/surf_flight.horizontal_speed)
 if state == 'Nabor Vblcotbl':
	AtDeg = maxAtDeg
 else:
	AtDeg = AtDeg + (((TVertSpeed*dVERTICALSPEED) - surf_flight.vertical_speed)/KVERTSPEED) 
 if AtDeg > maxAtDeg:
	 AtDeg = maxAtDeg
 if AtDeg < minAtDeg:
	 AtDeg = minAtDeg

 t=tLATLONG.bearing_line()-flight.heading	 
 tHeading = flight.heading
 if t>360:
   t=t-360
 if t>180 or (t<0 and t>-180):
   AtRoll = max(0-maxRoll, abs(t))
   tHeading =  tHeading + max(0-maxDeg,0-abs(t))
 else:
   AtRoll = min(maxRoll,abs(t))
   tHeading = tHeading + min(maxDeg,abs(t))	 
 if surf_flight.surface_altitude <= 90:
	AtRoll = 0	



 TTrottle = TrottlePid.update(surf_flight.horizontal_speed,vessel.met)
 if TTrottle > maxTrottle:
	 TTrottle = maxTrottle
 if TTrottle < minTrottle:
	 TTrottle = minTrottle
  
 if (((state == 'flight to RunwayEast') or (state == 'Glissada') or (state == 'Kasanie')) and ((not control.get_action_group(9)) or control.get_action_group(0)) and (surf_flight.horizontal_speed<65)) :
	 	control.set_action_group(0, False)
		control.set_action_group(9, True)
	
 ap.target_pitch_and_heading(AtDeg, tHeading)
 vessel.auto_pilot.target_roll = AtRoll
 control.throttle = TTrottle
 time.sleep(tsleep)

 if state == 'Nabor Vblcotbl' and surf_flight.speed < 120:
	control.set_action_group(9, False)
	control.set_action_group(0, True)

 if state == 'Nabor Vblcotbl' and surf_flight.surface_altitude >= tALTITUDE:
	state = 'flight to Recursive dot'
	tALTITUDE = tLATLONG.alt
	TrottlePid.setPoint(220)
	maxTrottle = 0.9
	minTrottle = 0.3
	
 if state == 'flight to Recursive dot' and tLATLONG.dist_line() < 500:
	state = 'flight to preRunwayEast'
	tLATLONG = preRunwayEast
	tALTITUDE = preRunwayEast.alt
	TrottlePid.setPoint(150)
	maxTrottle = 0.9
	minTrottle = 0.3
		 
 if state == 'flight to Two dot' and tLATLONG.dist_line() < 500:
 	state = 'Revers to recursive_dot'
 	tLATLONG = recursive_dot
 	tALTITUDE = tLATLONG.alt
	
 if state == 'Revers to recursive_dot' and tLATLONG.dist_line() < 500:
	state = 'flight to preRunwayEast'
	tLATLONG = preRunwayEast
	tALTITUDE = preRunwayEast.alt
	TrottlePid.setPoint(150)
	maxTrottle = 0.9
	minTrottle = 0.3
	
 if state == 'flight to preRunwayEast' and tLATLONG.dist_line() < 1000:
	state = 'flight to RunwayEast'
	tLATLONG = runwayEast
	tALTITUDE = 75
	minAtDeg = -2
	TrottlePid.setPoint(65)
	maxTrottle = 0.7
	minTrottle = 0.1
	#control.throttle = 0.3
	control.gear = True
	
 if state == 'flight to RunwayEast' and tLATLONG.dist_line() < 150:
	state = 'Glissada'
	tLATLONG = runwayWest
	tALTITUDE = 71
	TrottlePid.setPoint(20)
	maxTrottle = 0.2
	minTrottle = 0.2
	control.brakes = True

	
 if state == 'Glissada' and surf_flight.surface_altitude < 3:
	tALTITUDE = 50
	print 'Kasanie', tLATLONG.dist_line() 
	TrottlePid.setPoint(20)
	maxTrottle = 0.2
	minTrottle = 0.1
	control.set_action_group(6, True)
	control.brakes = True
	
 if state == 'Glissada' and surf_flight.horizontal_speed < 0.5:
	state = 'END'
	tLATLONG = runwayWest
	tALTITUDE = 50
	TrottlePid.setPoint(0)
	maxTrottle = 0.0
	minTrottle = 0.0
	control.throttle = 0
	control.brakes = True	
 
 dmet=vessel.met - old_met
 old_met=vessel.met
 print state, " AtDeg: %.3f ; %.3f  tAlt: %.3f  tVertSp: %.3f dist_line: %.3f bearing_line: %.3f ; %.3f ; %.3f" % (AtDeg, flight.pitch, tALTITUDE, TVertSpeed, tLATLONG.dist_line(), tLATLONG.bearing_line(), tHeading, dmet)




#end
print 'Distance >> ', tLATLONG.dist_line(), ' [meters]'
print 'Initial bearing >> ', tLATLONG.bearing_line(), '[degrees]'
print 'Horizontal speed >> ', surf_flight.horizontal_speed, 'm/s'
print ""
control.sas = True

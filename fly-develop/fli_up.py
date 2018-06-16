import math
import krpc
import time

# Connect to the server with the default settings
# (IP address 127.0.0.1 and port 50000)
print 'Connecting to server...'
ksp = krpc.connect(name='Fly_UP')
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
ap.set_pid_parameters(75,50,25)
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
  #runway_beg  -- координаты края впп на которую производится посадка
  #runway_stop -- координаты дальнего края впп в направлении которого идет пробежка после касания
  #dist        -- дистанция выноса точки глиссады
  dist_t = dist/(math.sqrt(((runway_beg.lat - runway_stop.lat)**2)+((runway_beg.lng - runway_stop.lng)**2))*10471.97333333)
  glis_dot = coordinates(name='glis_point', lat=(runway_beg.lat+dist_t*(runway_beg.lat-runway_stop.lat)), lng=(runway_beg.lng+dist_t*(runway_beg.lng-runway_stop.lng)), alt=(dist*0.1)+70.0)
  return glis_dot

  
runwayWest    = coordinates(name='runwayWest',   lat=-0.04855056049336841, lng=-74.72449313835466000, alt=70.0)
runwayEast    = coordinates(name='runwayEast',   lat=-0.05022509861205912, lng=-74.48951284451766242, alt=70.0)
preRunwayEast = coordinates(name='preRunwayEast',lat=-0.05022509861205912, lng=-73.40451284451766242, alt=500.0)

recursive_dot = coordinates(name='recursive_dot', lat=-0.000, lng=-72.48951284451766242, alt=1000.0)
two_dot =       coordinates(name='two_dot',        lat=0.000, lng=-70.48951284451766242, alt=1000.0)


#-------------PID settings---------------
delta_met=0.0000000000000000000000001
#PID
#Tangage
VaP = 0.07
VaI = 0.01    #izmenyaem tolko delitel
VaD = 0.025
VaInt=0
VaOldErr=0
VaLastInt = VaInt

#Trottle
TrP = 0.05
TrI = 0.01    #izmenyaem tolko delitel
TrD = 0.005
TrInt=0
TrOldErr=0
TrLastInt = TrInt
#-----------------------------------------

maxAtDeg = 12.0
minAtDeg = -12.0
minVERTICALSPEED = -35.0
maxVERTICALSPEED = 35.0
workVERTICALSPEED = 30
tALTITUDE = 1000.0
dVERTICALSPEED = 1.2
KVERTSPEED = 10
AtDegDebug = 0

maxRoll = 30

maxTrottle = 1.0
minTrottle = 0.3
minHorSpeed = 100.0
maxHorSpeed = 200.0
workHorSpeed = 200.0

DegStr = 25

StartTrustK = 0.7
StartDeg = 0.45

DegOtr = 10
SpeedOtr = 80
AltOtr = 15

DegNabora = 12
SpeedNabora = 30
AltNabora = 1000

ap.engage()
ap.target_pitch_and_heading(0.45, 90.40)
control.sas = False
control.rcs = False
control.brakes = True
control.wheel_steering = 0

#Select direction
if  runwayEast.dist_line() > runwayWest.dist_line():
  tLATLONG = runwayEast
  print "elevation to East direction runway"
  
else:
  tLATLONG = runwayWest
  print "elevation to West direction runway"
print 'Distance >> ', tLATLONG.dist_line(), ' [meters]' 
#------------------

print 'Razogrev'
control.throttle = 0
if vessel.available_thrust == 0.0 :
	control.activate_next_stage()
	print 'Start Engines'
	time.sleep(0.2)
control.throttle = 1
while (vessel.thrust) < (vessel.available_thrust * StartTrustK):
 time.sleep(0.5)

	
print 'Probeg'
control.brakes = False	
while surf_flight.speed < SpeedOtr:
	ap.target_pitch_and_heading(StartDeg, tLATLONG.bearing_line())
	vessel.auto_pilot.target_roll = 0



print 'Otrblv'
while surf_flight.surface_altitude < AltOtr:
	ap.target_pitch_and_heading(DegOtr, tLATLONG.bearing_line())
	vessel.auto_pilot.target_roll = 0


tLATLONG = recursive_dot
state = 'Nabor Vblcotbl'
print 'Nabor Vblcotbl'
control.gear = False
dDist = tLATLONG.dist_line() /10
maxAtDeg = DegNabora
minAtDeg = DegNabora
minVERTICALSPEED = SpeedNabora
maxVERTICALSPEED = SpeedNabora
tALTITUDE = AltNabora
AtDeg = DegNabora
oldAtDeg = AtDeg

TTrottle = 1.0

print 'Distance line >> ', tLATLONG.dist_line(), ' [meters]'	
print 'Distance >> ', tLATLONG.dist_line(), ' [meters]'
print 'Initial bearing >> ', tLATLONG.bearing_line(), '[degrees]'
print ""

delta_met=0.0000000000000000000000001
All_clock=time.time()
All_met=vessel.met
 
while state != 'END':
 this_clock=time.time()
 this_met=vessel.met
 
 
 if state == 'Nabor Vblcotbl' and surf_flight.surface_altitude >= tALTITUDE:
	state = 'Recursive dot'
	maxAtDeg = 12.0
	minAtDeg = -12.0
	minVERTICALSPEED = -35.0
	maxVERTICALSPEED = 35.0
	tALTITUDE = 1200
	control.throttle = 1.0
	#TTrottle = 1.0
	VaInt = 0
	VaLastInt = VaInt
	
 if state == 'Recursive dot' and tLATLONG.dist_line() < 500:
	state = 'preRunwayEast'
	tLATLONG = preRunwayEast
	tALTITUDE = preRunwayEast.alt
	VaInt = 0
	VaLastInt = VaInt
		 
 #if state == 'Two dot' and tLATLONG.dist_line() < 500:
 	#state = 'Revers to recursive_dot'
 	#tLATLONG = recursive_dot
 	#tALTITUDE = tLATLONG.alt
 	#VaInt = 0
 	#VaLastInt = VaInt
	
 if state == 'preRunwayEast' and tLATLONG.dist_line() < 700:
	state = 'RunwayEast'
	print 'gluk'
	tLATLONG = runwayEast
	tALTITUDE = 75
	minAtDeg = -2
	#TTrottle = 0.7
	control.throttle = 0.7
	workHorSpeed = 100.0
	control.gear = True
	
 if state == 'RunwayEast' and tLATLONG.dist_line() < 300:
	state = 'runwayWest'
	minVERTICALSPEED = -3.0
	maxVERTICALSPEED = -0.80
	tLATLONG = runwayWest
	tALTITUDE = 70
	control.throttle = 0
	TTrottle = 0.0
	workHorSpeed = 0.0
	VaInt = 0

	
 if state == 'runwayWest' and surf_flight.surface_altitude < 5:
	state = 'Kasanie'
	tLATLONG = runwayWest
	tALTITUDE = 50
	TTrottle = 0.0
	workHorSpeed = 0.0
	control.brakes = False
	VaInt = 0
	VaLastInt = VaInt
	
 if state == 'runwayWest' and tLATLONG.dist_line() < 2400:
	tALTITUDE = 50
	workHorSpeed = 0.0
	VaInt = 0
	VaLastInt = VaInt
	
 if state == 'runwayWest' and surf_flight.surface_altitude < 4:
	state = 'Kasanie'
	tLATLONG = runwayWest
	tALTITUDE = 50
	workHorSpeed = 0.0
	control.brakes = False
	control.throttle = 0
	VaInt = 0
	VaLastInt = VaInt
	
 if state == 'Kasanie' and ((tLATLONG.dist_line() < 1200) or (surf_flight.horizontal_speed < 80.0)):
	tALTITUDE = 50
	control.brakes = True
	control.throttle = 0
	
	
 if state == 'Kasanie' and surf_flight.horizontal_speed < 0.5:
	state = 'END'
	tLATLONG = runwayWest
	tALTITUDE = 50
	workHorSpeed = 0.0
	control.brakes = True
	VaInt = 0
	VaLastInt = VaInt	
 
 if delta_met<0.000000000000000000001:
	 delta_met=0.0000000000000000000000001
 
 
 #=========== Vertical Speed 
 TVertSpeed=(tALTITUDE-flight.mean_altitude)/abs((tLATLONG.dist_line()-(tLATLONG.dist_line()*0.1))/surf_flight.horizontal_speed)
 if TVertSpeed > maxVERTICALSPEED:
	 TVertSpeed = maxVERTICALSPEED
 if TVertSpeed < minVERTICALSPEED:
	 TVertSpeed = minVERTICALSPEED
 
 #=========== PID Tangage
 
 if delta_met<0.000000000000000000001:
	 delta_met=0.0000000000000000000000001

 oldAtDeg = AtDeg
 VaErr = TVertSpeed - surf_flight.vertical_speed
 VaInt = VaLastInt + VaI * delta_met * VaErr
 VaPID = (VaP * VaErr) + VaInt + (VaD/delta_met * (VaErr-VaOldErr))
 VaLastInt = VaInt
 VaOldErr = VaErr
 AtDeg = AtDeg+VaPID
 if (AtDeg > 1800) or (AtDeg < -1800):
   AtDeg = oldAtDeg
 
 AtDegDebug = AtDeg

	 
 if AtDeg > maxAtDeg:
	 AtDeg = maxAtDeg
 if AtDeg < minAtDeg:
	 AtDeg = minAtDeg
	 
 #=========== PID Trottle
 #TrErr = (workHorSpeed) - (surf_flight.horizontal_speed)	
 #TrInt = TrLastInt + TrI * delta_met * TrErr
 #TTrottle = (TrP * TrErr) + (TrI)*TrInt+TrD*(TrErr-TrOldErr)
 #TrLastInt = TrInt
 #TrOldErr = TrErr
	 
 #if TTrottle > maxTrottle:
	 #TTrottle = maxTrottle
 #if TTrottle < minTrottle:
	 #TTrottle = minTrottle


 t=tLATLONG.bearing_line()-flight.heading	 
 tHeading = flight.heading
 if t>360:
   t=t-360
 if t>180 or (t<0 and t>-180):
   AtRoll = max(0-maxRoll,0-abs(t*1.5))
   tHeading =  tHeading + max(0-DegStr,0-abs(t))
 else:
   AtRoll = min(maxRoll,abs(t*1.5))
   tHeading = tHeading + min(DegStr,abs(t))	 
 if surf_flight.surface_altitude <= 90:
	AtRoll = 0	
 
 if (AtRoll > 10) or (AtDeg < -10):
	 VaInt = 0
	 VaLastInt = VaInt
	 
 this_clock=time.time()
 this_met=vessel.met
 
 	
 ap.target_pitch_and_heading(AtDeg, tHeading)
 vessel.auto_pilot.target_roll = AtRoll
 #control.throttle = TTrottle 



 
 delta_clock=time.time()-this_clock
 #if delta_clock< 0.1:
	 #time.sleep(0.1-delta_clock)
 delta_met=vessel.met-this_met
 print state, 'Time: {:>6}, AtDeg: {:>7}; {:>10}; {:>7} tVertSp: {:>6}; {:>6} dist_line: {:>5} dTime : {:>5}; {:>5} VaInt: {:>5}; {:>7} VaP: {:>8};'.format('{: .2f}'.format(time.time()-All_clock), '{: .3f}'.format(AtDeg), '{: .3f}'.format(AtDegDebug), '{: .3f}'.format(flight.pitch), '{: .2f}'.format(TVertSpeed), '{: .2f}'.format(surf_flight.vertical_speed), '{: .1f}'.format(tLATLONG.dist_line()), '{: .3f}'.format(time.time()-this_clock), '{: .3f}'.format(delta_met), '{: .3f}'.format(VaInt), '{: .3f}'.format((VaI)*VaInt), '{: .3f}'.format(VaP * VaErr))





#end
print 'Distance >> ', tLATLONG.dist_line(), ' [meters]'
print 'Initial bearing >> ', tLATLONG.bearing_line(), '[degrees]'
print 'Horizontal speed >> ', surf_flight.horizontal_speed, 'm/s'
print 'Pogreshnost` vremeny >> ',(time.time()-All_clock)/(vessel.met-All_met)
print 'Vremya KSP >> ',(vessel.met-All_met)
print 'Real vremya >> ',(time.time()-All_clock)
print ""
control.sas = True

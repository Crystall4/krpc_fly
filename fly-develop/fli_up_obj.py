import math
import krpc
import time
import pid

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
 def set(self, lat=self.lat, lng=self.lng, alt=self.alt, name=self.name):
	self.lat=lat
	self.lng=lng
	self.name=name
	self.alt=alt
 def set_current(self, name='Current Position'):
	self.lat=flight.latitude
	self.lng=flight.longitude
	self.name=name
	self.alt=flight.mean_altitude
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
  return self.dist_deg()*10471.97333333
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

runwayWest    = coordinates(name='runwayWest',   lat=-0.04855056049336841, lng=-74.72449313835466000, alt=70.0)
runwayEast    = coordinates(name='runwayEast',   lat=-0.05022509861205912, lng=-74.48951284451766242, alt=70.0)
preRunwayWest = coordinates(name='preRunwayEast',lat=-0.04855056049336841, lng=-75.40451284451766242, alt=500.0)
preRunwayEast = coordinates(name='preRunwayEast',lat=-0.05022509861205912, lng=-73.40451284451766242, alt=500.0)

Ttask={0:'None', 1:'from_alt', 2:'from_coord', 3:'from_coord_and_alt', 4:'from_hor_speed', 5:'from_vert_speed'}
Ttolerance{0:'None',1:"PSpeed",2:'ASpeed',3:'Altitude',4:'Horizontal',5:'Tunnel',6:'Alt_Hor'}
Terror={0:'None', 1:'Diagnostic fault'}

class Fly_error:
	number = 0
	message = ''
	def __init__(self, number=0, message='undef'):
		self.number = number
		self.string = Terror.get(number)
		self.message = message

class tolerance:
	type_tolerance = 0
	speed_ptolerance = 0.0
	speed_atolerance = 0.0
	coord_tolerance  = {vertical:0.0, horizontal:0.0}

class mode:
	name = "None"
	maxAtDeg = 7.0 										# максимальный-минимальный расчетный угол тангажа
	minAtDeg = -7.0
	maxDeg = 25											# максимальное отклонение по тангажу в режиме аэро полета
	maxVERTICALSPEED = 15.0								# максимальная-минимальная расчетная вертикальная скорость
	minVERTICALSPEED = -10.0
	workVERTICALSPEED = 15								# рабочая вертикальная скорость
	maxRoll = 20										# максимальный угол крена
	maxTrottle = 1.0									# максимальная-минимальная установка РУД
	minTrottle = 0.3
	minHorSpeed = 100.0									# максимальная-минимальная горизонтальная скорость
	maxHorSpeed = 200.0
	workTrottle = 0.8
	sas			= True
	rcs			= False
	brakes		= False
	gear		= False

class target:
	type_task = 0
	name   = 'Default'
	coord  = coordinates(name='default', lat=0.000, lng=-70.48951284451766242, alt=1150.0)
	vspeed = 0.0
	hspeed = 150.0
	speed_tolerance  = tolerance(1, 10)
	coord_tolerance  = tolerance(6,150,1500)
	__init__(self, name,)

class task:
	name = "Default"
	sub_tasks_list=[]
	target=target()
	pre_run()
	run()
	error()
	post_run()
	
	__init__(self, name="Default", sub_tasks_list=[], target=''):
		self.name=name
		self.sub_tasks_list=sub_tasks_list
		if len(self.sub_tasks_list)>0:
			self.current_sub_task = self.sub_tasks_list.pop([i])
			self.target = self.current_sub_task.target
		else
			self.target = target

class vpp:
	k1 = coordinates(name='runwayWest',   lat=-0.04855056049336841, lng=-74.72449313835466000, alt=70.0)
	k2 = coordinates(name='runwayEast',   lat=-0.05022509861205912, lng=-74.48951284451766242, alt=70.0)	
	
class fly_vessel:
	
	basic_tasks = {takeoff:task(name="Takeoff",[0:target(),]), landing }
	basic_modes = {takeoff_pre:mode("takeoff", trottle=0.30, brakes=True, gear=True)}
	mode = mode()
	maxAtDeg = 7.0 										# максимальный-минимальный расчетный угол тангажа
	minAtDeg = -7.0
	maxDeg = 25											# максимальное отклонение по тангажу в режиме аэро полета
	maxVERTICALSPEED = 15.0								# максимальная-минимальная расчетная вертикальная скорость
	minVERTICALSPEED = -10.0
	workVERTICALSPEED = 15								# рабочая вертикальная скорость
	maxRoll = 20										# максимальный угол крена
	maxTrottle = 1.0									# максимальная-минимальная установка РУД
	minTrottle = 0.3
	marchTrottle = 0.8
	minHorSpeed = 100.0									# максимальная-минимальная горизонтальная скорость
	maxHorSpeed = 200.0
	SeparationSpeed = 100 								# горизонтальная скорость начала отрыва
	SeparationAngle = 3									# угол тангажа при отрыве
	SeparationAltitude = 15								# высота на которой отрыв считается состоявшимся
	max_flight_altitude = 12000							# максимальная полетная высота
	service_ceiling	= 10000								# практический потолок
	mass0=48600											# масса без груза
	landingspeed0 = 80									# мин. скорость захода на посадку при mass0
	Klandingspeed = 2									# коэффициент расчета посадочной скорости при массе отличающейся от mass0

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
	dVERTICALSPEED = 1.2
	KVERTSPEED = 10
	AtDegDebug = 0
	
	maxRoll = 30
	workHorSpeed = 200.0
	StartTrustK = 0.7
	StartDeg = 0.45

	DegNabora = 12
	SpeedNabora = 30
	AltNabora = 1000
	
	def __init__(self, name):
		
	
	def position(self):
		CP = coordinates(name='currentPosition',   lat=flight.latitude, lng=-74.72449313835466000, alt=70.0)
		CP.set_current()
		return CP
	
	def loop(self):
		control.throttle = self.calc_trottle()
		ap.target_pitch_and_heading(self.calc_pitch(), self.calc_yaw())
		vessel.auto_pilot.target_roll = self.calc_roll()
		self.mode.update()

	def diagnostic(self):
		return True

	def landingspeed(self):
		return self.landingspeed0+(self.landingspeed0*(((vessel.mass-self.mass0)/self.mass0)/2))

	def takeoff():
		if (not diagnostic()):
			err = Fly_error(number=1) 
			return err
			break

class mission:
	vessel=fly_vessel()
	tasks_queue = {}
	task = task()
	def task_add(task):
		return False

def glis_point(runway_beg, runway_stop, dist):
  #runway_beg  -- координаты края впп на которую производится посадка
  #runway_stop -- координаты дальнего края впп в направлении которого идет пробежка после касания
  #dist        -- дистанция выноса точки глиссады
  dist_t = dist/(math.sqrt(((runway_beg.lat - runway_stop.lat)**2)+((runway_beg.lng - runway_stop.lng)**2))*10471.97333333)
  glis_dot = coordinates(name='glis_point', lat=(runway_beg.lat+dist_t*(runway_beg.lat-runway_stop.lat)), lng=(runway_beg.lng+dist_t*(runway_beg.lng-runway_stop.lng)), alt=(dist*0.1)+70.0)
  return glis_dot


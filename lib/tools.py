# -*- coding: utf-8 -*-

import math
import time
import json


prch = [2,3,5,7,11,13,17,19,23,29,31,37,41]



#тип сообщения, определяется по коду в m_type 
type_message={
0:{'name':'Ping','isLogging':False,'log_mess':'', 'isParammetric':False} #просто пинг для проверки
1:{'name':'Hello','log_mess':'', 'isParammetric':False} #начало общения просто для проверки что получатель отвечает хоть как то)))
}
name_message={
'Ping' :0
'Hello':1
'OK'   :2
'Bad'  :3
}

#формат сырого сообщения pl-A4Aatm_142313:
#dict(
	#sender, код отправителя, состоит из:
		#1: 2х символов типа [
			#bs - база(статический или малоподвижный поверхностный объект, малоподвижный или неподвижный водный объект осуществляющй информирование и диспетчеризацию в некотором пространстве),
				#имя базы, допустимо указывать имя обьекта где размещена с указанием имени проекта базы или имя проекта + координаты и высота в формате 2-х или 3-х цифровых индексов округленные, координаты: до единиц или десятков; высота сотен метров или км над уровнем моря или задается вручную
			#ld - посадочный модуль(подвижный объект неспособный к активному, длительному маневрированию выполняющий спуск на реактивных двигателях или парашютах),
				#берётся из имени проекта + номер формируемый при инициализации скрипта управления или задается вручную
			#pl - планер(самолет, ссто и спускаемый аппарат самолетного типа),
				#берётся из префикса проекта + префикс из типа и названия флайтплана(может быть пустым) + знак подчеркивания + номер формируемый при активации скрипта миссии или указываемый вручную в том же файле 
			#pr - космический беспилотный объект, не предназначенный для посадки, не ведущий ретрансляцию данных,
				#берётся из имени проекта + номер формируемый при инициализации скрипта управления или задается вручную
			#rl - космический(не предназначенный для посадки) или поверхностный неманевренный беспилотный объект, ведущий ретрансляцию данных от других источников,
				#берётся из имени проекта + номер формируемый при инициализации скрипта управления, имя проекта + имя центрального тела + если орбита стационарна то координаты и высота в формате 2-х или 3-х цифровых индексов округленные, координаты: до единиц или десятков; высота сотен метров или км над уровнем моря или задается вручную
			#ro - поверхностный способный к движению и маневрированию объект, кроме самоходных баз,
			#sh - космический или водный подвижный способный к маневрированию объект способный иметь экипаж,
			#st - космическая база :-)]
			#после котрых идет знак минус
		#2: имя или бортовой номер составляемые для разных типов по собственным правилам(описаны в предыдущем пункте) и указымаемый при создании файла полета или берущиеся из ангара или задается вручную
	#receiver, код получателя (продумать роутинг для релаев)
	#m_type, код типа сообщения 
	#param, параметры сообщения, не обязательно, наличие зависит от типа
	#control контрольная сумма
	
class message:
	sender   = None 
	receiver = None
	m_type   = None #type_message
	m_name   = None #Имя сообщения при получении берется из type_message.name при создании из параметров self.create_message()
	param    = None #не обязательны, зависит от типа сообщения
	control  = None #статус проверки по контрольной сумме, расчитывается при создании сообщения по json строке сырого сообщения без контрольной суммы при парсинге по ней проверяется корректность получения сообщения
	def create_message(self,sender,receiver,m_name,param=None):
		if sender and receiver and m_name:
			if param != None:
				result = json.dumps(dict{'sender'=sender,'receiver'=receiver,'m_name'=m_name,'param'=param})
			else:
				result = json.dumps(dict{'sender'=sender,'receiver'=receiver,'m_name'=m_name})
		else:
			result = "Error"
		return result
	def parse_message(self,mess):
		messp=json.loads(data)
		self.sender   = None 
		self.receiver = None
		self.m_type   = None #type_message
		self.m_name   = None #Имя сообщения при получении берется из type_message.name при создании из параметров self.create_message()
		self.param    = None #не обязательны, зависит от типа сообщения
		
		
		

def sec_to_time(sec):
	if sec>86400: print time.strftime('%d дней %H:%M:%S',time.gmtime(sec))
	else: print time.strftime('%H:%M:%S',time.gmtime(sec))

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
 def dist_deg(self, CP):
  return math.sqrt(((self.lat - CP.lat)**2)+((self.lng - CP.lng)**2))
 def dist_line(self,CP):
  return math.sqrt(((self.lat - CP.lat)**2)+((self.lng - CP.lng)**2))*10471.97333333
 def dist_line_from(self,from_dot):
	 return math.sqrt(((self.lat - from_dot.lat)**2)+((self.lng - from_dot.lng)**2))*10471.97333333
 def dist_gc(self,CP):
  rad = 600000
  lat1 = CP.lat*math.pi/180.
  lat2 = self.lat*math.pi/180.
  long1 = CP.lng*math.pi/180.
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
 def bearing_gc(self,CP):
  rad = 600000
  lat1 = CP.lat*math.pi/180.
  lat2 = self.lat*math.pi/180.
  long1 = CP.lng*math.pi/180.
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
 def bearing_line(self,CP):
	dX = (CP.lng) - (self.lng) 
	dY = (CP.lat)  - (self.lat)
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
 def bearing_line_from(self,from_dot):
	dX = (from_dot.lng) - (self.lng) 
	dY = (from_dot.lat)  - (self.lat)
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
 def target_dot_from_dist_and_bear(self,bearing,dist):
	dX=math.cos(math.radians(bearing))*dist
	dY=math.sin(math.radians(bearing))*dist
	return coordinates(name='Raschet', lat=(self.lat+(dX/10471.97333333)), lng=(self.lng+(dY/10471.97333333)))

def glis_point(runway_beg, runway_stop, dist):
  dist_t = dist/(math.sqrt(((runway_beg.lat - runway_stop.lat)**2)+((runway_beg.lng - runway_stop.lng)**2))*10471.97333333)
  glis_dot = coordinates(name='glis point from '+runway_beg.name, lat=(runway_beg.lat+dist_t*(runway_beg.lat-runway_stop.lat)), lng=(runway_beg.lng+dist_t*(runway_beg.lng-runway_stop.lng)), alt=(dist*0.1)+70.0)
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

log_level= 5
log_file = 'log/debug'
lf       = None

def log(string_logging,level=5):
	if log_level >= level:
		print string_logging
	if lf != None:
		lf.write(string_logging.encode("utf-8")+'\n')

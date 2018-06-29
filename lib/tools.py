# -*- coding: utf-8 -*-

import math
import time

prch = [2,3,5,7,11,13,17,19,23,29,31,37,41]

chisl={
1 :{'int' :1,'str':'First',  'ru_str_f':'Первая'    ,'ru_str_m':'Первый'   ,'Rome':'I'   },
2 :{'int' :2,'str':'Second', 'ru_str_f':'Вторая'    ,'ru_str_m':'Второй'   ,'Rome':'II'  },
3 :{'int' :3,'str':'Third',  'ru_str_f':'Третья'    ,'ru_str_m':'Третий'   ,'Rome':'III' },
4 :{'int' :4,'str':'Fourth', 'ru_str_f':'Четвертая' ,'ru_str_m':'Четвертый','Rome':'IV'  },
5 :{'int' :5,'str':'Fifth',  'ru_str_f':'Пятая'     ,'ru_str_m':'Пятый'    ,'Rome':'V'   },    
6 :{'int' :6,'str':'Sixth',  'ru_str_f':'Шестая'    ,'ru_str_m':'Шестой'   ,'Rome':'VI'  },
7 :{'int' :7,'str':'Seventh','ru_str_f':'Седьмая'   ,'ru_str_m':'Седьмой'  ,'Rome':'VII' },
8 :{'int' :8,'str':'Eighth', 'ru_str_f':'Восьмая'   ,'ru_str_m':'Восьмой'  ,'Rome':'VIII'},
9 :{'int' :9,'str':'Ninth',  'ru_str_f':'Девятая'   ,'ru_str_m':'Девятый'  ,'Rome':'IX'  },
10:{'int':10,'str':'Tenth',  'ru_str_f':'Десятая'   ,'ru_str_m':'Десятый'  ,'Rome':'X'   }
}



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

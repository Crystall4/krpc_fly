import math
import krpc
import time

lng_step = 10506.0378591835
lat_step = 10485.2470800102
geofile=open("/home/sysadmin/1/KSP_linux/Ships/Script/geolog.ks",'r')

def takeActiveCoord():
 geofile.seek(-120,2)
 raw_data = geofile.read()
 geoline = raw_data.split('\n')[-1]
 print geoline
 geolist = geoline.split(';')
 print geolist
 return dict(name=geolist[0], lat=geolist[1], lng=geolist[2], alt=geolist[3])
 
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
 def distance(self, ac=takeActiveCoord()):
  if not ac:
    ac=takeActiveCoord()
  return math.sqrt((((self.lat - float(ac['lat']))*lat_step)**2)+(((self.lng - float(ac['lng']))*lng_step)**2))
  

runwayWest = coordinates(name='runwayWest',lat=-0.0486042921872496, lng=-74.7243248897512, alt=71.2204968751175)
runwayEast = coordinates(name='runwayEast',lat=-0.0502510692383407, lng=-74.493032574141, alt=71.2204968751175)
mypos      = takeActiveCoord()
mytest     = coordinates(name=mypos['name'], lat=float(mypos['lat'])+1, lng=float(mypos['lng'])+1, alt=float(mypos['alt'])+1)

print mytest.distance()
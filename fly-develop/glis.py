import match
import krpc
import time

lng_step = 10506.0378591835
lat_step = 10485.2470800102
geofile=open("geolog",r)

def takeActiveCoord();
 geofile.seek(0,2)
 geoline = geofile.readline()
 geolist = geoline.split(';')
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
  #return "name=self.name, lat=self.lat, lng=self.lng, alt=self.alt"
  return "%.3f" % (self.lat)
  
 def __str__(self):
  return 'Coordinates {}: {}, {}, {}'.format(self.name, self.lat, self.lng, self.alt)
 def __init__(self, lat=0.0, lng=0.0, alt=0, name=''):
  self.lat=lat
  self.lng=lng
  self.name=name
  self.alt=alt
 def distance(self, ac=takeActiveCoord())
  return math.sqrt(((self.lat - ac['lat'])**2)+((self.lng - ac['lng'])**2))
  

runwayWest = coordinates(name='runwayWest',lat=-0.0486042921872496, lng=-74.7243248897512, alt=71.2204968751175)
runwayEast = coordinates(name='runwayEast',lat=-0.0502510692383407, lng=-74.493032574141, alt=71.2204968751175)
tLATLONG = runwayWest.

if  runwayEast.distance < runwayWest.distance
  set tLATLONG to runwayEast.
  set distswitch to -74.45.
  print "landing to East direction runway" at (0,1).
else {
  set tLATLONG to runwayWest.
  set distswitch to -74.75.
  print "landing to West direction runway" at (0,1).
  }

set dotone to latlng(-0.05737096445295922, -73.493032574141).
set targLL to dotone.
set tHeading to ship:heading + (targLL:bearing/10).

set tRadarAlt to 2.05547523.
set tALTITUDE to 500.
set cAlt to 0.
set maxAtDeg  to 25.
set minAtDeg  to -5.
set minVERTICALSPEED to -50.
set maxVERTICALSPEED to 50.
set AtDeg to 8.
set dTIME to 0.
set dDIST to targLL:DISTANCE/10.
set dVERTICALSPEED to 1.2.
set KVERTSPEED to 75.
set Bwaypoint to true.
set Bprobeg to true.
set Bkasanie to true.
set Bstop to true.

lock DtrimHead to 1*(targLL:DISTANCE/10000).
lock STEERING TO HEADING(tHeading,AtDeg).
lock cAlt to ALTITUDE.
lock fHeading to (SHIP:FACING * R(0,90,0)):pitch + (targLL:bearing-(targLL:bearing/5)).

until 0{

if targLL:bearing > 0.2 {set tHeading to (fHeading + DtrimHead) .}
if targLL:bearing < -0.2 {set tHeading to (fHeading - DtrimHead) .}
if (tALTITUDE - ALTITUDE) /abs((targLL:DISTANCE-dDIST) /SHIP:SURFACESPEED) > maxVERTICALSPEED {set tVERTICALSPEED to maxVERTICALSPEED.}
else {
  if (tALTITUDE - ALTITUDE) /abs((targLL:DISTANCE-dDIST) /SHIP:SURFACESPEED) < minVERTICALSPEED {set tVERTICALSPEED to minVERTICALSPEED.} 
  else {set tVERTICALSPEED to   (tALTITUDE - ALTITUDE) /abs((targLL:DISTANCE-dDIST) /SHIP:SURFACESPEED).}
  }
set AtDeg to AtDeg + (((tVERTICALSPEED*dVERTICALSPEED) - VERTICALSPEED)/KVERTSPEED).
if AtDeg > maxAtDeg{set AtDeg to maxAtDeg.}
if AtDeg < minAtDeg{set AtDeg to minAtDeg.} 


print "##### Buran Auto-Landing System ##### " at (5,0).
print "Target Distance  : " + round(targLL:DISTANCE,1) + "        " at (0,3).
print "Radar  Altitude  : " + round(ALT:RADAR,1)       + "        " at (0,8).
print "Altitude         : " + round(ALTITUDE,1)        + "        " at (0,9).
print "Vertical Speed   : " + round(VERTICALSPEED,1)   + "        " at (0,11).
print "T Vertical Speed : " + round(tVERTICALSPEED,1)  + "        " at (0,12).

print "AtDeg            : " + round(AtDeg,2)   + "        " at (0,14).
print "tALT             : " +  tALTITUDE + "                          " at (0,15).
print "tHeading         : " + round(tHeading,2)  + "        " at (0,16). 
print "Bearing          : " + round(targLL:bearing,3)  + "        " at (0,17).
log TIME:SECONDS + ";" + tLATLONG:DISTANCE + ";" + ALT:RADAR + ";" + ALTITUDE + ";" + VERTICALSPEED + ";" + tVERTICALSPEED + ";" + AtDeg + ";" + tHeading + ";" + targLL:bearing + ";" + DtrimHead + SHIP:GEOPOSITION + ";" + targLL  to glislog.
print "Program Looptime : " + ROUND(TIME:SECONDS -dTIME, 4) + "                    " at (0,19).

if  round(SHIP:GEOPOSITION:LNG,2) < -73.40 and Bwaypoint {
  set Bwaypoint to false.
  print  round(TIME:SECONDS,1) + " WP: " + round(targLL:DISTANCE,3) + "m. Gear, Lights ON."  at (0,21).
  log TIME:SECONDS + " wp: " + SHIP:GEOPOSITION + targLL:DISTANCE + "m. Target Runway. Gear ON. Lights ON."  to glislog.
  set targLL to tLATLONG.
  set tALTITUDE to runwayalt.
  set dDIST to -50.
  set dVERTICALSPEED to 1.
  gear on.
  lights on.
  }
  
if round(SHIP:GEOPOSITION:LNG,2) = distswitch and Bprobeg { 
  if  runwayEast:DISTANCE > runwayWest:DISTANCE {
  set targLL to runwayEast.
  lock fHeading to (SHIP:FACING * R(0,90,0)):pitch + (targLL:bearing).
  print "probeg to East direction runway         " at (0,1).
  log TIME:SECONDS + " probeg to East direction runway. Trottle 0. " to glislog.
  print round(TIME:SECONDS,1) + "probeg to East direction runway. Trottle 0. " at (0,22).
  }
else {
  set targLL to runwayWest.
  print "probeg to West direction runway         " at (0,1).
  log  TIME:SECONDS + " probeg to West direction runway. Trottle 0." to glislog.
  print  round(TIME:SECONDS,1) + " probeg to West direction runway. Trottle 0." at (0,22).
  }
  set Bprobeg to false.
  set dVERTICALSPEED to 1.
  set tALTITUDE to 60.
  set KVERTSPEED to 50.
  set maxVERTICALSPEED to -1.
  set minVERTICALSPEED to -5.
  lock throttle to 0.
  }
if ALT:RADAR < 3.9 and Bkasanie {
  set Bkasanie to false.
  brakes on.
  lock throttle to 0.
  set maxVERTICALSPEED to 0.
  set minVERTICALSPEED to 0.
  set maxAtDeg  to 0.
  set minAtDeg  to -1.
  set tALTITUDE to 40.
  log TIME:SECONDS + " Kasanie :" + SHIP:GEOPOSITION + ".  " + targLL:DISTANCE + " do konca polosy. Brakes ON."  to glislog.
  print round(TIME:SECONDS,1) + " Kasanie : " + round(targLL:DISTANCE,3) + " do konca polosy. Brakes ON.                 "  at (0,23).
  }
if SHIP:SURFACESPEED < 0.01 and Bstop {
  set Bstop to false.
  log TIME:SECONDS + " STOP : " + SHIP:GEOPOSITION + "  " + targLL:DISTANCE + " do konca polosy."  to glislog.
  print round(TIME:SECONDS,1) + " Stop :" + SHIP:GEOPOSITION + round(targLL:DISTANCE,3) + " do konca polosy. Brakes ON.                 "  at (0,24).
  BREAK.
  }
set dTIME to TIME:SECONDS.
wait 0.05.
}

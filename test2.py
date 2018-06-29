import sys
sys.path.append("./lib")
sys.path.append("./runways")
sys.path.append("./aircrafts")
sys.path.append("./runways")

from tools import *
import KSC
import iceland

log_level=1

#for i in KSC.KSC_VPP.zones:
	#print i.name+"  "+i.message
#print '=============================================='
#for i in iceland.iceland_VPP.zones:
	#print i.name+"  "+i.message



#from test2 import *
KSC_BP   = coordinates(name= 'Begin Position', lat= -0.0485935550516, lng= -74.72465205780000000, alt=   70.3741567462)
tp       = coordinates(name= 'recursive_dot',  lat= -0.0000000000000, lng=  12.48951284451766242, alt= 1500.0000000000)

vp=KSC.KSC_VPP.get_SID(tp,KSC_BP)

print KSC_BP.dist_line(KSC.KSC_East)
print "taget distance: "+str(KSC_BP.dist_line(tp))+" bearing: "+ str(tp.bearing_line(KSC_BP))

for i in vp:
	print str(i.name)+" | distance: "+str(KSC_BP.dist_line(i)) + " alt: "+str(i.alt) + " bearing: "+ str(i.bearing_line(KSC_BP))





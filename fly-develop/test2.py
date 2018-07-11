import sys
sys.path.append("./lib")
sys.path.append("./runways")
sys.path.append("./aircrafts")


from tools import *
from handbooks import *
import KSC
import iceland

log_level=1

#for i in KSC.KSC_VPP.zones:
	#print i.name+"  "+i.message
#print '=============================================='
#for i in iceland.iceland_VPP.zones:
	#print i.name+"  "+i.message



#from test2 import *
#KSC_BP = coordinates(name= 'Begin Position', lat= -0.0485935550516, lng= -74.72465205780000000, alt=   70.3741567462)
tp     = coordinates(name= 'recursive_dot',  lat= -0.0000000000000, lng=  12.48951284451766242, alt= 1500.0000000000)


#disp=KSC.runway.traffic_controller(name='testKSC', vpp=[KSC.KSC_VPP])
#disp.run()
print KSC.KSC_West.dist_line(KSC.KSC_East)
print KSC.KSC_West.bearing_line(KSC.KSC_East)
print KSC.KSC_East.bearing_line(KSC.KSC_West)
print tp.bearing_line(KSC.KSC_West)
print tp.bearing_line(KSC.KSC_East)

print 'Center: '+str(KSC.KSC_East.target_dot_from_dist_and_bear(KSC.KSC_West.bearing_line(KSC.KSC_East),(KSC.KSC_West.dist_line(KSC.KSC_East)/2),name='Center KSC VPP'))

mtest=message()
mbuff=mtest.create_message('pl-A4Aatm_142313','tc-KSC_KSC1','Hello',7656746746574)

mtest.parse_message(mbuff)
print str(mtest)


print 'buff'+str(mbuff)

#vp=KSC.KSC_VPP.get_SID(tp,KSC_BP)

#print KSC_BP.dist_line(KSC.KSC_East)
#print "taget distance: "+str(KSC_BP.dist_line(tp))+" bearing: "+ str(tp.bearing_line(KSC_BP))

#for i in vp:
	#print str(i.name)+" | distance: "+str(KSC_BP.dist_line(i)) + " alt: "+str(i.alt) + " bearing: "+ str(i.bearing_line(KSC_BP))





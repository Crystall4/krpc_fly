#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import math
import sys
sys.path.append("./lib")
sys.path.append("./runways")
import tools
import runway
import handbooks


# генерация схем подхода ухода на базе VPP.get_SID() VPP.get_STAR()
import KSC
#wrunway=KSC.KSC_VPP
#print str(wrunway.name)+':{'
#tab='\t'

#for wbear in wrunway.vpp_bearings:
	#print tab+wbear.name+':{'
	#wedge=wbear.edge2
	##for i in range(0, 360+10, 10):
	#for i in range(0, 360+10, 90):
		#wdot=wedge.target_dot_from_dist_and_bear(i,100000,name=('Raschet_'+str(i)+'_deg'))
		#print 'bear: '+str(i)
		#for j in KSC.KSC_VPP.get_SID(wdot,KSC.KSC_BP):
			#if j.alt>80:print str(j)
	


#1 пересчитать dx на 0
#2 собрать последовательно идущие трушные сектора начала которых лежат между +45 и -45(315) если их нет то задача не имеет решения
#3 расчитать крайние точки


def pereschet(dx,dy):
	dd=dy-dx
	if dd <0: dd=360-dd
	return dd
	
def podbor_dl(radius,a2,a3):
	dlpr=0.0
	s=radius/3
	zerocoord=KSC.KSC_VPP.vpp_bearings[0].edge2
	while dlpr<radius:
		d1=zerocoord.target_dot_from_dist_and_bear(45.0000,s)
		d2=d1.target_dot_from_dist_and_bear(a2,s)
		d3=d2.target_dot_from_dist_and_bear(a3,s)
		dlpr=d3.dist_line(zerocoord)
		bear=d3.bearing_line(zerocoord)
		s=s+0.1
	return str(45.0)+ ' ; '+ str(a2)+ ' ; '+ str(a3)+ ' ; '+ str(s) + ' ; '+str(bear)+ ' ; '+str(dlpr)

def raschet2(radius, a1, a2, a3):
	return (radius*1.0)/(1.0+math.sin(math.radians(180.0-90.0-(a2*1.0)))+math.sin(math.radians(180.0-90.0-(a3*1.0))))

def raschet_dl(radius, a1, a2, a3):
	s= raschet2(radius, a1, a2, a3)
	dlpr=0.0
	zerocoord=KSC.KSC_VPP.vpp_bearings[0].edge2
	d1=zerocoord.target_dot_from_dist_and_bear(a1,s)
	d2=d1.target_dot_from_dist_and_bear(a1+a2,s)
	d3=d2.target_dot_from_dist_and_bear(a1+a2+a3,s)
	dlpr=d3.dist_line(zerocoord)
	bear=d3.bearing_line(zerocoord)
	return str(a1)+ ' ; '+ str(a2)+ ' ; '+ str(a3)+ ' ; '+ str(s) + ' ; '+str(bear)+ ' ; '+str(dlpr)

def control(s, a1,a2, a3):
	zerocoord=KSC.KSC_VPP.vpp_bearings[0].edge2
	radius=raschet2(s, a1, a2, a3)
	d1=zerocoord.target_dot_from_dist_and_bear(a1,radius)
	d2=d1.target_dot_from_dist_and_bear(a1+a2,radius)
	d3=d2.target_dot_from_dist_and_bear(a1+a2+a3,radius)
	return str(d3.dist_line(zerocoord)- s)

def rasmax():
	#45.0  градусов 10666.6666666     
	#90.0  градусов 11437.0158188
	#135.0 градусов 13254.833996
	dlpr=0
	zerocoord=KSC.KSC_VPP.vpp_bearings[0].edge2
	maxangle=45.0000000000000000000
	for a in range(0, 45+1, 1):
		angle1=a*1.0 #/10.0
		for i in range(0, 45+1, 1):
			angle2=i*1.0+0.0000000000000001 #/10.0
			print 'angle1;2: '+ str(angle1) + ' ; ' + str(angle2)
			for j in range(0, 45+1, 1):
				angle3=j*1.0+0.0000000000000001 #/10.0
				print str(raschet_dl(30000.000,angle1,angle2,angle3))+' ; '
				print str(control(30000.000,angle1,angle2,angle3))+'\n'


	
#control(13254.833996)

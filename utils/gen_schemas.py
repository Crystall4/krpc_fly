#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
sys.path.append("./lib")
sys.path.append("./runways")
import tools
import runway
import handbooks


# генерация схем подхода ухода на базе VPP.get_SID() VPP.get_STAR()
import KSC
wrunway=KSC.KSC_VPP
print str(wrunway.name)+':{'
tab='\t'

for wbear in wrunway.vpp_bearings:
	print tab+wbear.name+':{'
	wedge=wbear.edge2
	#for i in range(0, 360+10, 10):
	for i in range(0, 360+10, 90):
		wdot=wedge.target_dot_from_dist_and_bear(i,100000,name=('Raschet_'+str(i)+'_deg'))
		print 'bear: '+str(i)
		for j in KSC.KSC_VPP.get_SID(wdot,KSC.KSC_BP):
			if j.alt>80:print str(j)
	


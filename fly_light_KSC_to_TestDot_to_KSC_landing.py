#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import importlib
import fly

#======================================================================================================================
# импорт модуля ЛА
airc_str='Aeris_4A_atmos'
sys.path.append("./aircrafts")
globals().update(importlib.import_module(airc_str).__dict__)

#======================================================================================================================
#импорт модулей ВПП
vpp_str='KSC'
sys.path.append("./runways")
globals().update(importlib.import_module(vpp_str).__dict__)
#vpp_str='iceland'
#globals().update(importlib.import_module(vpp_str).__dict__)


log_level= 9

flplan               = fly.fly_plan()
flplan.pf            = 'handbook'
flplan.aircraft_name = 'Aeris_4A_atmos'
flplan.begin_name    = "KSC_VPP"
flplan.begin         = KSC_VPP
flplan.to_vpp_bear   = 9
flplan.end_name      = "KSC_VPP"
flplan.land_vpp_bear = 27
flplan.CruisePlan.append(coord_from_dict(handbooks.coord.get('two_dot')))
flplan.begin_dot     = coord_from_dict(handbooks.coord.get('KSC_BP'))
flplan.plan_compile()


 
testap = fly.fly_ap(flplan)
testap.take_off()
#testap.Go()
testap.CruiseSpeed=230
testap.Cruise()
old_met=0
print "State; Trottle; HS; AtDeg; Pitch; tVertSp; VerticalSpeed; AtRoll; bearing; tHeading;tAlt;  dist_line;  landingspeed;" 
testap.landing(iceland_VPP)




#end
print 'Distance >> ', end_r.dist_line(), ' [meters]'
print 'Horizontal speed >> ', surf_flight.horizontal_speed, 'm/s'
print ""
control.sas = True

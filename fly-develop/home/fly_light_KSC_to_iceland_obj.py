import fly
 
testap = fly.fly()
testap.take_off(fly.KSP_VPP)
testap.TrottlePid.setPoint(160)
testap.maxTrottle = 1.0
testap.minTrottle = 0.1
old_met=0
print "State; Trottle; HS; AtDeg; Pitch; tVertSp; VerticalSpeed; AtRoll; bearing; tHeading;tAlt;  dist_line;  landingspeed;" 
testap.landing(fly.iceland_VPP)




#end
print 'Distance >> ', end_r.dist_line(), ' [meters]'
print 'Horizontal speed >> ', surf_flight.horizontal_speed, 'm/s'
print ""
control.sas = True

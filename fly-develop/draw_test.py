#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# from draw_test import *
import math
import krpc
import time
import sys
sys.path.append("../lib")
from tools import *
sys.path.append("../runways")
from KSC import *


# Connect to the server with the default settings
# (IP address 127.0.0.1 and port 50000)
print 'Connecting to server...'
ksp = krpc.connect(name='draw_test')
print 'Connected to server, version', ksp.krpc.get_status().version

space_center = ksp.space_center
vessel = space_center.active_vessel
orbit = vessel.orbit
ap = vessel.auto_pilot
control = vessel.control
flight = vessel.flight()
surf_flight = vessel.flight(orbit.body.reference_frame)

vsframe=vessel.surface_reference_frame
KSCN=KSC_VPP
def curr_position(krpc_vessel):
	return coordinates(name='CP', lat=krpc_vessel.flight().latitude, lng=krpc_vessel.flight().longitude, alt=krpc_vessel.flight().surface_altitude)

tp=coord_from_dict({'name':'KSC East Dot','lat':-0.05025878770915180, 'lng':-74.48951284451766242, 'alt':70.0000000000})
#вверх север восток
dw=ksp.drawing
l1=dw.add_line((0.0, 0.0, 0.0),get_surface_vector(curr_position(vessel),tp),vsframe)
print get_surface_vector(curr_position(vessel),tp)
print '(0.0, -17.417008007614566, 2460.442576991467)'
ll=dw.add_line((0.0, 0.0, 0.0),(0.0, -17.417008007614566, 2460.442576991467),vsframe)
ll.color=(0.0,1.0,0.0)
#l2=dw.add_line((0.0, 0.0, 0.0),(0.0, 0.0, 2460.77),vsframe)
#l3=dw.add_line((0.0, 0.0, 0.0),(0.0, 0.0, 2460.77),vsframe)


z=KSCN.zones[1]
for i in z.get_TakeOff_route(90):
	dw.add_line((0.0, 0.0, 0.0),get_surface_vector(curr_position(vessel),i),vsframe)

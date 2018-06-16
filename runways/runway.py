# -*- coding: utf-8 -*-

import math
import sys
sys.path.append("../lib")
import tools
coordinates = tools.coordinates

#=====================================================================================================================  


#---------------------------------------------------------------------------------------------------------------------
recursive_dot  = coordinates(name='recursive_dot', lat=-0.02022509861205912, lng=-72.18951284451766242, alt=1000.0)
recursive_dot1 = coordinates(name='recursive_dot', lat=-0.02022509861205912, lng=-76.18951284451766242, alt=600.0 )
two_dot        = coordinates(name='two_dot',        lat=1.35022509861205912,  lng=-70.48951284451766242, alt=1000.0)
#======================================================================================================================

class radialZone:
	name="default"
	message=""
	beg_deg=0
	end_deg=0
	status_TakeOff=True
	status_Landing =True
	subzones=[12,24,32]
	zone_center = ""
	TakeOff_beg_detour = [0.0,0.0,0.0]
	TakeOff_end_detour = [0.0,0.0,0.0]
	TakeOff_main_route = [0.0,0.0,0.0]
	#по высотам 12км 500-2000, 24км 1000-4500 32км 3000-6000
	TakeOff_subzones_alt=[1000,2000,3000,4000]
	Landing_beg_detour = [0.0,0.0,0.0]
	Landing_end_detour = [0.0,0.0,0.0]
	Landing_main_route = [0.0,0.0,0.0]
	def __init__(self,name="NoName",beg_deg=0,end_deg=0,status_TakeOff=False,status_Landing=False,zone_center=coordinates(name='default zone center', lat=0.0, lng=0.0, alt=0.0),subzones=[12000,24000,32000],TakeOff_beg_detour=[666.0,666.0,666.0],TakeOff_end_detour=[666.0,666.0,666.0],TakeOff_main_route=[666.0,666.0,666.0],Landing_beg_detour=[666.0,666.0,666.0],message=""):
		if beg_deg!=end_deg:
			self.name=name
			self.message=message
			self.status_TakeOff=status_TakeOff
			self.status_Landing=status_Landing
			self.zone_center =zone_center
			self.zone_center.name = '"'+name +'" zone center'
			subzones.sort()
			self.subzones=subzones
			self.TakeOff_beg_detour=TakeOff_beg_detour
			self.TakeOff_end_detour=TakeOff_end_detour
			self.TakeOff_main_route=TakeOff_main_route
			if beg_deg<end_deg:
				self.beg_deg=beg_deg
				self.end_deg=end_deg
			else:
				self.beg_deg=end_deg
				self.end_deg=beg_deg
		else:
			print "Error create zone"
	def check_belonging_bearing(self,bearing):
		return (bearing>beg_deg and bearing<end_deg)
	def check_belonging_dot(self,coord):
		bearing=coord.bearing_line_from(self.zone_center)
		return (bearing>beg_deg and bearing<end_deg and coord.dist_line_from(self.zone_center)<self.subzones[len(self.subzones)-1])
	def get_TakeOff_route(self,bearing):
		sh=0
		if status_TakeOff!=True and ((bearing-beg_deg)<(end_deg-bearing)):
			situation_route = TakeOff_beg_detour
		elif status_TakeOff!=True and ((bearing-beg_deg)>(end_deg-bearing)):
			situation_route = TakeOff_end_detour
		else: situation_route = TakeOff_main_route
		for i in situation_route:
			if i > 360.0 :
				dot=target_dot_from_dist_and_bear(bearing,subzones[sh])
			else:
				dot=target_dot_from_dist_and_bear(i,subzones[sh])
			dot.name="SID"+(sh+1)+"from "+self.name+" zone"
			dot.alt=TakeOff_subzones_alt[sh]
			route.append(dot)
			sh+=1
		return tuple(route)

class VPP:
	edge1 = ''
	edge2 = ''
	zones=[]
	def __init__(self, edge1, edge2, ;zones=[]):
		self.edge1=edge1
		self.edge2=edge2
		self.zones=zones
	def get_SID(self,target):
		#Получение схемы выхода из зоны ВПП
		#SID1:Дальний край ВПП
		#--------------SID1
		if  self.edge1.dist_line() > self.edge2.dist_line():
			self.SID1 = self.edge1
		else:
			self.SID1 = self.edge2
		
		bearing_Z=target.bearing_line_from(SID1)
		zone=''
		for nz in self.zones:
			if nz.check_belonging_bearing(bearing): zone=nz
		if zone.status_take_off:
			route=zone.get_route(bearing)
		else:
			route=zone.get_detour_route(bearing)
		#--------------SID2
		SID=[SID1,]
		for r in route:
			SID.append(r)

		return tuple(SID)			
	def get_STAR(self,coord):
		#Получение схемы подхода к ВПП
		if self.edge1.dist_line() < self.edge2.dist_line():
			#print "Sit to East direction runway"
			beg_r = self.edge1
			end_r = self.edge2
		else:
			#print "Sit to", beg_r.name," direction runway"
			beg_r = self.edge2
			end_r = self.edge1
	def glis_point(runway_beg, runway_stop, dist=12000):
		dist_t = dist/(math.sqrt(((runway_beg.lat - runway_stop.lat)**2)+((runway_beg.lng - runway_stop.lng)**2))*10471.97333333)
		glis_dot = coordinates(name='glis point from '+runway_beg.name, lat=(runway_beg.lat+dist_t*(runway_beg.lat-runway_stop.lat)), lng=(runway_beg.lng+dist_t*(runway_beg.lng-runway_stop.lng)), alt=(dist*0.1)+70.0)
		return glis_dot




#======================================================================================================================

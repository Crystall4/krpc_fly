# -*- coding: utf-8 -*-

import socket
import json
import math
import sys
sys.path.append("../lib")
from tools import *


#======================================================================================================================


#---------------------------------------------------------------------------------------------------------------------
recursive_dot  = coordinates(name='recursive_dot', lat=-0.02022509861205912, lng=-72.18951284451766242, alt=1000.0)
recursive_dot1 = coordinates(name='recursive_dot', lat=-0.02022509861205912, lng=-76.18951284451766242, alt= 600.0)
two_dot        = coordinates(name='two_dot',       lat= 1.35022509861205912, lng=-70.48951284451766242, alt=1000.0)
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
			#self.zone_center.name = '"'+name +'" zone center'
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
		return (bearing>self.beg_deg and bearing<self.end_deg)
	def check_belonging_dot(self,coord):
		bearing=coord.bearing_line_from(self.zone_center)
		return (bearing>beg_deg and bearing<end_deg and coord.dist_line_from(self.zone_center)<self.subzones[len(self.subzones)-1])
	def get_TakeOff_route(self,bearing):
		route = []
		sh=0
		if self.status_TakeOff!=True and ((bearing-self.beg_deg)<(self.end_deg-bearing)):
			situation_route = self.TakeOff_beg_detour
		elif self.status_TakeOff!=True and ((bearing-self.beg_deg)>(self.end_deg-bearing)):
			situation_route = self.TakeOff_end_detour
		else: situation_route = TakeOff_main_route
		for i in situation_route:
			if i > 360.0 :
				dot=self.zone_center.target_dot_from_dist_and_bear(bearing,self.subzones[sh])
			else:
				dot=self.zone_center.target_dot_from_dist_and_bear(i,self.subzones[sh])
			dot.name="SID "+str(sh+1)+" from "+self.name+" zone"
			dot.alt=self.TakeOff_subzones_alt[sh]
			route.append(dot)
			sh+=1
		return tuple(route)


class vpp_bearing:
	name  = ''
	VPP   = None
	edge1 = None
	edge2 = None
	def __init__(self, name='Unknown', edge1=None, edge2=None):
		self.name  = name
		self.edge1 = edge1
		self.edge2 = edge2
	def get_distance(self,CP):
		self.edge1.dist_line(CP)


class VPP:
	vpp_bearings = None
	zones = None
	
	def __init__(self, vpp_bearings, zones):
		self.vpp_bearings = vpp_bearings
		self.zones=zones

	def get_bear(self, coord):
		#Получить направление захода/выхода
		result = self.vpp_bearings[0]
		if self.vpp_bearings[0].edge1.dist_line(coord) > self.vpp_bearings[1].edge1.dist_line(coord):
			result=self.vpp_bearings[0]
		else:
			result=self.vpp_bearings[1]
		return result
		
	def get_SID(self,target,CP):
		#Получение схемы выхода из зоны ВПП
		#SID1:Дальний край ВПП
		#--------------SID1
		max_dist_bear=0.0
		bear=self.get_bear(CP)
		SID1=bear.edge1
		for bear in self.vpp_bearings:
			td = bear.get_distance(CP)
			if td > max_dist_bear:
				max_dist_bear = td
				SID1 = bear.edge1
				log(SID1)
		
		bearing_Z=target.bearing_line_from(SID1)
		zone=''
		for nz in self.zones:
			if nz.check_belonging_bearing(bearing_Z): zone=nz
		if zone.status_TakeOff:
			route=zone.get_route(bearing)
		else:
			route=zone.get_TakeOff_route(bearing_Z)
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
			
		return tuple(SID)
			
	def get_STAR_from(self,coord, get_vpp_bear=None):
		#Получение схемы подхода к ВПП
		if get_vpp_bear==None:
			pass
			#if self.edge1.dist_line_from(coord) < self.edge2.dist_line_from(coord):
				##print "Sit to East direction runway"
				#beg_r = self.edge1
				#end_r = self.edge2
			#else:
				##print "Sit to", beg_r.name," direction runway"
				#beg_r = self.edge2
				#end_r = self.edge1
		else:
			pass
		 
		STAR=[]
		
		return tuple(STAR)
		
	def glis_point(runway_beg, runway_stop, dist=12000):
		dist_t = dist/(math.sqrt(((runway_beg.lat - runway_stop.lat)**2)+((runway_beg.lng - runway_stop.lng)**2))*10471.97333333)
		glis_dot = coordinates(name='glis point from '+runway_beg.name, lat=(runway_beg.lat+dist_t*(runway_beg.lat-runway_stop.lat)), lng=(runway_beg.lng+dist_t*(runway_beg.lng-runway_stop.lng)), alt=(dist*0.1)+70.0)
		return glis_dot

#======================================================================================================================
class traffic_controller:
	name=''
	listen=''
	port=''
	status=''
	def __init__(self, name, vpp, host='127.0.0.1',port=5001):
		if name and vpp:
			self.name=name
			self.vpp=vpp
		#try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.bind((host,port))
			self.s.listen(1)
		#except Exception:
			#log('error open socket')
			#self.status='Error'
		#else:
			#self.status='Listen'
	def run(self):
		try:
			while True:
				conn, addr = self.s.accept()
				data = conn.recv(1024)
				print 'client is at', addr , data
				conn.send(data)
		except BaseException:
			conn.close()
	

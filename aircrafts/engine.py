# -*- coding: utf-8 -*-
import sys
sys.path.append("./lib")
from tools import *

class engine_mode:
	modes            = {0:"Off",1:"warm-up",2:"TakeOff mode",3:"Cruise mode",4:"Landing mode",5:"Forsage maneur mode",6:"Emergency mode"}
	statuses         = {0:"eq target mode", 1:"transient mode", 2:"pre transient mode", 3:"emergency mode", 4:"emergency off"}
	emergency_causes = {0:"not emergency", 1:"no fuel", 2:"other"}
	emergency_cause  = 0
	pre_mode         = 0
	target_mode      = 0
	status           = 0
	
	def set_target_mode(tmode):
		result=False
		return result

class engine:
	mode = engine_mode()
	krpc_engine = None
	hashtag = None
	
	def __init__(self, pengine=None):
		result = False
		if pengine.part != None:
			self.krpc_engine = pengine
			result=True
		return result
	
	def get_mode(self):
		if self.mode.status == 0:
			result=self.mode.target_mode
		if self.mode.status == 1:
			result=self.mode.status
		if self.mode.status == 2:
			result=self.mode.pre_mode
		if self.mode.status == 3 or self.mode.status == 4:
			result=6
		return result
	
	def start_test(self):
		result=False
		return result

	def set_mode(self, tmode):
		if self.mode.status == 0:
			if self.mode.target_mode == 0 and self.start_test():
				self.mode.pre_mode=self.mode.target_mode
				self.mode.status=1
				
				#Написать код старта движков
			
		if mode.status == 1:
			result=mode.status
		if mode.status == 2:
			result=mode.pre_mode
		if mode.status == 3 or mode.status == 4:
			result=6
		
		return result
			
		

class engines:
	krpc_disp = None
	mode = engine_mode()
	aengines = []
	
	def __init__(self, krpc_disp=None):
		result = True
		if krpc_disp != None:
			self.krpc_disp = krpc_disp
		else:
			result = False
		return result
	
	def attach_engine(self, pengine=None):
		
		result = True
		comment=""
		if pengine == None:
			comment = "don`t engine parametr"
			result = False
		
		if (result and (pengine.part.engine == None)):
			comment = "don`t engine"
			result = False
		
		find=False
		for en in self.aengines:
			if (result and (en.hashtag() == pengine.part.__hash__)):
				comment = "this engine is already appended"
				result  = False
		
		if result:
			oengine = engine(pengine)
			self.aengines.append(oengine)
			log(engine.part.title + " " + engine.part.__hash__() + " successfully connected")
		else:
			log("Append engine failed: " + comment)
			result=False
		return result
	




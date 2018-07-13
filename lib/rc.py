#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import socket
import threading
import Queue
import time
import json
from tools import *
import handbooks


class RadioTC:
	port=None
	host='localhost'
	status=None
	name=None
	posstr=''
	pTC=None
	status = 'pre_config'
	subdisps=[]
	subzones=[]
	
	def __init__(self,name=None, zone=None, tc_type=None,pzone=0):
		if name != None and zone != None and tc_type != None:
			station=handbooks.TCList.get(handbooks.TCZones_list.get(zone).get('name')+'_'+name,'manual defined')
			if station != 'manual defined':
				print 'Auto configure from init: '+handbooks.TCZones_list.get(zone).get('name')+'_'+name
				self.port=station.get('port')
				self.host=station.get('host')
				self.pzone=handbooks.TCZones_list.get(pzone)
				self.pTC=handbooks.TCList.get((self.pzone.get('name')+'_'+self.pzone.get('mainTC')))
				self.tc_type=tc_type
				self.zone=handbooks.TCZones_list.get(zone)
				self.name=self.zone.get('name')+'_'+name
				self.posstr='tc-'+self.name+str(tc_type)
				self.status='configured'

			else:
				self.status='unconfigured'
		
		if self.status == 'pre_config':
			print 'Not configured: '+self.status
			self.status='error'
		self.inq =Queue.Queue()
		self.outq=Queue.Queue()
		self.sysq=Queue.Queue()
	
	def __str__(self):
		return 'Traffic controller {} с позывным {}, контроллирует зону {}'.format(self.name, self.posstr, self.zone.get('name'))
			
	def configure(self, posstr=None,tc_type=None,zone=None,port=None,pzone=None):
		if port != None:
			self.port=station.get('port')
		if pzone != None:
			self.pzone=handbooks.TCZones_list.get(pzone)
			self.pTC=handbooks.TCList.get(self.pzone.get('mainTC'))
		if tc_type != None:
			self.tc_type=tc_type
		if zone != None:
			self.zone=handbooks.TCZones_list.get(zone)
			self.name=self.zone.get('name')+'_'+name
			self.host=self.host
		if posstr != None:
			self.posstr='tc-'+self.name+str(tc_type)
		self.status='configured'
					
	def reciver(self, name, client, inq, sysq):
		run=True
		print 'Run receiver '+ name + ' timeout= '+str(client.gettimeout())
		tname=''
		while run:
			try:
				# Здесь поток блокируется до тех пор
				# пока не будут считаны все имеющиеся
				# в сокете данные
				data, addr = client.recvfrom(1024)
			except:
				#print 'socket except'
				pass 
			else:
				#if data: # Если есть данные
					# Отправляем в очередь сообщений кортеж
					# содержащий сокет отправителя
					# и принятые данные
				mess=message()
				mess.parse_message(data, addr)
				print('{}: От {} получено: {}'.format(name, str(addr), data.decode()))
				inq.put((addr, mess))
				
				
			#print 'receiver '+name+' cikl'	
			try:
	            # Получаем из очереди сообщений
	            # сокет отправителя и принятые данные
				tname, sysmessage = sysq.get(timeout=0.1)
			except Queue.Empty:
				pass # Игнорируем отсутствие сообщений в очереди
			else: # Если же сообщения есть
				if tname== name:
					print('{}: получено системное сообщение: {}'.format(name, sysmessage.decode()))
					sysq.task_done() # Сообщаем, что сообщение обработано
				else: sysq.put((tname, sysmessage))
			if  ((tname == name) and (sysmessage == 'exit')) : 
				run=False
				print 'Stop reciver '+ name
				break

	def readq(self,q,ttimeout=1):
		try:
			# Получаем из очереди сообщений
			# сокет отправителя и принятые данные
			qmess = tuple(q.get(timeout=ttimeout))
		except Queue.Empty:
			result = None # Обрабатываем отсутствие сообщений в очереди
		else: # Если же сообщения есть
			result = qmess
			q.task_done() # Сообщаем, что сообщение обработано

	def sender(self, name, connections, inq):
		print 'Run sender '+ name + ' timeout= '+str(connections.gettimeout())
		run = True
		while run:
			try:
				# Получаем из очереди сообщений
				# сокет отправителя и принятые данные
				sender, message = inq.get(timeout=5)
			except Queue.Empty:
				pass # Игнорируем отсутствие сообщений в очереди
			else: # Если же сообщения есть
				print 'message inq: '+str(sender)+' : '+str(message)
				if sender == name:
					print(name+': получено системное сообщение: {}'.format( message.decode()))
					inq.task_done() # Сообщаем, что сообщение обработано
					if message == 'exit':
						run=False
						print 'Stop sender '+ name
						break
				else:
					connections.sendto(message.buff, sender)
					print('Ответ {} отправлен клиенту: {}'.format( message.decode(), str(sender)))
					inq.task_done() # Сообщаем, что сообщение обработано

	def registered(self):
		print 'Start registry'
		if self.status != 'configured':
			print 'Not configured '+self.status
			return 'Error'
		
		param_buff={'posstr':self.posstr, 'zone':self.zone.get('i'), 'tc_type':self.tc_type, 'port':self.port}
		mess=message()
		self.p_udp_in_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.p_udp_in_socket.settimeout(5)
		threading.Thread(target=self.reciver, args=('register_rec',self.p_udp_in_socket, self.inq, self.sysq)).start()
		if ((self.zone != 0) and (self.tc_type !=0)):
			print 'Запрос на регистрацию TC: {} с позывным {}, в зоне {} на частоте {}'.format(self.name, self.posstr, self.zone.get('name'), self.port)
			print 'отправлен TC {} на частоте {}'.format('tc-'+self.pzone.get('name')+'_'+self.pzone.get('mainTC')+'0', self.pTC.get('port'))
			mess.create_message(self.posstr+'_pre','tc-'+self.pzone.get('name')+'_'+self.pzone.get('mainTC')+'0','tc register request',param_buff)			
			addr=None
			data=None
			self.p_udp_in_socket.sendto(mess.buff, (self.pTC.get('host'),self.pTC.get('port')))
			re=self.readq(self.inq,10)
			if re != None:
				addr,data=re
			else:
				data =None
				addr =None
			if data != None:
				mess.parse_message(data)
				if mess.m_name == 'tc register reconfig':
					if mess.param.get('zone') == self.zone.get('i'): 
						self.configure(posstr=mess.param.get('posstr'),tc_type=mess.param.get('tc_type'),zone=mess.param.get('zone'),port=mess.param.get('port'))
						mess.create_message(self.posstr+'_pre',self.pzone.get('mainTC'),'OK')
						self.status='registered'
						udp_socket.sendto(mess.buff, (self.pTC.get('host'),self.pTC.get('port')))
						mess.create_message(self.posstr,self.pzone.get('mainTC'),'tc register rep',param_buff)
						udp_socket.sendto(mess.buff, (self.pTC.get('host'),self.pTC.get('port')))
						sysq.put(('register_rec', 'exit'))
						return True
					else:
						mess.create_message(self.posstr+'_pre',self.pzone.get('mainTC'),'Bad')
						udp_socket.sendto(mess.buff, (self.pTC.get('host'),self.pTC.get('port')))
						self.status='register trable configure'
						mess.create_message(self.posstr+'_pre',self.pzone.get('mainTC'),'tc register request',param_buff)
						udp_socket.sendto(mess.buff, (self.pTC.get('host'),self.pTC.get('port')))
						result	= False
			else:
				self.status='register trable not request'
				result	= False
				
			if result == False:
				addr,data=self.inq.get(timeout=10)
				if data != None:
					mess.parse_message(data)
					if mess.m_name == 'tc register reconfig':
						if mess.param.get('zone') == self.zone.get('i'): 
							self.configure(posstr=mess.param.get('posstr'),tc_type=mess.param.get('tc_type'),zone=mess.param.get('zone'),port=mess.param.get('port'))
							mess.create_message(self.posstr+'_pre',self.pzone.get('mainTC'),'OK')
							self.status='registered'
							udp_socket.sendto(mess.buff, (self.pTC.get('host'),self.pTC.get('port')))
							mess.create_message(self.posstr,self.pzone.get('mainTC'),'tc register rep',param_buff)
							udp_socket.sendto(mess.buff, (self.pTC.get('host'),self.pTC.get('port')))
							result	= True
						else:
							mess.create_message(self.posstr+'_pre',self.pzone.get('mainTC'),'Bad')
							udp_socket.sendto(mess.buff, (self.pTC.get('host'),self.pTC.get('port')))
							self.status='register trable'
							mess.create_message(self.posstr+'_pre',self.pzone.get('mainTC'),'tc register request',param_buff)
							udp_socket.sendto(mess.buff, (self.pTC.get('host'),self.pTC.get('port')))
							result	= False
				else:
					self.status='register trable not request'
					result	= False
			sysq.put(('register_rec', 'exit'))
			self.sysq.put(('register_rec','exit'))
		else:
			print '{} проверяет возможность стать глобальным TC:  с позывным {}, на частоте {}'.format(self.name, self.posstr, self.port)
			mess.create_message(self.posstr+'_pre',self.zone.get('mainTC'),'tc register request',param_buff)
			#threading.Thread(target=self.reciver, args=('register_rec',self.p_udp_in_socket, self.inq, self.sysq)).start()
			addr=None
			data=None
			self.p_udp_in_socket.sendto(mess.buff, (self.pTC.get('host'),self.pTC.get('port')))
			re=self.readq(self.inq,3)
			self.sysq.put(('register_rec','exit'))
			if re != None:
				addr,data=re
			else:
				data =None
				addr =None
			if data != None:
				self.status='trable global TC'
				result	= False
				return False
			else:
				self.status='registered'
				result	= True
				return True
		
		return result
		
	def start_sub_threads(self, addr, mess):
		rc_queue=Queue.Queue()
		sub_thread=threading.Thread(target=self.job, args=(mess.sender, addr,rc_queue))
		thr_l={'name':mess.sender,'t_addr':addr,'rc_queue':rc_queue,'thread':sub_thread}
		self.sub_threads.append(thr_l)

	def find_thread(self,name):
		result='not find'
		for i in self.sub_threads: 
			if i.get('name') == name: return i
	
	def job(self, name, addr, rcq):
		print 'Run job '+ name + 'For ' + addr + 'client'
		while run:
			try:
				# Получаем из очереди сообщений
				# сокет отправителя и принятые данные
				sender, message = rcq.get(timeout=0.1)
			except Queue.Empty:
				pass # Игнорируем отсутствие сообщений в очереди
			else: # Если же сообщения есть
				if message == 'exit':
					run=False
					print 'Stop job '+ name
					break
					return 'exit'
				else:
					self.outq.put((addr,message))
					print('Ответ {} клиенту {} поставлен в очередь отправки'.format( message.decode(), str(sender)))
					rcq.task_done() # Сообщаем, что сообщение обработано	
	
	def find_zone(self, name):
		subzone=None
		for hzone in handbooks.TCZones_list.keys():
			if hzone.get('name')==name:
				subzone=hzone
				status='find zone in handbook'
		if status=='find zone in handbook':
			return {'result':True, 'from':'handbook', 'zone':subzone}
		for localsz in self.subzones:
			if localsz.get('name')==name:
				subzone=localsz
				status='find zone in local'
		if status=='find zone in local':
			return {'result':True, 'from':'local', 'zone':subzone}
		if 	status==None:
			return {'result':False, 'from':'', 'zone':None}

	def reg_sub_tc(self,rc_data):
		subzone=None
		subdisp=None
		status=''
		zp=rc_data.get('param')
		#проверка на существование подзоны
		fz=self.find_zone(zp.get('zone'))
		if fz.get('result'):
			if fz.get('from') == 'handbook':
				subzone=fz.get('zone')
				if subzone.get() ==  and 
			
			
			
			
			#проверка на существование диспа в подзоне
			for stc in self.subdisps:
				if stc.get('name')==zp.get('name'):
					pass
			#сохранение диспа в массиве подчиненных диспов
			#внесение измений в запись подзоны о диспетчере
		else:
			#не найдена зона
		
	def run(self):
		self.registered()
		self.p_udp_in_socket.close
		if self.status != 'registered':
			return 'Error'
		else:
			print 'TC: {} с позывным {}, приступает к работе в зоне {} на частоте {}'.format(self.name, self.posstr, self.zone.get('name'), self.port)
		self.main_udp_in_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.main_udp_in_socket.settimeout(1)
		self.main_udp_in_socket.bind((self.host, self.port))
		self.main_rc_thread=threading.Thread(target=self.reciver, args=('main_reciver',self.main_udp_in_socket, self.inq, self.sysq))
		self.main_rc_thread.start()
		self.main_send_thread=threading.Thread(target=self.sender, args=('main_send',self.main_udp_in_socket, self.outq))
		self.main_send_thread.start()
		self.sub_threads=[]
		mess=message()
		run=True

		while run:
			rc_data=None
			try:
				rc_addr,rc_data=self.inq.get(timeout=0.1)
			except:
				pass
			
			if rc_data :
				print 'Получено: {} от {} c с параметрами {}'.format(rc_data.m_name, rc_data.sender, rc_data.param)
				if rc_data.m_name=='Hello':
					fthr=self.find_thread(rc_data.sender)
					if fthr != 'not find':
						fthr.get('sys_queue').put('exit')
						fhtr.get('threads').join()
					self.start_sub_threads(rc_addr,rc_data)
				elif (rc_data.m_type>10 and rc_data.m_type<220):
					fthr=self.find_thread(rc_data.sender)
					if fthr != 'not find':
						fthr.get('sys_queue').put(rc_data)
					else:
						self.outq.put((rc_data.sender_addr,rc_data))
				elif rc_data.m_name=='tc register request':
					self.reg_sub_tc(rc_data)
				elif rc_data.m_name=='sys command':
					if rc_data.param == 'shutdown':
						run = False
						print ''
						break
					elif rc_data.param == 'hz':
						pass
		
		for i in self.sub_threads:
			i.get('rc_queue').put((i.get('name'),'exit'))
			i.get('threads').join()
			
		self.sysq.put(('main_reciver','exit'))
		self.sysq.put(('register_rec','exit'))
		self.outq.put(('main_send','exit'))
		
		self.main_rc_thread.join()
		self.main_send_thread.join()
		print 'stop main'


	

		
		
		
		
			
			
	

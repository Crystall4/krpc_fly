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
	def __init__(self,name=None, zone=None, tc_type=None,pzone=0):
		if name and zone and tc_type:
			station=handbooks.TCList.get(zone+'_'+name,'manual defined')
			if station != 'manual defined':
				self.port=station.get('port')
				self.host=station.get('host')
				self.pzone=handbooks.TCZones_list.get(pzone)
				self.pTC=handbooks.TCList.get(self.pzone.get('mainTC'))
				self.tc_type=tc_type
				self.zone=handbooks.TCZones_list.get(zone)
				self.name=self.zone.get('name')+'_'+name
				self.posstr='tc-'+self.name+str(tc_type)
				self.status='configured'

			else:
				self.status='unconfigured'
		if ((self.status != 'configured') or (self.status != 'unconfigured')):
			self.status='error'
		self.inq =Queue.Queue()
		self.outq=Queue.Queue()
		self.sysq=Queue.Queue()
			
	def configure(self, posstr=self.posstr,tc_type=self.tc_type,zone=self.zone,port=self.port,pzone=self.pzone.get('i')) :
		self.port=station.get('port')
		self.host=self.host
		self.pzone=handbooks.TCZones_list.get(pzone)
		self.pTC=handbooks.TCList.get(self.pzone.get('mainTC'))
		self.tc_type=tc_type
		self.zone=handbooks.TCZones_list.get(zone)
		self.name=self.zone.get('name')+'_'+name
		self.posstr='tc-'+self.name+str(tc_type)
		self.status='configured'
					
	def reciver(self, name, client, inq, sysq):
		run=True
		while run:
			try:
				# Здесь поток блокируется до тех пор
				# пока не будут считаны все имеющиеся
				# в сокете данные
				data, addr = client.recvfrom(1024)
				if data: # Если есть данные
					# Отправляем в очередь сообщений кортеж
					# содержащий сокет отправителя
					# и принятые данные
					inq.put((addr, data))
					print('От {} получено: {}'.format(str(addr), data.decode()))
                
			except:
				break #В случае ошибки выходим из цикла
			try:
	            # Получаем из очереди сообщений
	            # сокет отправителя и принятые данные
				tname, message = sysq.get(timeout=1)
			except Queue.Empty:
				pass # Игнорируем отсутствие сообщений в очереди
			else: # Если же сообщения есть
				if tname== name
					print('получено системное сообщение: {}'.format( message.decode()))
					sysq.task_done() # Сообщаем, что сообщение обработано
				else: sysq.put((tname, message))
						
			if  ((tname == name) and (message == 'exit')) : 
				run=False
				break

	def sender(self, name, connections, inq):
		while run:
	        try:
	            # Получаем из очереди сообщений
	            # сокет отправителя и принятые данные
	            sender, message = q.get(timeout=0.1)
	        except Queue.Empty:
	            pass # Игнорируем отсутствие сообщений в очереди
	        else: # Если же сообщения есть
	            connections.sendto(message, sender)
	            print('Ответ {} отправлен клиенту: {}'.format( message.decode(), str(sender)))
	            q.task_done() # Сообщаем, что сообщение обработано

	def registered(self):
		if self.status != 'configured': return 'Error'
		param_buff={'posstr':self.posstr, 'zone':self.zone.get('i'), 'tc_type':self.tc_type, 'port':self.port}
		mess=message()
		if ((self.zone != 0) and (self.tc_type !=0)):
			mess.create_message(self.posstr+'_pre',self.pzone.get('mainTC'),'tc register request',param_buff)
			self.p_udp_in_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			threading.Thread(target=self.reciver, args=('register_rec',self.p_udp_in_socket, self.inq, self.sysq)).start()
			addr=None
			data=None
			udp_socket.sendto(mess.buff, (self.pTC.get('host'),self.pTC.get('port')))
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
		else:
			mess.create_message(self.posstr+'_pre',self.zone.get('mainTC'),'tc register request',param_buff)
			threading.Thread(target=self.reciver, args=('register_rec',self.p_udp_in_socket, self.inq, self.sysq)).start()
			addr=None
			data=None
			udp_socket.sendto(mess.buff, (self.pTC.get('host'),self.pTC.get('port')))
			addr,data=self.inq.get(timeout=10)
			if data != None:
				self.status='trable global TC'
				return False
			else:
				self.status='registered'
				return True
		return result
		
	def start_sub_threads(self, addr, mess):
		thr_l={'name':mess.sender,'t_addr':addr,'rc_queue':Queue.Queue()}
		self.sub_threads.append(thr_l)
		self.main_rc_thread=threading.Thread(target=self.job, args=(mess.sender, addr,thr_l.get('rc_queue')))

	def find_thread(self,name):
		result='not find'
		for i in self.sub_threads: if i.get('name') == name: return i
	
	def job(self, name, addr rcq):
		while run:
			try:
				# Получаем из очереди сообщений
				# сокет отправителя и принятые данные
				sender, message = q.get(timeout=0.1)
			except Queue.Empty:
				pass # Игнорируем отсутствие сообщений в очереди
			else: # Если же сообщения есть
				self.outq.put((addr,message))
				print('Ответ {} клиенту {} поставлен в очередь отправки'.format( message.decode(), str(sender)))
				q.task_done() # Сообщаем, что сообщение обработано	
		
	def run(self):
		self.registered()
		if self.status != 'registered': return 'Error'
		self.main_udp_in_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.main_rc_thread=threading.Thread(target=self.reciver, args=('main_rec',self.main_udp_in_socket, self.inq, self.sysq))
		self.main_rc_thread.start()
		self.main_send_thread=threading.Thread(target=self.sender, args=('main_send',self.main_udp_in_socket, self.outq))
		self.main_send_thread.start()
		self.sub_threads=[]
		mess=message()
		run=True
		
		while run:
			rc_data=None
			rc_addr,rc_data=self.inq.get(timeout=0.1)
			if data :
				mess.parse_message(rc_data)
				if mess.m_name=='Hello':
					fthr=self.find_thread(mess.sender)
					if fthr != 'not find':
						fthr.get('sys_queue').put('exit')
							
					self.start_sub_threads(rc_addr,mess)


		
		
		
		
			
			
	

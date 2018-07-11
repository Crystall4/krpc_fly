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
	host=None
	status=None
	name=None
	posstr=''
	def __init__(self,name=None, zone=None, tc_type=None,pzone=0):
		if name and zone and tc_type:
			station=handbooks.TCList.get(zone+'_'+name,'manual defined')
			if station != 'manual defined':
				self.port=station.get('port')
				self.host=station.get('localhost')
				self.pzone=handbooks.TCZones_list.get(pzone)
				self.tc_type=tc_type
				self.zone=handbooks.TCZones_list.get(zone)
				self.name=self.zone.get('name')+'_'+name
				self.posstr='tc-'+self.name+str(tc_type)
				self.status='configured'
				self.inq =Queue.Queue()
				self.outq=Queue.Queue()
				self.sysq=Queue.Queue()
			else:
				self.status='unconfigured'
		if ((self.status != 'configured') or (self.status != 'unconfigured'))
			self.status='error'
			
	def reciver(self, client, inq, name, sysq):
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
					if data == name+'exit':
					else:
						inq.put((addr, data))
						print('От {} получено: {}'.format(str(addr), data.decode()))
                
			except:
				break # В случае ошибки выходим из цикла
		try:
            # Получаем из очереди сообщений
            # сокет отправителя и принятые данные
            tname, message = sysq.get(timeout=0.1)
        except Queue.Empty:
            pass # Игнорируем отсутствие сообщений в очереди
        else: # Если же сообщения есть
			if tname== name or tname=='all':
				print('получено системное сообщение: {}'.format( message.decode()))
				if tname==name: sysq.task_done() # Сообщаем, что сообщение обработано
		if  data == name+'exit': break
	
	def registered(self):
		if self.status != 'configured': return 'Error'
		param_buff={'posstr':self.posstr, 'zone':self.zone.get('i'), 'tc_type':self.tc_type, 'port':self.port}
		mess=message()
		if ((self.zone != 0) and (self.tc_type !=0)):
			mess.create_message(self.posstr+'_pre',self.pzone.get('mainTC'),'tc register request',param_buff)
			self.send_request(mess)
			udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			udp_socket.sendto(mess.buff, (self.host,self.port))
			

		
			
				
				
				
			


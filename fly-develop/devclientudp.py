#! /usr/bin/env python2
# -*- coding: utf-8 -*-


import socket
import json
import time
import sys
sys.path.append("./lib")
from tools   import *

tp = coordinates(name= 'recursive_dot',  lat= -0.0000000000000, lng=  12.48951284451766242, alt= 1500.0000000000)
mtest=message()
mbuff=mtest.create_message('pl-A4Aatm_142313','tc-KSC_KSC1','test param',tp.get())
print 'mbuff: '+str(mbuff)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = 'localhost'
port = 1777
addr = (host,port)


#encode - перекодирует введенные данные в байты, decode - обратно
#Отправка
#data = str.encode(buff)
print time.clock()
udp_socket.sendto(mbuff, addr)


#получение
data,addr = udp_socket.recvfrom(1024)
print 'print: '+str(data)
#data = bytes.decode(data)

mtest.parse_message(data)
print 'parsing message ', str(mtest)

print 'parsing param ',str(coord_from_dict(mtest.param))

udp_socket.close()

#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import socket

import sys
sys.path.append("./lib")
sys.path.append("./runways")
from tools   import *
from KSC     import *
from iceland import *

host = 'localhost'
port = 1777
#socket - функция создания сокета 
#первый параметр socket_family может быть AF_INET или AF_UNIX
#второй параметр socket_type может быть SOCK_STREAM(для TCP) или SOCK_DGRAM(для UDP)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#bind - связывает адрес и порт с сокетом
udp_socket.bind((host,port))

n='n'
y='y'
#Бесконечный цикл работы программы
while True:
    
    print('wait data...')
    
    #recvfrom - получает UDP сообщения
    conn, addr = udp_socket.recvfrom(1024)
    print('client addr: ', addr)
    print('data: ',conn)
    
    #sendto - передача сообщения UDP
    udp_socket.sendto(conn, addr)

udp_socket.close()

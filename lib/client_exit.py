#! /usr/bin/env python2
# -*- coding: utf-8 -*-


import socket
import json
import time
import sys
sys.path.append("./lib")
from tools   import *

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = 'localhost'
port = 5000
addr = (host,port)
mess=message()
mess.create_message('Admin','tc-Global_SuperViser0','sys command','shutdown')
udp_socket.sendto(mess.buff, addr)
time.sleep(1.0)
udp_socket.sendto(mess.buff, addr)
udp_socket.close()

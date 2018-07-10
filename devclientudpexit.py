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
port = 1777
addr = (host,port)
udp_socket.sendto('exit', addr)
time.sleep(0.1)
udp_socket.sendto('', addr)
udp_socket.close()

#! /usr/bin/env python2
# -*- coding: utf-8 -*-


import socket
import json
import sys
sys.path.append("./lib")
from tools   import *

tp = coordinates(name= 'recursive_dot',  lat= -0.0000000000000, lng=  12.48951284451766242, alt= 1500.0000000000)
buff = json.dumps(tp.get())
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 5001
s.connect((host, port))
s.send(buff)  
data = s.recv(1000000) 
pdata=json.loads(data)
sendp=coordinates(name= pdata.get('name'),  lat= pdata.get('lat'), lng= pdata.get('lng'), alt= pdata.get('alt'))
print 'received ', data,' ', len(data), ' bytes'
print 'parsing dict ', pdata
print 'parsing object ', sendp.__str__()
s.close()

#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import socket
import threading
import Queue
import time
import json
import tools
import handbooks


class RadioTC:
	port=None
	host=None
	status=None
	name=None
	def __init__(self,name=None, zone=None, tc_type=None):
		if name and zone and tc_type:
			station=handbooks.TCList.get(zone+'_'+name,'manual defined')
			if station != 'manual defined':
				self.port=station.get('port')
				self.host=station.get('localhost')
				self.name=name
				
			


#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import threading
import Queue
import sys
sys.path.append("./lib")
sys.path.append("./runways")
import tools
import runway
import handbooks


# генерация схем подхода ухода на базе VPP.get_SID() VPP.get_STAR()
import KSC

#1 пересчитать dx на 0
#2 собрать последовательно идущие трушные сектора начала которых лежат между +45 и -45(315) если их нет то задача не имеет решения
#3 расчитать крайние точки
#угол под которым будет находится точка выхода = a1+(a2*0.6666666666666666)+(a3*0.3333333333333333)
#угол с которым будет выход a1+a2+a3
#пока лучшее это макс а1 + (a2,a3) примерно пополам если пополам не получается то а3>a2
#10 0 = 36.1
#10 1 = 40.1
#10 2 = 44.9
#?????radius/(math.sin(math.radians(0))+math.sin(math.radians(180-90-a2))+math.sin(math.radians(180-90-a3)))



def readq(q,ttimeout=1):
		try:
			# Получаем из очереди сообщений
			# сокет отправителя и принятые данные
			qmess = q.get(timeout=ttimeout)
		except Queue.Empty:
			result = None # Обрабатываем отсутствие сообщений в очереди
		else: # Если же сообщения есть
			result = qmess
			q.task_done() # Сообщаем, что сообщение обработано
		return result

def pereschet(dx,dy):
	dd=dy-dx
	if dd <0: dd=360-dd
	return dd

def raschet1(dy):
	if dy <45:
		return '1/3d ['+str(dy)+',0,0]'
	elif dy>315:
		return '1/3d ['+str(0-(360-dy))+',0,0]'

zerocoord=KSC.KSC_VPP.vpp_bearings[0].edge2

def podbor_dl(radius,a1,a2,a3,lq):
	dlpr=0.0
	s=radius/3
	while dlpr<radius:
		d1=zerocoord.target_dot_from_dist_and_bear(a1,s)
		d2=d1.target_dot_from_dist_and_bear(a1+a2,s)
		d3=d2.target_dot_from_dist_and_bear(a1+a2+a3,s)
		dlpr=d3.dist_line(zerocoord)
		bear=d3.bearing_line(zerocoord)
		s=s+0.1
	lq.put( str(a1)+ ' ; '+ str(a2)+ ' ; '+ str(a3)+ ' ; '+ str(s) + ' ; '+str(bear)+ ' ; '+str(dlpr))

def rasmax(angle2q,n,lq):
	#45.0  градусов 10666.6666666     
	#90.0  градусов 11437.0158188
	#135.0 градусов 13254.833996
	run=True
	#print 'rasmax thread № '+str(n)+' started'
	while run:
		mess=readq(angle2q)
		if mess == None: pass
		elif mess== 'Exit':
			#print 'rasmax №'+str(n)+' get Exit \n'
			run=False
		else:
			#print 'rasmax №'+str(n)+' angle2: '+ str(angle2)
			angle1,angle2,angle3=mess
			podbor_dl(32000.000,angle1,angle2,angle3,lq)
	#print 'rasmax №'+str(n)+' shutdown \n'		
	

def log_thread(lq):
	logfile='podborthr.log'
	f = open(logfile, 'w')
	f.write('Log started')
	f.close()
	run=True
	f = open(logfile, 'a')
	print 'log thread started'
	while run:
		mess=readq(lq)
		if mess == None: pass
		elif mess=='Exit':
			#f.write('logthread get Exit \n')
			run=False
		else: 
			f.write(mess+'\n')
	f.write('logthread Shutdown \n')
	print 'logthread Shutdown \n'
	f.close()



logq=Queue.Queue(maxsize=1073741824)
a2q =Queue.Queue(maxsize=10485760)

logq.put('Log thread started...')
print 'Log thread started...'
log_thr=threading.Thread(target=log_thread, args=(logq,))
log_thr.start()

logq.join()
print 'Log thread started...Ok'

print 'Work threads started...'
maxthreads=64
threads=[]
for i in range(0, maxthreads, 1):
	threads.append(threading.Thread(target=rasmax, args=(a2q,i+1,logq)))
	
for i in threads:
	i.start()
print 'Work threads '+str(len(threads))+' start'

for a in range(36, 45+1, 1):
	angle1=a
	for i in range(0, 45+1, 1):
		angle2=i#/10.0
		print 'a2q put '+str(angle1)+' '+str(angle2)
		for j in range(0, 45+1, 1):
			angle3=j#/10.0
			a2q.put((angle1,angle2,angle3),timeout=1000)


a2q.join()
print 'a2q clean'
	
for i in range(0, maxthreads*2, 1):
	a2q.put('Exit')
	a2q.put('Exit')
	
for i in threads:
	a2q.put('Exit')
	a2q.put('Exit')
	i.join()


logq.join()

logq.put('Exit')	
logq.put('Exit')

log_thr.join()




def control(s):
	zerocoord=KSC.KSC_VPP.vpp_bearings[0].edge2
	d1=zerocoord.target_dot_from_dist_and_bear(45.000000,s)
	d2=d1.target_dot_from_dist_and_bear(90.000000,s)
	d3=d2.target_dot_from_dist_and_bear(135.000000,s)
	print d3.dist_line(zerocoord)
	
#control(13254.833996)

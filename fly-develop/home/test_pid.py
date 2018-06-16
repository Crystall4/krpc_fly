import pid
import math 
from Tkinter import *


root = Tk()

canv = Canvas(root, width = 1900, height = 1000, bg = "lightgray", cursor = "pencil")


masx = 20.0
masy = 20.0
First_x = -10;

#for i in range(20):
	#k = i+1-10
	#canv.create_line(k *(1000/masx) + 500,  -5 + 500, k *(1000/masx)+ 500, 5 + 500, width = 0.5, fill = 'black')
	#canv.create_text(k *(1000/masx) + 505, -10 + 500, text = str(k), fill="purple", font=("Helvectica", "10"))
	#canv.create_line(-5 + 500, 500-k*(1000/masy), 5 + 500, 500-k*(1000/masy), width = 0.5, fill = 'black')
	#canv.create_text(10 + 500, 500-k*(1000/masy), text = str(k), fill="purple", font=("Helvectica", "10"))
	
#for i in range(22):
	#k = i+1.5-11
	#canv.create_line(k *(1000/masx) + 500,  -3 + 500, k *(1000/masx)+ 500, 3 + 500, width = 0.5, fill = 'black')
	#canv.create_line(-3 + 500, 500-k*(1000/masy), 3 + 500, 500-k*(1000/masy), width = 0.5, fill = 'black')
	##canv.create_line(k *(1000/masx) + 500,  0, k *(1000/masx)+ 500, 1000, width = 0.1, fill = 'black')
	##canv.create_line(0, 500-k*(1000/masy), 1000, 500-k*(1000/masy), width = 0.1, fill = 'black')
# buran?
#Kp = 75
#Ki = 0.001
#Kd = 150
Kp = 7.5
Ki = 0.0001
Kd = 15.0
p=pid.PID(Kp,Ki,Kd)
speed=100
old_speed=speed
tspeed = 150
acc = 0
timestep=0.3
p.setPoint(tspeed)
count=0
dPID=0
time=0.01
#buran?
#m=92000000
#currtd=20000000.0
#maxtd = 40000000.0
m=37000000
maxtd = 22571418.0
currtd=maxtd/2
ls=1
masx = 2000.0
miny = 90.0
masy = 210 #tspeed + (tspeed*0.1)
#canv.create_line(950,1900,950,0,width=2,arrow=LAST) 
y=1000-((1000/(masy-miny))*(tspeed-miny))
canv.create_line(0,y,1900,y,width=2,arrow=LAST, fill="red") 
y=1000-((1000/(masy-miny))*(speed-miny))
canv.create_line(0,y,1900,y,width=2,arrow=LAST, fill='green')
revers=True
while (dPID <=1000 and count<100000):
	cpid=p.update(speed,time)
	#cpid=1
	oldtd=currtd
	#currtd=oldtd+((cpid*maxtd)/((maxtd-oldtd)**2))
	acctd=(((cpid*maxtd)-oldtd)-(oldtd/maxtd))/4
	currtd=round(oldtd+(acctd*timestep),4)
	if currtd>maxtd:
		currtd=maxtd
	if currtd<0.000001:
		currtd = 0.000001
	ls=0.82*(1.293*(speed*speed)/2)*837
	acc=currtd/m
	brk=ls/m
	speed= (acc*timestep)+old_speed-(brk*timestep)
	En=m*speed
	count+=1
	if (abs(old_speed-speed)<0.0000000001 and abs(speed-tspeed)<0.25):
		dPID+=1
	else : dPID=0
	#if revers and dPID>=150 :
		#print count,";",'{:4f} ; {:3f}'.format(speed,cpid),";",currtd/1000000,";",acc,";",ls,";",En
		#tspeed = 120
		#p.setPoint(tspeed)
		#revers=False
	old_speed=speed
	time += timestep
	y=1000-((1000/(masy-miny))*(speed-miny))
	#print count,";",'{:4f} ; {:3f}'.format(speed,cpid),";",currtd/1000000,";",acc,";",ls,";",En
	canv.create_oval(count/25, y, count/25 + 1, y + 1, fill = 'black')
	y=1000-((1000/(masy-miny))*((cpid*100+100)-miny))
	canv.create_oval(count/25, y, count/25 + 1, y + 1, fill = 'black')
tspeed = 120
p.setPoint(tspeed)

print count,";",'{:4f} ; {:3f}'.format(speed,cpid),";",currtd/1000000,";",acc,";",brk,";",En
canv.pack()	
root.mainloop()

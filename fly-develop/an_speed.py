import pid
import math 
from Tkinter import *


root = Tk()


masx = 20.0
masy = 20.0
First_x = 0;


logfile=open("fly_heavy_stearwing.log",'r')

colvolines = 0
maxspeed   = 0 
minspeed   = 0
maxtrottle = 1
mintrottle = 0
parr = []

for line in logfile:
	#if line.startswith("Nabor Vblcotbl") or line.startswith("Razvorot") or line.startswith("Recursive dot") or line.startswith("preRunway") or line.startswith("Runway") or line.startswith("Glissada"):
	if line.startswith("preRunway") or line.startswith("Runway") or line.startswith("Glissada"):
	#if line.startswith("Runway"):
		rd=line.split(';')
		colvolines +=1
		precc    = [float(rd[1]),float(rd[2]),float(rd[11])]
		maxspeed = max(maxspeed, max(precc[1],precc[2]))
		minspeed = min(minspeed, min(precc[1],precc[2]))
		parr.append(precc)


maxspeed = maxspeed*1.05
minspeed = minspeed*0.95
width   = 1900		
height  = 1000
xstep   = float(width)/colvolines
ytstep  = height/1.1
yspstep = height/float(maxspeed-minspeed)

old_x=0
canv = Canvas(root, width = width, height = height, bg = "lightgray", cursor = "pencil")
old_ytrottle =height
old_ylspeed  =height
old_yspeed   =height
old_yfllapspeed = height
for i in range(colvolines):
	x=xstep*i
	yspeed  =height-((parr[i][1]-minspeed)*yspstep)
	yfllapspeed=height-(((parr[i][2]*1.05)-minspeed)*yspstep)
	ylspeed =height-((parr[i][2]-minspeed)*yspstep)
	ytrottle=height-(ytstep*parr[i][0])
	print parr[i][2],ylspeed, parr[i][1],yspeed, x
	canv.create_line(old_x, old_ytrottle, x, ytrottle, width = 1.0, fill = 'red')
	canv.create_line(old_x, old_yfllapspeed,  x, yfllapspeed, width = 1.0, fill = 'black')
	canv.create_line(old_x, old_ylspeed,  x, ylspeed, width = 1.0, fill = 'black')
	canv.create_line(old_x, old_yspeed,   x, yspeed, width = 1.0, fill = 'green')
	old_ytrottle = ytrottle
	old_x = x
	old_yfllapspeed = yfllapspeed
	old_ylspeed = ylspeed
	old_yspeed = yspeed
	#canv.create_oval(x, yspeed, x + 1, yspeed + 1, fill = 'black')
	#canv.create_oval(x, ylspeed, x + 1, ylspeed + 1, fill = 'black')

canv.pack()	
root.mainloop()
	

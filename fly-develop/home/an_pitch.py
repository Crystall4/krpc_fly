import pid
import math 
from Tkinter import *


root = Tk()


masx = 20.0
masy = 20.0
First_x = 0;


logfile=open("fly_heavy_stearwing.log",'r')

colvolines = 0
maxpitch   = 0 
minpitch   = 0
maxspeed = 1
minspeed = 0
parr = []

for line in logfile:
	#if line.startswith("Nabor Vblcotbl") or line.startswith("Recursive dot") or line.startswith("preRunway") or line.startswith("Runway") or line.startswith("Glissada"):
	if line.startswith("Runway") or line.startswith("Glissada"):
	#if line.startswith("Runway"):
		rd=line.split(';')
		colvolines +=1
		precc    = [float(rd[3]),float(rd[4]),float(rd[5])]
		maxpitch = max(maxpitch, max(precc[0],precc[1]))
		minpitch = min(minpitch, min(precc[0],precc[0]))
		maxspeed = max(maxspeed, precc[2])
		minspeed = min(minspeed, precc[2])
		parr.append(precc)


maxpitch = maxpitch*1.05
minpitch = minpitch*0.95
maxspeed = maxspeed*1.05
minspeed = minspeed*0.95
width   = 1200		
height  = 900
xstep   = float(width)/colvolines
ytstep  = height/1.1
ypitchstep = height/float(maxpitch-minpitch)
yspeedstep = height/float(maxpitch-minpitch)

old_x=0
canv = Canvas(root, width = width, height = height, bg = "lightgray", cursor = "pencil")
old_ylpitch = height
old_ypitch  = height
old_yspeed  = height
canv.create_line(0, height-((0-minspeed)*yspeedstep), width, height-((0-minspeed)*yspeedstep), width = 1.0, fill = 'red')
canv.create_line(0, height-((-1-minspeed)*yspeedstep), width, height-((-1-minspeed)*yspeedstep), width = 1.0, fill = 'red')
canv.create_line(0, height-((-2-minspeed)*yspeedstep), width, height-((-2-minspeed)*yspeedstep), width = 1.0, fill = 'red')
for i in range(colvolines):
	x=xstep*i
	ypitch  =height-((parr[i][0]-minpitch)*ypitchstep)
	ylpitch =height-((parr[i][1]-minpitch)*ypitchstep)
	yspeed  =height-((parr[i][2]-minspeed)*yspeedstep)
	print parr[i][2],ylpitch, parr[i][1],ypitch, x
	canv.create_line(old_x, old_yspeed, x, yspeed, width = 1.0, fill = 'red')
	canv.create_line(old_x, old_ylpitch, x, ylpitch, width = 1.0, fill = 'black')
	canv.create_line(old_x, old_ypitch,  x, ypitch,  width = 1.0, fill = 'green')
	old_x = x
	old_yspeed = yspeed
	old_ylpitch = ylpitch
	old_ypitch = ypitch


canv.pack()	
root.mainloop()
	

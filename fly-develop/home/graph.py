import math 
from Tkinter import *


root = Tk()

canv = Canvas(root, width = 1000, height = 1500, bg = "lightgray", cursor = "pencil")
canv.create_line(500,1000,500,0,width=2,arrow=LAST) 
canv.create_line(0,500,1000,500,width=2,arrow=LAST) 

masx = 20.0
masy = 120.0
First_x = 1;

for i in range(40):
	k = i+1-10
	canv.create_line(k *(1000/masx) + 500,  -5 + 500, k *(1000/masx)+ 500, 5 + 500, width = 0.5, fill = 'black')
	canv.create_text(k *(1000/masx) + 505, -10 + 500, text = str(k), fill="purple", font=("Helvectica", "10"))
	canv.create_line(-5 + 500, 500-k*(1000/masy), 5 + 500, 500-k*(1000/masy), width = 0.5, fill = 'black')
	canv.create_text(10 + 500, 500-k*(1000/masy), text = str(k), fill="purple", font=("Helvectica", "10"))
	
for i in range(42):
	k = i+1.5-11
	canv.create_line(k *(1000/masx) + 500,  -3 + 500, k *(1000/masx)+ 500, 3 + 500, width = 0.5, fill = 'black')
	canv.create_line(-3 + 500, 500-k*(1000/masy), 3 + 500, 500-k*(1000/masy), width = 0.5, fill = 'black')
	#canv.create_line(k *(1000/masx) + 500,  0, k *(1000/masx)+ 500, 1000, width = 0.1, fill = 'black')
	#canv.create_line(0, 500-k*(1000/masy), 1000, 500-k*(1000/masy), width = 0.1, fill = 'black')	
y2=15.0
old_y2=15.0
maxy2=60.0
count=0
for i in range(1600):	
	x = First_x + (1.0 / (1600/masx)) * i	
	#y1 = math.sin(x+3.14)
	#y2 = math.sin(x)
	acc = (maxy2/(400*old_y2))
	if old_y2>maxy2: 
		acc=0
	y1=acc*(70-old_y2)
	y2=old_y2+y1
	old_y2=y2
	count +=1
	print count,";",y1,";",y2,";",acc
	y1 = 500-y1*(1000/masy)
	y2 = 500-y2*(1000/masy)
	x = x*(1000/masx)+500
	canv.create_oval(x, y1, x + 1, y1 + 1, fill = 'red')
	canv.create_oval(x, y2, x + 1, y2 + 1, fill = 'purple')
	
	
canv.pack()	
root.mainloop()

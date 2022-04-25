#! /usr/bin/python

#./png.py [file]
import sys
from copy import deepcopy
from PIL import Image
import numpy as np

#Initialisation Variables
quickfort = False
height = 12
width = 8
out = "disp.html"
im = Image.open("curses.png")
curses = np.array(im)

carray = [	["&nbsp;","☺","☻","♥","♦","♣","♠","•","◘","○","◙","♂","♀","♪","♫","☼"],
		["►","◄","↕","‼","¶","§","▬","↨","↑","↓","→","←","∟","↔","▲","▼"],
		[" ","!","\"","#","$","%","&","'","(",")","*","+",",","-",".","/"],
		["0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","?"],
		["@","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O"],
		["P","Q","R","S","T","U","V","W","X","Y","Z","[","\\","]","^","_"],
		["`","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o"],
		["p","q","r","s","t","u","v","w","x","y","z","{","|","}","~","⌂"],
		["Ç","ü","é","â","ä","à","å","ç","ê","ë","è","ï","î","ì","Ä","Å"],
		["É","æ","Æ","ô","ö","ò","û","ù","ÿ","Ö","Ü","¢","£","¥","₧","ƒ"],
		["á","í","ó","ú","ñ","Ñ","ª","º","¿","⌐","¬","½","¼","¡","«","»"],
		["░","▒","▓","│","┤","╡","╢","╖","╕","╣","║","╗","╝","╜","╛","┐"],
		["└","┴","┬","├","─","┼","╞","╟","╚","╔","╩","╦","╠","═","╬","╧"],
		["╨","╤","╥","╙","╘","╒","╓","╫","╪","┘","┌","█","▄","▌","▐","▀"],
		["α","ß","Γ","π","Σ","σ","µ","τ","Φ","Θ","Ω","δ","∞","φ","ε","∩"],
		["≡","±","≥","≤","⌠","⌡","÷","≈","°","∙","·","√","ⁿ","²","■"," "]]


#open image
im = Image.open(sys.argv[1])
im = im.convert('RGB')	#convert to RGB from whatever
arr = np.array(im)
arr = arr[:,:,:3]	#remove alpha channel
disp_arr = deepcopy(arr)

#calc x_diffs
diff = [0]*(len(arr)-1)
max_diff = -1
max_diff_i = -1
ydiff = [0]*(len(arr[0]))

for j in range(0,len(arr)-1):
	for i in range(0,len(arr[0])):
		if not(arr[j,i]==arr[j+1,i]).all():
			diff[j] = diff[j] + 1
			ydiff[i] = ydiff[i] + 1
	if diff[j] > max_diff:
		max_diff = diff[j]
		max_diff_i = j

#calc y_diffs
min_ydiff = 999
for i in range(0,len(ydiff)):
	if min_ydiff > ydiff[i]:
		min_ydiff = ydiff[i]

#for each possible offset
for u_offset in range(0,height):
	disp_arr_bak = deepcopy(disp_arr)
	f1=open(out,"w")
#	u_offset = int(sys.argv[2])
	dead = 0
	d_offset = height-u_offset

	#draw horizontal grid
	u_work_i = max_diff_i + u_offset
	d_work_i = max_diff_i - d_offset
	while u_work_i < len(arr):
		for i in range(0,len(arr[0])):
			disp_arr[u_work_i,i] = [255,255,255]
		u_work_i = u_work_i + height
	while d_work_i >= 0:
		for i in range(0,len(arr[0])):
			disp_arr[d_work_i,i] = [255,255,255]
		d_work_i = d_work_i - height
	top_y = d_work_i + height + 1

	#draw vertical grid
	mod = [0]*width
	for i in range(0,len(ydiff)):
		if ydiff[i] == min_ydiff:
			mod[i%width] = mod[i%width] + 1
	max_mod = -1
	max_mod_i = -1
	for i in range(0,width):
		if max_mod <= mod[i]:
			max_mod = mod[i]
			max_mod_i = i

	for i in range(0,len(arr[0])-1):
		if i%width == max_mod_i:
			for j in range(0,len(arr)-1):
				disp_arr[j,i] = [255,255,255]
	top_x = max_mod_i + 1

	#print output
	print("<head><link rel='stylesheet' type='text/css' href='./df.css'></head><body>",file=f1)

	counter = 0
	for j in range(0,int(len(arr)/12)):
		back_bak = [0,0,0]
		fore_bak = [0,0,0]
		for i in range(0,int(len(arr[0])/8)):
			subarr = deepcopy(arr[top_y+j*height:top_y+j*height+height,top_x+i*width:top_x+i*width+width])
			if len(subarr)<1 or len(subarr[0])<1:	#break if tile is incomplete
				break
			back = deepcopy(subarr[0][0]).tolist()	#get background colour (top left pixel)
			fore = [0,0,0]
			
			#reduce subarray to two colours
			for k in range(0,len(subarr)):
				for l in range(0,len(subarr[0])):
					if (subarr[k][l]==back).all():
						subarr[k][l] = [0,0,0]
					else:
						fore = deepcopy(subarr[k][l]).tolist()
						subarr[k][l] = [255,255,255]
			subarr = np.array(Image.fromarray(subarr).convert("1",dither=Image.NONE))
			
			breakpoint = 0
			
			#compare to each curses tile
			for curses_y in range(0,16):
				for curses_x in range(0,16):
					change = 0
					subcurses = curses[curses_y*height:curses_y*height+height,curses_x*width:curses_x*width+width]
					if len(subcurses)!=len(subarr) or len(subcurses[0])!=len(subarr[0]):	#break if partial tiles
						breakpoint = 1
						break;
					if (subcurses==subarr).all() or (subcurses!=subarr).all():	#if match
						if(subcurses!=subarr).all():	#swap foreground and background colour if they are inverted
							fore,back = back,fore

						#html shenanigans
						if (fore==fore_bak or (curses_y==0 and curses_x==0)) and back==back_bak:
							if not(i):
								print("<span>",end="",file=f1)
							pass;
#						elif (fore==fore_bak or (curses_y==0 and curses_x==0)) and back!=back_bak:
#							print("</span><span style='background-color:rgb({},{},{})'>".format(back[0],back[1],back[2]),end="",file=f1)
						elif fore!=fore_bak and back==[0,0,0]:
							print("</span><span style='color:rgb({},{},{})'>".format(fore[0],fore[1],fore[2]),end="",file=f1)
							change = 1
						else:
							print("</span><span style='color:rgb({},{},{});background-color:rgb({},{},{})'>".format(fore[0],fore[1],fore[2],back[0],back[1],back[2]),end="",file=f1)
							change = 1
						print(carray[curses_y][curses_x],end="",file=f1)
						if(quickfort):
							if(back != [0,0,0]):
								glyph = carray[curses_y][curses_x]
								if(glyph == "&nbsp;"):
									print("d,",end="")
								elif(glyph == "<"):
									print("u,",end="")
								elif(glyph == ">"):
									print("j,",end="")
								elif(glyph == "X"):
									print("i,",end="")
								elif(glyph == "_"):
									print("h,",end="")
								elif(glyph == "▲"):
									print("r,",end="")
								else:
									print(" ,",end="")
							else:
								print(" ,",end="")
#						print("</span>",end="",file=f1)
						if curses_y!=0 or curses_x!=0 or change:
							fore_bak = deepcopy(fore)
						back_bak = deepcopy(back)
						breakpoint = 1
						counter = counter + 1
						break
				if breakpoint:
					break
			if not(breakpoint):
				if j!=int(len(arr)/12)-1 and i!=int(len(arr[0])/8)-1:	#file doesn't fail on the last line
					dead = 1
				break;
		if dead:	#errors are present in the file
			f1.close()
			break;
		print("</span><br>",file=f1)
		if(quickfort):
			print("#")
	if not(dead):
		break
	disp_arr = deepcopy(disp_arr_bak)
print("</body>",end="",file=f1)
f1.close()

if dead:	#if no offsets work
	f1=open(out,"w")
	print("ERROR",file=f1)
	
#print(counter)	#print number of tiles
#draw image	
#Image.fromarray(disp_arr).show()

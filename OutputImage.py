#!/usr/bin/python
import Image
import numpy as np
import time
import pickle
import os
import copy
import traceback

# User variables
multiple=20
inputfilename="F:\Documents\simple-gps-points.csv"
outputimage="Whitby.png"
picklefilename="array.pickle3"

# system variables
starttime=time.time()
print time.ctime()
mapwidth,mapheight=360*multiple,180*multiple

#lat is west-east, lon is north-south
# whole of UK
#topleft=[58.879671,-11.711426] #lat,lon
#bottomright=[49.976662,2.2790527] #lat,lon

# London
#topleft=[51.550178 , -0.256462]
#bottomright=[51.42062 , 0.095787]
#scale=10000

# whitby
topleft=[54.493873 , -0.63386]
bottomright=[54.468342 , -0.602446]
#scale=50000

#england
#topleft=[51.750839 , -0.568542]
#bottomright=[49.976662,2.2790527]

#NZ
#topleft=[-33,165]
#bottomright=[-47,178]
#scale=500

#silverstone
#topleft=[52.082302 , -1.032414]
#bottomright=[52.060829 , -1.002717]

#nurburgring
#topleft=[50.377656 , 6.91186]
#bottomright=[50.325738 , 7.001982]

#Europe
#topleft=[58.904646 , -15.908203]
#bottomright=[ 35.960223 , 43.198242 ]

#USA
#topleft=[49.15297 , -129.990234]
#bottomright=[21.616579 , -61.259766]

largestside=6000

black=0xff000000
gold=0xff00d7ff
halfgold=0xff00758b
blue=0xffffdb00
halfblue=0xffcd9a00
green=0xff00ff7f
halfgreen=0xff008b45
red=0xff9314ff
halfred=0xff500a8b

colourdict={90:gold,
80:blue,
70:green,
60:red,
9:halfgold,
8:halfblue,
7:halfgreen,
6:halfred,
0:black}

def getcolour(val,maxvalue):
	# work out val as a percent of max
	valpercent=100 * float(val)/float(maxvalue)
	#if val !=1: print val,maxvalue,valpercent
	colour=60

	colour=0
	halfcolour=0
	if valpercent > 0.0125: 
		colour=60
		halfcolour=6
	if valpercent > 0.025: 
		colour=70
		halfcolour=7
	if valpercent > 0.25: 
		colour=80
		halfcolour=8
	if valpercent > 0.5: 
		colour=90
		halfcolour=9
	return colour,halfcolour


def loaddata(inputfilename):
	# lat = col 0, lon= col 1
	# max and min lat and long=
	# lat= -90, +90
	# lon= -180, +180
	# so to zero them we need to add 90 to lat and 180 to long
	
	# example of data in csv: -466611080,1690980270
	
	# these numbers can be converted into gps values, by dividing by 10000000
	#  we need to make these values all positive, by adding 900000000 to lat and 1800000000 to lon
	
	global topleft,bottomright,scale
	
	#scale2=scale*1.5
	
	
	topleft=[topleft[0]+90,topleft[1]+180]
	bottomright=[bottomright[0]+90,bottomright[1]+180]	
	
	# work out the scale - make the largest side of the map 3000 pixels
	width=float(bottomright[1]-topleft[1])
	height=float(topleft[0]-bottomright[0])
	scale=largestside/max([width,height])
	print width,height,scale
	print width,height,scale
	
	
	#quit()
	
	scale2=scale
	#modtopleft=[(topleft[0]*scale)+(90*scale),(topleft[1]*scale)+(180*scale)]
	#modbottomright=[(bottomright[0]*scale)+(90*scale),(bottomright[1]*scale)+(180*scale)]
	modtopleft=[topleft[0]*scale2,topleft[1]*scale]
	modbottomright=[bottomright[0]*scale2,bottomright[1]*scale]
	
	# now find the width and height of the map, by taking the topleft[0] from bottomright[0] and bottomright[1] from topleft[1]
	mapwidth=int(modbottomright[1]-modtopleft[1])+2
	mapheight=int(modtopleft[0]-modbottomright[0])+2
	
	print modtopleft,modbottomright,mapwidth,mapheight

	maparray=np.empty( (mapwidth,mapheight),np.uint32)
	maparray.shape=mapheight,mapwidth

	count=0
	count2=0
	inputfile=open(inputfilename)
	for line in inputfile:
		count=count+1
		count2=count2+1
		#if count2==500000: break
		line=line.strip()
		if line=="": continue
		if count==500: 
			count=0
			#continue

		#count=0
		line=line.split(',')
		#print line
		try:
			lat=(float(line[0].strip())/10000000)+90
			lon=(float(line[1].strip())/10000000)+180
		except:
			continue

		#discard any data points that don't fit into our topleft, bottom right geofence
		#print lat,topleft[0]
		
		if lat > topleft[0]: continue
		if lat < bottomright[0]: continue
		if lon < topleft[1]: continue
		if lon > bottomright[1]: continue
		#print lat,lon,modtopleft,modbottomright
		
		lat2=(lat*scale2)-modbottomright[0]
		lon2=(lon*scale)-modtopleft[1]
	
		#print "modded:",lat2,lon2
		#print line
		#quit()
		try:
			maparray[lat2,lon2]=maparray[lat2,lon2]+1
		except:
			print count2,line
			print lat,lon
			print lat2,lon2
			print modtopleft
			print modbottomright
			print mapheight,mapwidth
			#break
			#quit(1)


	inputfile.close()
	return maparray,mapwidth,mapheight
	
#load the data every time..
maparray,mapwidth,mapheight=loaddata(inputfilename)


# Make the map pretty
newarray=copy.deepcopy(maparray)
maxvalue=newarray.max()	

count=0	
rowcount=0

print "emprettify"
for row in maparray:
	colcount=0
	for pixel in row:
		if pixel !=0: 
			colourvalue,halfcolourvalue=getcolour(pixel,maxvalue)
			#if colourvalue >=8: print pixel,colourvalue,rowcount,colcount
			#print newarray[rowcount][colcount]

			# place the half colours
			colour=colourdict[colourvalue]
			halfcolour=colourdict[halfcolourvalue]
			newarray[rowcount][colcount]=colour
	
			if colourvalue > 75:
				try:
					if rowcount !=0: 
						if newarray[rowcount-1][colcount]==colourdict[0]:
							newarray[rowcount-1][colcount]=halfcolour
					if rowcount !=(mapheight-1): 
						if newarray[rowcount+1][colcount]!=colourdict[0]:
							newarray[rowcount+1][colcount]=halfcolour
					if colcount !=0:
						if newarray[rowcount][colcount+1]!=colourdict[0]:
							newarray[rowcount][colcount+1]=halfcolour
					if colcount !=(mapwidth-1): 
						if newarray[rowcount][colcount-1]==colourdict[0]:
							newarray[rowcount][colcount-1]=halfcolour
				except:
					print traceback.print_exc()
					print colcount,rowcount
					pass

		else:
			if newarray[rowcount][colcount]==0: newarray[rowcount][colcount]=colourdict[0]
		colcount+=1	
	rowcount+=1
print time.ctime(),
print "creating image"

#imageMap=Image.new("RGB", (mapwidth,mapheight), (0,0,0) )
imageMap=Image.frombuffer('RGBA', (mapwidth,mapheight),newarray,'raw','RGBA',0,1).transpose(Image.FLIP_TOP_BOTTOM)

imageMap.save(outputimage)
image2=imageMap.resize((mapwidth/2,mapheight/2),Image.ANTIALIAS)
quality_val=100
image2.save("map7-1.png", 'PNG', quality=quality_val)
#imageMap.show()


endtime=time.time()
print time.ctime()
print  "Elapsed time:%s",endtime-starttime



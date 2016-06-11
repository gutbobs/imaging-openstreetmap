#!/usr/bin/python
import Image
import time
import copy
import traceback

from modules import ColourRules
from modules import LoadData

__author__ = 'gutbobs'

def main():
	# User variables
	multiple = 20
	inputfilename = "F:\Documents\simple-gps-points.csv"
	outputimage = "Whitby.png"
	picklefilename = "array.pickle3"

	# system variables
	starttime = time.time()
	print time.ctime()
	mapwidth, mapheight = 360 * multiple, 180 * multiple


	# whitby
	topleft = [54.493873, -0.63386]
	bottomright = [54.468342, -0.602446]
	# scale=50000
	largestside = 6000

	# load the data every time..
	#maparray, mapwidth, mapheight = LoadData.loaddata(inputfilename, topleft, bottomright)
	mapdata=LoadData.LoadData()
	mapdata.inputfilename=inputfilename
	mapdata.topleft=topleft
	mapdata.bottomright=bottomright
	mapdata.largestside=largestside
	mapdata.go()
	maparray=mapdata.maparray
	mapwidth=mapdata.mapwidth
	mapheight=mapdata.mapheight


	# Make the map pretty
	newarray = copy.deepcopy(maparray)
	maxvalue = newarray.max()

	count = 0
	rowcount = 0

	GetColourdict = ColourRules.getcolour()
	GetColourdict.init()
	colourdict = GetColourdict.colourdict

	print "emprettify"
	for row in maparray:
		colcount = 0
		for pixel in row:
			if pixel != 0:
				colourvalue, halfcolourvalue = ColourRules.getcolour(pixel, maxvalue)

				# place the half colours
				colour = colourdict[colourvalue]
				halfcolour = colourdict[halfcolourvalue]
				newarray[rowcount][colcount] = colour

				if colourvalue > 75:
					try:
						if rowcount != 0:
							if newarray[rowcount - 1][colcount] == colourdict[0]:
								newarray[rowcount - 1][colcount] = halfcolour
						if rowcount != (mapheight - 1):
							if newarray[rowcount + 1][colcount] != colourdict[0]:
								newarray[rowcount + 1][colcount] = halfcolour
						if colcount != 0:
							if newarray[rowcount][colcount + 1] != colourdict[0]:
								newarray[rowcount][colcount + 1] = halfcolour
						if colcount != (mapwidth - 1):
							if newarray[rowcount][colcount - 1] == colourdict[0]:
								newarray[rowcount][colcount - 1] = halfcolour
					except:
						print traceback.print_exc()
						print colcount, rowcount
						pass

			else:
				if newarray[rowcount][colcount] == 0: newarray[rowcount][colcount] = colourdict[0]
			colcount += 1
		rowcount += 1
	print time.ctime(),
	print "creating image"

	# imageMap=Image.new("RGB", (mapwidth,mapheight), (0,0,0) )
	imageMap = Image.frombuffer('RGBA', (mapwidth, mapheight), newarray, 'raw', 'RGBA', 0, 1).transpose(
		Image.FLIP_TOP_BOTTOM)

	imageMap.save(outputimage)
	image2 = imageMap.resize((mapwidth / 2, mapheight / 2), Image.ANTIALIAS)
	quality_val = 100
	image2.save("map7-1.png", 'PNG', quality=quality_val)
	# imageMap.show()


	endtime = time.time()
	print time.ctime()
	print  "Elapsed time:%s", endtime - starttime


if __name__ == "__main__":
	main()

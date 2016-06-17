import sys
import numpy as np
import pandas
import sqlite3
import os

__author__ = 'gutbobs'

class LoadData:
    def __init__(self):
        self.inputfilename = ""
        self.topleft = [0, 0]
        self.bottomright = [0, 0]
        self.largestside = 6000
        self.mapwidth = 0
        self.mapheight = 0
        self.dbname = "database.db"
        self.latmultiplier = 90 * 10000000
        self.lonmultiplier = 180 * 10000000

    def getsize(self):
        topleft = [self.topleft[0] + 90, self.topleft[1] + 180]
        bottomright = [self.bottomright[0] + 90, self.bottomright[1] + 180]

        # work out the scale - make the largest side of the map 'largestside' pixels
        width = float(bottomright[1] - topleft[1])
        height = float(topleft[0] - bottomright[0])
        self.scale = self.largestside / max([width, height])
        print width, height, self.scale
        self.scale2 = self.scale

        self.modtopleft = [topleft[0] * self.scale2, topleft[1] *self. scale]
        self.modbottomright = [bottomright[0] * self.scale2, bottomright[1] * self.scale]

        # now find the width and height of the map,
        # by taking the topleft[0] from bottomright[0] and bottomright[1] from topleft[1]
        self.mapwidth = int(self.modbottomright[1] - self.modtopleft[1]) + 2
        self.mapheight = int(self.modtopleft[0] - self.modbottomright[0]) + 2

        print "modtopleft:\t%s\nmodbottomright:\t%s\nmapwidth:\t%s\nmapheight:\t%s\n" %(self.modtopleft, self.modbottomright, self.mapwidth, self.mapheight)

        self.maparray = np.empty((self.mapwidth, self.mapheight), np.uint32)
        self.maparray.shape = self.mapheight, self.mapwidth

    def DatabaseCheck(self):
        # lat = col 0, lon= col 1
        # max and min lat and long=
        # lat= -90, +90
        # lon= -180, +180
        # so to zero them we need to add 90 to lat and 180 to long

        # example of data in csv: -466611080,1690980270

        # these numbers can be converted into gps values, by dividing by 10000000
        #  we need to make these values all positive, by adding 900000000 to lat and 1800000000 to lon
        # self.getsize()

        if not os.path.exists(self.dbname):
            conn = sqlite3.connect(self.dbname)
            sqlquery = "CREATE TABLE GPS (LAT INT, LON INT);"
            print sqlquery
            conn.execute(sqlquery)


            count = 0
            count2 = 0
            readrows = 1000000
            # inputfile = open(self.inputfilename)
            print "opening:", self.inputfilename
            for chunk in pandas.read_csv(self.inputfilename, sep=',', chunksize=readrows, header=1):
                # print chunk
                for row in chunk.values:
                    count += 1
                    count2 += 1
                    # print "row:'%s'" % row
                    # print float(row[0])
                    try:
                        lat = row[0]+self.latmultiplier
                        lon = row[1]+self.lonmultiplier
                        # print "lat:%s\tlon:%s" % (lat,lon)
                    except:
                        print row
                        continue

                    sqlquery = "INSERT INTO GPS (LAT,LON) VALUES (%s,%s);" % (lat, lon)
                    conn.execute(sqlquery)


                    if count % 10000 == 0: print ".",
                    if count % 400000 == 0: print "{:,}".format(count)
                conn.commit()
			
                if count == 100000000: break
            conn.close()



    # discard any data points that don't fit into our topleft, bottom right geofence
    """
        if lat > self.topleft[0]: continue
        if lat < self.bottomright[0]: continue
        if lon < self.topleft[1]: continue
        if lon > self.bottomright[1]: continue
        # print lat,lon,modtopleft,modbottomright

        lat2 = (lat * scale2) - self.modbottomright[0]
        lon2 = (lon * scale) - self.modtopleft[1]

        try:
            self.maparray[lat2, lon2] = self.maparray[lat2, lon2] + 1
        except:
            print count2, line
            print lat, lon
            print lat2, lon2
            print modtopleft
            print modbottomright
            print self.mapheight, self.mapwidth
            # break
            # quit(1)
        """
    print "Finished loading data"
	
    def MakeArray(self):
        self.topleftx=(self.topleft[0]+90)*10000000
        self.toplefty=(self.topleft[1]+180)*10000000
        self.bottomrightx=(self.bottomright[0]+90)*10000000
        self.bottomrighty=(self.bottomright[1]+180)*10000000

        #print self.topleftx
        #print self.toplefty
        #print self.bottomrightx
        #print self.bottomrighty

        self.getsize()
        #sqlquery="select lat,lon from gps where (lat < 570000000.0 and lon > 3450000000.0) and (lat > 430000000.0 and lon < 3580000000.0);"

        sqlquery="SELECT LAT,LON from GPS WHERE (LAT <= %s and LON >= %s) and (LAT >= %s and LON <= %s);" %(self.topleftx,self.toplefty,self.bottomrightx,self.bottomrighty)
        print sqlquery
        conn=sqlite3.connect(self.dbname)
        gpsdata=conn.execute(sqlquery)

        rowcount=0
        for row in gpsdata:
            lat=row[0]/10000000
            lon=row[1]/10000000

            lat2 = (lat * self.scale2) - self.modbottomright[0]
            lon2 = (lon * self.scale) - self.modtopleft[1]

            #print lat2,lon2
            if rowcount % 10000 == 0: 
                print ".",
                sys.stdout.flush()
            if rowcount % 400000 == 0 : 
                print rowcount
                sys.stdout.flush()
            rowcount+=1
            try:
                self.maparray[lat2, lon2] = self.maparray[lat2, lon2] + 1
            except:
                print rowcount, row
                print lat, lon
                print lat2, lon2
                print modtopleft
                print modbottomright
                print self.mapheight, self.mapwidth
                #print lat,lon

        print "Map array complete"



		
		

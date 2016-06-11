import numpy as np

__author__ = 'rich_000'


class LoadData:
    def __init__(self):
        self.inputfilename = ""
        self.topleft = [0, 0]
        self.bottomright = [0, 0]
        self.largestside = 6000
        self.mapwidth = 0
        self.mapheight = 0

    def go(self):
        # lat = col 0, lon= col 1
        # max and min lat and long=
        # lat= -90, +90
        # lon= -180, +180
        # so to zero them we need to add 90 to lat and 180 to long

        # example of data in csv: -466611080,1690980270

        # these numbers can be converted into gps values, by dividing by 10000000
        #  we need to make these values all positive, by adding 900000000 to lat and 1800000000 to lon

        topleft = [self.topleft[0] + 90, self.topleft[1] + 180]
        bottomright = [self.bottomright[0] + 90, self.bottomright[1] + 180]

        # work out the scale - make the largest side of the map 3000 pixels
        width = float(bottomright[1] - topleft[1])
        height = float(topleft[0] - bottomright[0])
        scale = self.largestside / max([width, height])
        print(width, height, scale)
        print(width, height, scale)

        scale2 = scale

        modtopleft = [topleft[0] * scale2, topleft[1] * scale]
        modbottomright = [bottomright[0] * scale2, bottomright[1] * scale]

        # now find the width and height of the map,
        # by taking the topleft[0] from bottomright[0] and bottomright[1] from topleft[1]
        self.mapwidth = int(modbottomright[1] - modtopleft[1]) + 2
        self.mapheight = int(modtopleft[0] - modbottomright[0]) + 2

        print modtopleft, modbottomright, self.mapwidth, self.mapheight

        self.maparray = np.empty((self.mapwidth, self.mapheight), np.uint32)
        self.maparray.shape = self.mapheight, self.mapwidth

        count = 0
        count2 = 0
        inputfile = open(self.inputfilename)
        for line in inputfile:
            count += 1
            count2 += 1
            # if count2==500000: break
            line = line.strip()
            if line == "": continue
            if count == 500:
                count = 0
            # continue

            # count=0
            line = line.split(',')
            try:
                lat = (float(line[0].strip()) / 10000000) + 90
                lon = (float(line[1].strip()) / 10000000) + 180
            except:
                continue

            # discard any data points that don't fit into our topleft, bottom right geofence
            if lat > topleft[0]: continue
            if lat < bottomright[0]: continue
            if lon < topleft[1]: continue
            if lon > bottomright[1]: continue
            # print lat,lon,modtopleft,modbottomright

            lat2 = (lat * scale2) - modbottomright[0]
            lon2 = (lon * scale) - modtopleft[1]

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

        inputfile.close()

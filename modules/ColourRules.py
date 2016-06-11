__author__ = 'gutbobs'

class getcolour:
    def init(self):
        self.black=0xff000000
        self.gold=0xff00d7ff
        self.halfgold=0xff00758b
        self.blue=0xffffdb00
        self.halfblue=0xffcd9a00
        self.green=0xff00ff7f
        self.halfgreen=0xff008b45
        self.red=0xff9314ff
        self.halfred=0xff500a8b

        self.colourdict={90:self.gold,
            80:self.blue,
            70:self.green,
            60:self.red,
            9:self.halfgold,
            8:self.halfblue,
            7:self.halfgreen,
            6:self.halfred,
            0:self.black}

def ReturnColour(self,val,maxvalue):
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
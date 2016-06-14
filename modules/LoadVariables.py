import os

__author__ = 'gutbobs'

def converttolist(conversionstring):
    data=conversionstring.split(',')
    returnlist=[]
    for item in data:
        returnlist.append(float(item))
    return returnlist

class OpenFile:
    def __init__(self):
        self.filename=""
        self.inputfilename=""
        self.outputfilename=""
        self.topleft=[0,0]
        self.bottomright=[0,0]
        self.ErrorCode=0
        self.largestside=1000

    def ReadFile(self):
        if not os.path.exists(self.filename): self.ErrorCode=1
        print "Opening:",self.filename

        if self.ErrorCode==0:
            variablesdict={}
            inputfile=open(self.filename,'r')
            for line in inputfile:
                data=line.strip().split('=')
                variable=data[0]
                value=data[1:]
                variablesdict[variable]=value

            self.inputfilename="".join(variablesdict['inputfilename'])
            self.outputfilename="".join(variablesdict['outputfilename'])
            self.topleft=converttolist("".join(variablesdict['topleft']))
            self.bottomright=converttolist("".join(variablesdict['bottomright']))
            self.largestside=int("".join(variablesdict['largestside']))

            if not os.path.exists(self.inputfilename): self.ErrorCode=2





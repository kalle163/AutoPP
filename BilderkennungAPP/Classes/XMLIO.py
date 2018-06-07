import shutil
import os

class XMLWriter(object):

    listofquader = list()
    listofballs  = list()
    listofblobquader  =list()

    def __init__(self, *args, **kwargs):
        return super(XMLWriter, self).__init__(*args, **kwargs)

    def AddNewQuader(self,xpos,ypos,zpos,xlen,ylen,zlen,angle):
        quader = Quader(xpos,ypos,zpos,xlen,ylen,zlen,angle)
        self.listofquader.append(quader)
        return

    def AddNewBall(self,xpos,ypos,zpos,rad):
        ball= Ball(xpos,ypos,zpos,rad)
        self.listofballs.append(ball)
        return
    def AddNewBlobQuader(self,xpos,ypos,zpos,beta):
        quader= BlobQuader(xpos,ypos,zpos,beta)
        self.listofblobquader.append(quader)
        return


    def deleteList(quader=True,balls=True):
        if quader:
            del listofquader[:]
        if balls:
            del listofballs[:]
        return
    def WriteToXML(self,pfad):
        if len(self.listofquader) >0 or len(self.listofballs) >0:
            file= open(pfad,'w')
            if len(self.listofquader) >0:
                file.write("<Barriers>\n")
                k=1
                for i in self.listofquader:
                    file.write("\t<Quader Nr=%s >\n" % (str(k)))
                    file.write("\t\t<Position x=%s y=%s z=%s/>\n" % (str(i.xpos),str(i.ypos),str(i.zpos)))
                    file.write("\t\t<Length x=%s y=%s z=%s/>\n" % (str(i.xlen),str(i.ylen),str(i.zlen)))
                    file.write("\t\t<Angle Value=%s/>\n" % (str(i.angle)))
                    file.write("\t</Quader>\n")
                    k+=1
                file.write("</Barriers>\n\n")
            if len(self.listofballs)  >0:
                file.write("<Blob_Objects>\n")
                k=1
                for i in self.listofballs:
                    file.write("\t<Ball Nr=%s >\n" % (k))
                    file.write("\t\t<Position x=%s y=%s z=%s/>\n" % (str(i.xpos),str(i.ypos),str(i.zpos))) 
                    file.write("\t\t<Radius Value=%s/>\n" % (str(i.Radius)))
                    file.write("\t</Ball>\n")
                    k+=1
                k=1
                for i in self.listofblobquader:
                    file.write("\t<Quader Nr=%s >\n" % (k))
                    file.write("\t\t<Position x=%s y=%s z=%s/>\n" % (str(i.xpos),str(i.ypos),str(i.zpos))) 
                    file.write("\t\t<Angle Value=%s/>\n" % (str(i.Winkel)))
                    file.write("\t</Quader>\n")
                    k+=1
                file.write("</Blob_Objects>\n\n")
            file.close()
            return

class XMLReader(object):
    listofblobobjects=list()
    listofproperties=["rgb","hsv","grey","circularity","area","convexity","inertiaratio"]
    def __init__(self, *args, **kwargs):
        return super(XMLReader, self).__init__(*args, **kwargs)

    def readinputfile(self,pfad):
        objectactive=False
        if not os.path.exists(pfad):
            print("Input.xml not found")
            return
        with open(pfad,'r') as file:
            for line in file:
                if line.find("#")<0 and line.find("<")>=0 and line.find(">")>=0:
                    if objectactive and (line=="</BlobObject>\n" or line=="</BlobObject>"):
                        objectactive=False
                        blobobject.SaveValues()
                        self.listofblobobjects.append(blobobject)
                    elif objectactive and not line=="</BlobObject>\n" and not line=="</BlobObject>":
                        line=line.replace(">","")
                        line=line.replace("<","")
                        line=line.replace("/","")
                        splits=line.split()
                        if splits[0] in self.listofproperties:
                            for i in range(1,len(splits)):
                                subsplit=splits[i].split("=")
                                ret=blobobject.SetProperty(subsplit[0]+splits[0],subsplit[1])
                                if not ret:
                                    print("No "+subsplit[0]+splits[0]+" defined for BlobObjects")
                                    break
                        else:
                            print("No "+splits[0]+" Property defined for BlobObjects. Property musst be "+str(self.listofproperties))
                            break
                    elif not objectactive and line.find("/")<0:
                        line=line.replace(">","")
                        line=line.replace("<","")
                        splits=line.split()
                        if splits[0] == "BlobObject":
                            name="object"
                            if len(splits)>1:
                                splits=splits[1].split("=")
                                if splits[0]=="name":
                                    name=splits[1]
                                else:
                                    print("The Property "+ splits[0]+" is not defined for BlobObjects it has to be name")
                                    break
                            blobobject= BlobObject(name) 
                            objectactive=True

                        else:
                            print("No Object defined. You have to define a BlobObject ")
                            break   
  
        return

    def getlistofblobobjects(self):
        return self.listofblobobjects
        

class BlobObject(object):
    name = "object"
    __Properties = {
    "minrgb":(0,0,0),
    "maxrgb":(255,255,255),
    "minhsv":(0,0,0),
    "maxhsv":(255,255,255),
    "mingrey":0,
    "maxgrey":255,
    "mincircularity":0,
    "maxcircularity":1,
    "maxarea":-1,
    "minarea":0,
    "minconvexity":0,
    "maxconvexity":1,
    "mininertiaratio":0,
    "maxinertiaratio":1,
        }
   
    def __init__(self,name):
        self.name=name
        return
    def errormessage(self,property,value):
        print(value+" is out of range for "+property)
        return
    def SetProperty(self,property,value):
        listofintprobs=["mingrey","maxgrey","minarea","maxarea"]
        listofvecprobs=["minrgb","maxrgb","minhsv","maxhsv"]
        if property in self.__Properties: 
            if property in listofintprobs:
                valueint=int(value)
                if (property == "maxgrey" and valueint <=255 and valueint > 0) or (property  == "mingrey" and valueint >=0 and valueint <255) or (property.find("area")>0 and valueint >=0):
                    self.__Properties[property]=valueint
                else: 
                    self.errormessage(property,value)
                    return False
            elif property in listofvecprobs:
                splits=value.split(",")
                valuevec=(int(splits[0]),int(splits[1]),int(splits[2]))
                if valuevec[0] <=255 and valuevec[0] >=0 and valuevec[1] <=255 and valuevec[1] >=0 and valuevec[2] <=255 and valuevec[2] >=0:
                    self.__Properties[property]=valuevec
                else:
                    self.errormessage(property,value)
                    return False
            else:
                valuefloat=float(value)
                if valuefloat >= 0.0 and valuefloat <=1.0: 
                    self.__Properties[property]=valuefloat
                else:
                    self.errormessage(property,value)
                    return False
            return True
        else:
            return False

    def SaveValues(self):
        self.minrgb= self.__Properties["minrgb"]
        self.maxrgb= self.__Properties["maxrgb"]
        self.minhsv= self.__Properties["minhsv"]
        self.maxhsv= self.__Properties["maxhsv"]
        self.mingrey= self.__Properties["mingrey"]
        self.maxgrey= self.__Properties["maxgrey"]
        self.mincircularity= self.__Properties["mincircularity"]
        self.maxcircularity= self.__Properties["maxcircularity"]
        self.maxarea= self.__Properties["maxarea"]
        self.minarea= self.__Properties["minarea"]
        self.minconvexity= self.__Properties["minconvexity"]
        self.maxconvexity= self.__Properties["maxconvexity"]
        self.mininertiaratio= self.__Properties["mininertiaratio"]
        self.maxinertiaratio= self.__Properties["maxinertiaratio"]
        
    

class Quader(object):
    
    def __init__(self,xpos,ypos,zpos,xlen,ylen,zlen,angle):
        self.xpos=xpos
        self.ypos=ypos
        self.zpos=zpos
        self.xlen=xlen
        self.ylen=ylen
        self.zlen=zlen
        self.angle=angle
        return

class Ball(object):

    def __init__(self,xpos,ypos,zpos,rad):
        self.xpos=xpos
        self.ypos=ypos
        self.zpos=zpos
        self.Radius =rad
        return

class BlobQuader(object):

    def __init__(self,xpos,ypos,zpos,beta):
        self.xpos=xpos
        self.ypos=ypos
        self.zpos=zpos
        self.Winkel =beta
        return
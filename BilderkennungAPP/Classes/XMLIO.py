
class XMLWriter(object):

    listofquader = list()
    listofballs  = list()

    def __init__(self, *args, **kwargs):
        return super(XMLWriter, self).__init__(*args, **kwargs)

    def AddNewQuader(self,xpos,ypos,zpos,xlen,ylen,zlen):
        quader = Quader(xpos,ypos,zpos,xlen,ylen,zlen)
        self.listofquader.append(quader)
        return

    def AddNewBall(self,xpos,ypos,zpos,rad):
        ball= Ball(xpos,ypos,zpos,rad)
        self.listofballs.append(ball)
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
                for i in self.listofquader:
                    file.write("\t<Quader Nr=%s >\n",(i))
                    file.write("\t\t<Position x=%s y=%s z=%s/>\n",(i.Position["x"].tostring(),i.Position["y"].tostring(),i.Position["z"].tostring()))
                    file.write("\t\t<Length x=%s y=%s z=%s/>\n",(i.Length["x"].tostring(),i.Length["y"].tostring(),i.Lentgh["z"].tostring()))
                    file.write("\t</Quader>\n")
                file.write("</Barriers>\n\n")
            if len(self.listofballs)  >0:
                file.write("<Blob_Objects>\n")
                for i in self.listofballs:
                    file.write("\t<Ball Nr=%s >\n",(i))
                    file.write("\t\t<Position x=%s y=%s z=%s/>\n",(i.Position["x"].tostring(),i.Position["y"].tostring(),i.Position["z"].tostring())) 
                    file.write("\t\t<Radius Value=%s />\n",(i.Radius.tostring()))
                    file.write("\t</Ball>\n")
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
        with open(pfad,'r') as file:
            for line in file:
                if line.find("#")<0 and line.find("<")>=0 and line.find(">")>=0:
                    if objectactive and (line=="</BlobObject>\n" or line=="</BlobObject>"):
                        objectactive=False
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
    Properties = {
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
    "maxinertiaration":1,
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
        if property in self.Properties: 
            if property in listofintprobs:
                valueint=int(value)
                if (property is "maxgrey" and valueint <=255 and valueint > 0) or (property is "mingrey" and valueint <=0 and valueint <255) or (property.find("area")>0 and valueint >=0):
                    self.Properties[property]=valueint
                else: 
                    self.errormessage(property,value)
                    return False
            elif property in listofvecprobs:
                splits=value.split(",")
                valuevec=(int(splits[0]),int(splits[1]),int(splits[2]))
                if valuevec[0] <=255 and valuevec[0] >=0 and valuevec[1] <=255 and valuevec[1] >=0 and valuevec[2] <=255 and valuevec[2] >=0:
                    self.Properties[property]=valuevec
                else:
                    self.errormessage(property,value)
                    return False
            else:
                valuefloat=float(value)
                if valuefloat >= 0.0 and valuefloat <=1.0: 
                    self.Properties[property]=valuefloat
                else:
                    self.errormessage(property,value)
                    return False
            return True
        else:
            return False
       
    def GetProperty(self,property):
        return self.Properties[property]
    

class Quader(object):
    
    Position ={
    "x":0,
    "y":0,
    "z":0,
    }
    Length ={
    "x":0,
    "y":0,
    "z":0,       
    }

    def __init__(self,xpos,ypos,zpos,xlen,ylen,zlen):
        self.Position["x"]=xpos
        self.Position["y"]=ypos
        self.Position["z"]=zpos
        self.Length["x"]=xlen
        self.Length["y"]=ylen
        self.Length["z"]=zlen
        return

class Ball(object):
    Position ={
    "x":0,
    "y":0,
    "z":0,
    }
    Radius = 0

    def __init__(self,xpos,ypos,zpos,rad):
        self.Position["x"]=xpos
        self.Position["y"]=ypos
        self.Position["z"]=zpos
        self.Radius =rad
        return



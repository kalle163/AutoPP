


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
                    file.write("\t<Quader Nr:%s >\n",(i))
                    file.write("\t\t<Position>\n")
                    file.write("\t\t\t<x %s />\n",(i.Position["x"].tostring()))
                    file.write("\t\t\t<y %s />\n",(i.Position["y"].tostring()))
                    file.write("\t\t\t<z %s />\n",(i.Position["z"].tostring()))
                    file.write("\t\t</Position>\n")
                    file.write("\t\t<Length>\n")
                    file.write("\t\t\t<x %s />\n",(i.Length["x"].tostring()))
                    file.write("\t\t\t<y %s />\n",(i.Length["y"].tostring()))
                    file.write("\t\t\t<z %s />\n",(i.Length["z"].tostring()))
                    file.write("\t\t</Length>\n")
                    file.write("\t</Quader>\n")
                file.write("</Barriers>\n\n")
            if len(self.listofballs)  >0:
                file.write("<Moveable_Objects>\n")
                for i in self.listofballs:
                    file.write("\t<Ball Nr:%s >\n",(i))
                    file.write("\t\t<Position>\n")
                    file.write("\t\t\t<x %s />\n",(i.Position["x"].tostring()))
                    file.write("\t\t\t<y %s />\n",(i.Position["y"].tostring()))
                    file.write("\t\t\t<z %s />\n",(i.Position["z"].tostring()))
                    file.write("\t\t</Position>\n")
                    file.write("\t\t<Radius %s />\n",(i.Radius.tostring()))
                    file.write("\t</Ball>\n")
                file.write("</Moveable_Objects>\n\n")
            file.close()
            return

class XMLReader(object):
    
    def __init__(self, *args, **kwargs):
        return super(XMLReader, self).__init__(*args, **kwargs)

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



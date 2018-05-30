import numpy as np 
import cv2
from Classes.XMLIO import *
import shelve
import Kinect.const as const
import math 

class Simple2DImageto3DCoords(object):

    def __init__(self):
        return super(Simple2DImageto3DCoords, self).__init__()

    def load(self):
        caliresult = shelve.open(const.rootfolder+"\CalibrationResults")
        self.distancetoground= np.load(const.rootfolder+"/distancetoground.npy")
        self.lenperpix = caliresult['lenperpix']
        self.pointzero = caliresult['pointzero']
        caliresult.close()

    def __Calculate3DPoint__(self,x,y):
        Point = np.zeros(2,1)
        Point[0] = (x-self.pointzero[0])*self.lenperpix[0]
        Point[1] = (y-self.pointzero[1])*self.lenperpix[1]
        return Point

    def ConvertPixQuadertoCoordQuader(self,listofquaders,XMLWriter):
        if not listofquaders:
            return
        for quader in listofquaders:
            x1= quader.x
            y1= quader.y
            z= quader.height
            print (str(x1-(const.ir_image_size[0]/2))+"   "+str(y1-(const.ir_image_size[1]/2))+"    "+str(z))
            x2 =quader.x+quader.widthx
            y2 =quader.y+quader.widthy
            if not z==0:
                Point1=self.__Calculate3DPoint__(x1,y1,z)
                Point2=self.__Calculate3DPoint__(x2,y2,z)
                XMLWriter.AddNewQuader(Point1[0],Point1[1],0,abs(Point1[0]-Point2[0]),abs(Point1[1]-Point2[1]),Point1[2])
        return

    def ConvertBalltoCoords(self,listofballs,XMLWriter,depthframe):
        if not listofballs:
            return
        for keypoint in listofballs:
            x = int(keypoint.pt[0])
            y = int(keypoint.pt[1])
            #z = depthframe[x,y]
            s = keypoint.size
            r = math.sqrt(s/math.pi)
            rad=r*self.lenperpix[0]
            Point = self.__Calculate3DPoint__(x,y)
            XMLWriter.AddNewBall(Point[0],Point[1],rad,rad)
        return

    def ConvertQuadertoCoords(self,listofballs,XMLWriter,depthframe):
        if not listofballs:
            return
        for keypoint in listofballs:
            x = int(keypoint.pt[0])
            y = int(keypoint.pt[1])
            #z = depthframe[x,y]
            Point = self.__Calculate3DPoint__(x,y)
            XMLWriter.AddNewBall(Point[0],Point[1],Point[2],rad)
        return


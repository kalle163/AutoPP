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
        self.lenperpix = caliresult['lenperpix']
        self.pointzero = caliresult['pointzero']
        caliresult.close()
        caliresult = shelve.open(const.rootfolder+"\IRCalibrationResults")
        self.distancetoground= caliresult['depth']
        self.irlenperpix = caliresult['lenperpix']
        self.irpointzero = caliresult['pointzero']
        caliresult.close()

    def __Calculate3DPoint__(self,x,y):
        Point = np.zeros((2,1),dtype=float)
        Point[0] = (x-self.pointzero[0])*self.lenperpix[0]
        Point[1] = (y-self.pointzero[1])*self.lenperpix[1]
        return Point
    def __Calculate3DPointIR__(self,x,y):
        Point = np.zeros((2,1),dtype=float)
        Point[0] = (x-self.irpointzero[0])*self.irlenperpix[0]
        Point[1] = (y-self.irpointzero[1])*self.irlenperpix[1]
        return Point


    def ConvertPixQuadertoCoordQuader(self,listofquaders,XMLWriter):
        if not listofquaders:
            return
        for quader in listofquaders:
                Point=self.__Calculate3DPointIR__(quader.x,quader.y)
                w = quader.widthx*self.irlenperpix[0]
                h = quader.widthy*self.irlenperpix[1]
                XMLWriter.AddNewQuader(Point[0],Point[1],0,w,h,quader.height,quader.angle)
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
            XMLWriter.AddNewBlobQuader(Point[0],Point[1],0,0)
        return


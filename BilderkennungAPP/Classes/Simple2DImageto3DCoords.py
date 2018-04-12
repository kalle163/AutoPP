import numpy as np 
import cv2
from Classes.XMLIO import *
import shelve
import Kinect.const as const
import math 

class Simple2DImageto3DCoords(object):

    def __init__(self):
        self.distancetoground= np.load(const.rootfolder+"/distancetoground.npy")
        self.depthfov = const.fovofkinectv2depth
        self.rgbfov = const.fovofkinectv2rgb
        return super(Simple2DImageto3DCoords, self).__init__()

    def __Calculate3DPoint__(self,u,v,dis):
        dis=float(dis)
        u=float(u)
        v=float(v)
        Point=np.zeros((3,1),dtype="float")
        Point[0]= math.tan(self.depthfov[0]/2*math.pi/180)*dis*2*u/const.ir_image_size[0]
        Point[1]=math.tan(self.depthfov[1]/2*math.pi/180)*dis*2*v/const.ir_image_size[1]
        Point[2]=(self.distancetoground-dis)
        return Point

    def ConvertPixQuadertoCoordQuader(self,listofquaders,XMLWriter):
        if not listofquaders:
            return
        for quader in listofquaders:
            x1= quader.x
            y1= quader.y
            z= quader.height
            x2 =quader.x+quader.widthx
            y2 =quader.y+quader.widthy
            if not z==0:
                Point1=self.__Calculate3DPoint__(x1,y1,z)
                Point2=self.__Calculate3DPoint__(x2,y2,z)
                XMLWriter.AddNewQuader(Point1[0],Point1[1],0,abs(Point1[0]-Point2[0]),abs(Point1[1]-Point2[1]),Point1[2])
        return

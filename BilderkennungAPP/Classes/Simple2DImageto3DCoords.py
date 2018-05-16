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
        localdis=dis
        localdistancetoground = self.distancetoground
        for x in range(0, 100):
            localx= (math.tan(self.depthfov[0]/2*math.pi/180)*dis*2*u/const.ir_image_size[0])-(math.tan(self.depthfov[0]/2*math.pi/180)*dis)
            localy= (math.tan(self.depthfov[1]/2*math.pi/180)*dis*2*v/const.ir_image_size[1])-(math.tan(self.depthfov[1]/2*math.pi/180)*dis)
            localdis=math.sqrt(math.pow(localdis,2)-math.sqrt(math.pow(localx,2)+math.pow(localy,2)))
            localdistancetoground = math.sqrt(math.pow(localdistancetoground,2)-math.sqrt(math.pow(localx,2)+math.pow(localy,2)))
        Point[0]= math.tan(self.depthfov[0]/2*math.pi/180)*localdis*2*u/const.ir_image_size[0]
        Point[1]=math.tan(self.depthfov[1]/2*math.pi/180)*localdis*2*v/const.ir_image_size[1]
        Point[2]=(localdistancetoground-localdis)
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
            x = int(keypoint.pt[0]*const.ir_image_size[0]/const.rgb_image_size[0])
            y = int(keypoint.pt[1]*const.ir_image_size[1]/const.rgb_image_size[1])
            z = depthframe[x,y]
            s = keypoint.size
            r = math.sqrt(s/math.pi)
            rad= math.tan(self.depthfov[0]/2*math.pi/180)*z*2*r/const.ir_image_size[0]
            Point = self.__Calculate3DPoint__(x,y,z)
            XMLWriter.AddNewBall(Point[0],Point[1],Point[2],rad)
        return

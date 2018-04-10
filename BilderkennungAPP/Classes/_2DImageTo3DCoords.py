import numpy as np 
import cv2
from Classes.XMLIO import *
import shelve
import Kinect.const as const

class C2DImageTo3DCoords(object):
    def __init__(self,floor):
        self.irCamera = shelve.open(const.irCameraIntrinsic+"/IR")
        self.depth_Fx = self.irCamera['camera_matrix'][0,0]
        self.depth_Fy = self.irCamera['camera_matrix'][1,1]
        self.depth_Cx = self.irCamera['camera_matrix'][0,2]
        self.depth_Cy = self.irCamera['camera_matrix'][1,2]
        self.rgbCamera = shelve.open(const.rgbCameraIntrinsic+"/RGB")
        self.rgb_Fx = self.rgbCamera['camera_matrix'][0,0]
        self.rgb_Fy = self.rgbCamera['camera_matrix'][1,1]
        self.rgb_Cx = self.rgbCamera['camera_matrix'][0,2]
        self.rgb_Cy = self.rgbCamera['camera_matrix'][1,2]
        self.ZeroPoint =np.zeros((3,1),dtype="float")
        floor=float(floor)
        floor=floor/1000 # floor distance in meters
        self.ZeroPoint[0] = floor*(0-self.depth_Cx)/self.depth_Fx #x0 
        self.ZeroPoint[1] = floor*(0-self.depth_Cy)/self.depth_Fy #y0
        self.ZeroPoint[2] = floor   
        return super(C2DImageTo3DCoords, self).__init__()  
        
    def __Calculate3DPoint__(self,u,v,z):
        Point = np.zeros((3,1),dtype="float")
        z=float(z)
        z=z/1000  #z in meters
        if (z > 0):
            Point[0] = (z*(u-self.depth_Cx)/self.depth_Fx) + abs(self.ZeroPoint[0]) #x
            Point[1] = (z*(v-self.depth_Cy)/self.depth_Fy) + abs(self.ZeroPoint[1]) #y
            Point[2] = abs(z-self.ZeroPoint[2])

        return Point

    def CalcualteCoodinatesOfQuaders(self,listofquaders,XMLWriter):
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

    def UndistortDepthFrame(self,frame):       
        frame = cv2.undistort(colorFrame,self.irCamera['camera_matrix'], self.irCamera['dist_coefs'])
        return frame
         


       
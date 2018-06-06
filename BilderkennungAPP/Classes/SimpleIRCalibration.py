
import cv2
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import Kinect.const as const
import time
from kivy.graphics.texture import Texture
import imutils

class SimpleIRCalibrator(object):
    def __init__(self):
        self.xyratio=1.0
        return super(SimpleIRCalibrator, self).__init__()

    def takePicture(self,chessboard):
        kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color |
                                             PyKinectV2.FrameSourceTypes_Infrared |
                                         PyKinectV2.FrameSourceTypes_Depth)
        pictureok = False
        while not pictureok: 
            #cv2.namedWindow('image',WINDOW_NORMAL)
            #cv2.resizeWindow('image', 600,600)
            while(cv2.waitKey(1) != 27):#wait ESC press
                colorFrame = kinect.get_last_infrared_frame()
                colorFrame = colorFrame.reshape(const.ir_image_size[0],const.ir_image_size[1])
                colorFrame = cv2.flip(colorFrame,+1);
                colorFrame = np.uint8(colorFrame/256)
                cv2.imshow('IR',colorFrame) 
            if not chessboard:
                pictureok = True
            found, corners = cv2.findChessboardCorners(colorFrame, const.pattern_size, flags=cv2.CALIB_CB_ADAPTIVE_THRESH)
            if found:
                rgbFilePath = const.rootfolder + "SimpleColorCalibration.jpg"
                cv2.imwrite(rgbFilePath, colorFrame)
                print("ok")
                pictureok = True
            else:
                print("Dont found chessboard in rgb frame. Repeat recording Picture")
            depthframe = kinect.get_last_depth_frame()
            depthframe = depthframe.reshape(const.ir_image_size[0],const.ir_image_size[1])
            depthframe= cv2.flip(depthframe,+1);
    
        cv2.destroyAllWindows()
        colorFrame = cv2.cvtColor(colorFrame,cv2.COLOR_GRAY2BGRA)
        self.colorframe = colorFrame
        self.depthframe =depthframe
        return 

    def PictureWithCross(self,rot,x,y):
         localcolorframe = self.colorframe.copy()
         localcolorframe = imutils.rotate(localcolorframe,rot)
         for k in range(-20,20):
             localcolorframe[y+k,x,:]=(0,0,255,255)
         for k in range(-20,20):
             localcolorframe[y,x+k,:]=(0,0,255,255)
         return _ColorFrameToKivyPicture_(localcolorframe)
   

    def find_points(self,rot):
        image = self.colorframe.copy()
        image = imutils.rotate(image,rot)
        if self.xyratio > 1:
            image = cv2.resize(image, (0,0), fx=(1/self.xyratio), fy=1.0) 
        elif self.xyratio < 1:
            image = cv2.resize(image, (0,0), fx=1.0, fy=self.xyratio) 
        color_image = image.copy()
        image = cv2.cvtColor(image,cv2.COLOR_BGRA2GRAY)
        cv2.imshow('Color',image)
        cv2.waitKey(0)
        debug_images = []
       
        found, corners = cv2.findChessboardCorners(image, const.pattern_size,  flags=cv2.CALIB_CB_ADAPTIVE_THRESH)
        if found:
            cv2.cornerSubPix(image, corners, (5, 5), (-1, -1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
            if (corners[3][0][1] - 30) >corners[0][0][1]:
                const.pattern_size = const.pattern_size[::-1]
                found, corners = cv2.findChessboardCorners(image, const.pattern_size,  flags=cv2.CALIB_CB_ADAPTIVE_THRESH)
                if found:
                    cv2.cornerSubPix(image, corners, (5, 5), (-1, -1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)) 
           
            cv2.drawChessboardCorners(color_image, const.pattern_size, corners, found)
            localareaofinterest = np.array([corners[0][0],corners[const.pattern_size[0]-1][0],corners[const.pattern_size[0]*(const.pattern_size[1]-1)][0],corners[(const.pattern_size[0]*const.pattern_size[1])-1][0]])
            print(corners)
            print("Interesse")
            print(localareaofinterest)
            areaofinterest = _SortAreaOfInterest_(localareaofinterest)
            print(areaofinterest)
            self.areaofinterest = areaofinterest
            self.sortedcorners = _SortCorners_(corners)
            cv2.imshow('Corner',color_image)
            cv2.waitKey(0)
            cv2.imwrite(const.rootfolder+"\IRChessbaord.jpg",color_image)
        else:
            print("Chessboard not found. No Area of Interst defined")
            areaofinterest = 0
        return  areaofinterest

    def Distortion(self,x,y):
        bigxyratio = ((((self.areaofinterest[1][0]-self.areaofinterest[0][0])+(self.areaofinterest[3][0]-self.areaofinterest[2][0]))/2)/(const.pattern_size[0]-1))/((((self.areaofinterest[2][1]-self.areaofinterest[0][1])+(self.areaofinterest[3][1]-self.areaofinterest[1][1]))/2)/(const.pattern_size[1]-1))
        print(bigxyratio)
        self.xyratio = bigxyratio
        if bigxyratio > 1:
            x=int(x/bigxyratio)
        elif bigxyratio < 1:
            y=int(y*bigxyratio)
        return bigxyratio,x,y

    def Exit(self):
        bigxyratio = ((((self.areaofinterest[1][0]-self.areaofinterest[0][0])+(self.areaofinterest[3][0]-self.areaofinterest[2][0]))/2)/(const.pattern_size[0]-1))/((((self.areaofinterest[2][1]-self.areaofinterest[0][1])+(self.areaofinterest[3][1]-self.areaofinterest[1][1]))/2)/(const.pattern_size[1]-1))
        print(bigxyratio)
        xlenperpix = const.square_size/((((self.areaofinterest[1][0]-self.areaofinterest[0][0])+(self.areaofinterest[3][0]-self.areaofinterest[2][0]))/2)/(const.pattern_size[0]-1))
        ylenperpix = const.square_size/((((self.areaofinterest[2][1]-self.areaofinterest[0][1])+(self.areaofinterest[3][1]-self.areaofinterest[1][1]))/2)/(const.pattern_size[1]-1))
        return xlenperpix, ylenperpix

    def takedepth(self,x,y,rot):
        image = self.depthframe.copy()
        image = imutils.rotate(image,rot)
        if self.xyratio > 1:
            image = cv2.resize(image, (0,0), fx=(1/self.xyratio), fy=1.0) 
        elif self.xyratio < 1:
            image = cv2.resize(image, (0,0), fx=1.0, fy=self.xyratio) 
        depth = image[x,y]
        return depth 


def _SortAreaOfInterest_(localareaofinterest):
    avgx=0
    avgy=0
    for point in localareaofinterest:
        avgx=avgx+point[0]
        avgy=avgy+point[1]
    avgx=avgx/4
    avgy=avgy/4
    areaofinterest = np.zeros((4,2),dtype=float)    
    find=False
    i=0
    while not find:
        if localareaofinterest[i][0] < avgx and localareaofinterest[i][1] < avgy:
            find=True
        else:
            i=i+1
    areaofinterest[0]=localareaofinterest[i]
    find=False
    i=0
    while not find:
        if localareaofinterest[i][0] > avgx and localareaofinterest[i][1] < avgy:
            find=True
        else:
            i=i+1
    areaofinterest[1]=localareaofinterest[i]
    find=False
    i=0
    while not find:
        if localareaofinterest[i][0] < avgx and localareaofinterest[i][1] > avgy:
            find=True
        else:
            i=i+1
    areaofinterest[2]=localareaofinterest[i]
    find=False
    i=0
    while not find:
        if localareaofinterest[i][0] > avgx and localareaofinterest[i][1] > avgy:
            find=True
        else:
            i=i+1
    areaofinterest[3]=localareaofinterest[i]
    return areaofinterest

def _ColorFrameToKivyPicture_(colorframe):
        texturecolor = Texture.create(size=(512,424),colorfmt='bgr')
        colorframe= cv2.cvtColor(colorframe,cv2.COLOR_BGRA2BGR)
        colorframe = cv2.flip(colorframe,0);
        colorframe = colorframe.reshape(424*512*3)
        texturecolor.blit_buffer(colorframe,bufferfmt='ubyte',colorfmt='bgr')
        return texturecolor 

def _SortCorners_(corners):
    if corners[0][0][1] > corners[(const.pattern_size[0]*const.pattern_size[1])-1][0][1]:
        horswift=True
    else:
        horswift=False
    if corners[0][0][0] > corners[(const.pattern_size[0]*const.pattern_size[1])-1][0][0]:
        verswift=True
    else:
        verswift=False
    corners = corners.reshape(const.pattern_size[0]*const.pattern_size[1]*2)
    corners = corners.reshape(const.pattern_size[1],const.pattern_size[0],2)
    if horswift:
        corners=np.flipud(corners)
    if verswift:
        corners=np.fliplr(corners)
    return corners
import cv2
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import Kinect.const as const
import time
from kivy.graphics.texture import Texture
import imutils

class SimpleCalibrator(object):
    def __init__(self):
        return super(SimpleCalibrator, self).__init__()

    def takePicture(self,chessboard):
        kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color |
                                             PyKinectV2.FrameSourceTypes_Infrared |
                                         PyKinectV2.FrameSourceTypes_Depth)
        pictureok = False
        while not pictureok: 
            #cv2.namedWindow('image',WINDOW_NORMAL)
            #cv2.resizeWindow('image', 600,600)
            while(cv2.waitKey(1) != 27):#wait ESC press
                colorFrame = kinect.get_last_color_frame()
                colorFrame = colorFrame.reshape(const.rgb_image_size[1],const.rgb_image_size[0],4)
                colorFrame = cv2.flip(colorFrame,+1);
                cv2.imshow('RGB',colorFrame) 
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
    
        cv2.destroyAllWindows()
        self.colorframe = colorFrame
        return 

    def PictureWithCross(self,rot,x,y):
         localcolorframe = self.colorframe.copy()
         localcolorframe = imutils.rotate(localcolorframe,rot)
         for k in range(-30,30):
             localcolorframe[y+k,x-1,:]=(0,0,255,255)
             localcolorframe[y+k,x,:]=(0,0,255,255)
             localcolorframe[y+k,x+1,:]=(0,0,255,255)
         for k in range(-30,30):
             localcolorframe[y-1,x+k,:]=(0,0,255,255)
             localcolorframe[y,x+k,:]=(0,0,255,255)
             localcolorframe[y+1,x+k,:]=(0,0,255,255)
         return _ColorFrameToKivyPicture_(localcolorframe)
   

    def find_points(self,rot):
        PATTERN_SIZE = (7, 5)
        image = self.colorframe.copy()
        image = imutils.rotate(image,rot)
        color_image = image.copy()
        image = cv2.cvtColor(image,cv2.COLOR_BGRA2GRAY)
        cv2.imshow('Color',image)
        cv2.waitKey(0)
        debug_images = []
       
        found, corners = cv2.findChessboardCorners(image, PATTERN_SIZE,  flags=cv2.CALIB_CB_ADAPTIVE_THRESH)
        if found:
            cv2.cornerSubPix(image, corners, (5, 5), (-1, -1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
            cv2.drawChessboardCorners(color_image, PATTERN_SIZE, corners, found)
            print(corners)
            cv2.imshow('Corner',color_image)
            cv2.waitKey(0)
        return 






def _ColorFrameToKivyPicture_(colorframe):
        texturecolor = Texture.create(size=(1920,1080),colorfmt='bgr')
        colorframe= cv2.cvtColor(colorframe,cv2.COLOR_BGRA2BGR)
        colorframe = cv2.flip(colorframe,0);
        colorframe = colorframe.reshape(1080*1920*3)
        texturecolor.blit_buffer(colorframe,bufferfmt='ubyte',colorfmt='bgr')
        return texturecolor 


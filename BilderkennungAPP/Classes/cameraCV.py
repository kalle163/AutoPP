import numpy as np
import cv2
import pykinect2.PyKinectRuntime as PKR
import pykinect2.PyKinectV2 as PKV
import ctypes
import _ctypes
import sys


class CameraPyKinectCV(object):
    
    def __init__(self):
        self._kinect =  PKR.PyKinectRuntime(PKV.FrameSourceTypes_Color | PKV.FrameSourceTypes_Depth | PKV.FrameSourceTypes_BodyIndex)
        

    def showpicturecolor(self):
        framedone=False
        while True:
            while not framedone:
                if self._kinect.has_new_color_frame():
                    frame = self._kinect.get_last_color_frame()
                    framedone=True;
            frame= frame.reshape(1080,1920,4)
            cv2.imshow('Image',frame)
            cv2.waitKey(1);
            framedone=False

    def showpicturedepth(self):
        framedone=False
        while True:
            while not framedone:
                if self._kinect.has_new_depth_frame():
                    frame = self._kinect.get_last_depth_frame()
                    framedone=True;
            frame= frame.reshape(424,512)
            
            max= frame.max()
            frame2=np.zeros(424*512*4,dtype=np.uint8)
            frame2=frame2.reshape(424,512,4)
            for depthx in  range(0,frame.shape[0]):
                for depthy in range(0,frame.shape[1]):
                    z=frame[depthx,depthy]
                    z=z*258/max                   
                    frame2[depthx,depthy,0]=z
                    frame2[depthx,depthy,1]=z
                    frame2[depthx,depthy,2]=z
                    frame2[depthx,depthy,3]=258
            cv2.imwrite('D:/test.bmp',frame2)
            cv2.imshow('Image',frame2)
            cv2.waitKey(25);
            framedone=False

    def showpicturebody(self):
        framedone=False
        while True:
            while not framedone:
                if self._kinect.has_new_body_index_frame():
                    frame = self._kinect.get_last_body_index_frame()
                    framedone=True;
            frame= frame.reshape(424,512) 
            cv2.imshow('Image',frame)
            cv2.waitKey(1);
            framedone=False

    
    def getpicturedepth(self,maxabstandzumboden):
        framedone=False
        while not framedone:
            if self._kinect.has_new_depth_frame():
               frame = self._kinect.get_last_depth_frame()
               framedone=True;            
        max=0.0
        while max==0.0:
            if frame.max() > maxabstandzumboden:
                frame[np.unravel_index(frame.argmax(), frame.shape)]=0
            else:
                max=float(frame.max())
        frame2=frame.astype(float)
        frame2*=255/max
        frame2=frame2.astype(int)
        frame2=np.matrix(frame2)
        frame2=np.transpose(frame2)
        multiplicator=np.matrix([1,1,1])
        frame2=frame2*multiplicator
        frame2=frame2.A
        frame2=frame2.astype(np.uint8)
        frame2=frame2.reshape(424*512*3)
        frame=frame.reshape(424,512)
        return frame,frame2
            
    
    def getpicturecolor(self):
        framedone=False
        
        while not framedone:
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                framedone=True;
        frame=frame.reshape(1080,1920,4)
        return frame

           
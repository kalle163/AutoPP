import numpy as np
import cv2
import pykinect2.PyKinectRuntime as PKR
import pykinect2.PyKinectV2 as PKV
import ctypes
import _ctypes
import sys
import operator


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

    
    def getpicturedepth(self):
        framedone=False
        while not framedone:
            if self._kinect.has_new_depth_frame():
               frame = self._kinect.get_last_depth_frame()
               framedone=True;  
        unique, counts = np.unique(frame, return_counts=True)
        anzahl=dict(zip(unique, counts))
        new_anzahl = {k: v for k, v in anzahl.iteritems() if v >= 10}        
        maxi=max(new_anzahl, key=np.uint16)
        frame2=frame.astype(float)
        frame2*=255.0/maxi
        frame2[frame2>255.0] = 255.0
        frame2=frame2.astype(np.uint8)
        frame2=frame2.reshape(424,512)
        frame=frame.reshape(424,512)
        g=maxi/255
        return frame,frame2,g,maxi
            
    
    def getpicturecolor(self):
        framedone=False
        
        while not framedone:
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                framedone=True;
        frame=frame.reshape(1080,1920,4)
        return frame

           
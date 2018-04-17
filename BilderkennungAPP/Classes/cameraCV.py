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
        self._kinect =  PKR.PyKinectRuntime(PKV.FrameSourceTypes_Color | PKV.FrameSourceTypes_Depth |  PKV.FrameSourceTypes_Infrared)
        

    
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
        return frame,frame2,g
            
    
    def getpicturecolor(self):
        framedone=False
        
        while not framedone:
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                framedone=True;
        frame=frame.reshape(1080,1920,4)
        return frame

        
    def getpictureir(self):
        framedone=False
        while not framedone:
            if self._kinect.has_new_infrared_frame():
                frame = self._kinect.get_last_infrared_frame()  
                framedone=True
        frame=frame.reshape(424,512)
        return frame
       
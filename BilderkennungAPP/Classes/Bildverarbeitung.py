import numpy as np 
from kivy.graphics.texture import Texture
from array import array
import cv2
import Kinect.const as const
from imutils import contours
from skimage import measure

class Bildverarbeitung(object):

    texturedepth = Texture.create(size=(512,424),colorfmt='bgr')
    texturecolor = Texture.create(size=(1920,1080),colorfmt='bgr')
    def __init__(self, *args, **kwargs):
        return super(Bildverarbeitung, self).__init__(*args, **kwargs)
    def DetphFrameToKivyPicture(self,depthframe):
        depthframe = depthframe.reshape(424*512)
        depthframe=cv2.cvtColor(depthframe,cv2.COLOR_GRAY2BGR)
        depthframe = depthframe.reshape(424*512*3)
        self.texturedepth.blit_buffer(depthframe,bufferfmt='ubyte',colorfmt='bgr')
        return self.texturedepth
    def ColorFrameToKivyPicture(self,colorframe):
        colorframe = colorframe.reshape(1080*1920*3)
        self.texturecolor.blit_buffer(colorframe,bufferfmt='ubyte',colorfmt='bgr')
        return self.texturecolor 
    def DetectionOfDepthObjects(self,framemilli,framegrey,g):
        a,b=GetMinDistances(g)
        frametherehold = np.zeros(framegrey.shape,dtype='uint8')
        frametherehold = cv2.threshold(framegrey,(255-a),255,cv2.THRESH_TOZERO_INV)
        frametherehold = frametherehold[1]
        cv2.imshow('frametherehold',frametherehold)
        cv2.waitKey(0)
        labels = measure.label(frametherehold,background=0,connectivity=3)
        mask = np.zeros(frametherehold.shape,dtype="uint8")
        for label in np.unique(labels):
	        if label == 0:
		        continue
	        labelMask = np.zeros(thresh.shape, dtype="uint8")
	        labelMask[labels == label] = 255
	        numPixels = cv2.countNonZero(labelMask)
	        if numPixels > 30:
		        mask = cv2.add(mask, labelMask)
        
        print("blabla")
        return 

def GetMinDistances(g):
     if const.distancefirstobjecttofloor > g:
         i=1
         while(const.distancefirstobjecttofloor> g*i):
             i+=1
         a=i

     else:
         a = g
     if const.distanceobjecttoobject >g:
         i=1
         while(const.distanceobjecttoobject> g*i):
             i+=1
         b=i
     else:
         b= g
     print(str(a)+"  "+str(b))
     return a,b 
    
    
    
    


        
       


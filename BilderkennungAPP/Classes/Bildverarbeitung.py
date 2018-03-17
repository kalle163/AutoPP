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
        depthframe = depthframe.reshape(424*512*3)
        self.texturedepth.blit_buffer(depthframe,bufferfmt='ubyte',colorfmt='bgr')
        return self.texturedepth
    def ColorFrameToKivyPicture(self,colorframe):
        colorframe = colorframe.reshape(1080*1920*3)
        self.texturecolor.blit_buffer(colorframe,bufferfmt='ubyte',colorfmt='bgr')
        return self.texturecolor 
    def DetectionOfDepthObjects(self,framemilli,framegrey):
        framegrey=framegrey.reshape(424,512,3)
        frametherehold = cv2.threshold(framegray,10,255,cv2.THRESH_TOZERO)
        frametherehold = cv2.erode(thresh, None, iterations=2)
        frametherehold = cv2.dilate(thresh, None, iterations=4)
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
    
    
    
    


        
       


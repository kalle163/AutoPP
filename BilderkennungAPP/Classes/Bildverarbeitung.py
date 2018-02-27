import numpy as np 
from kivy.graphics.texture import Texture
from array import array
import cv2
import Kinect.const as const

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
        cv2.imshow('framegrey',framegrey)
        cv2.waitKey(0)
        cv2.imwrite(const.rootfolder+"/framegrayohneblur.jpg",framegrey)
        framegrey=cv2.GaussianBlur(framegrey,(3,3),0)
        cv2.imshow('framegrey',framegrey)
        cv2.waitKey(0)
        cv2.imwrite(const.rootfolder+"/framegraymitblur.jpg",framegrey)
        grey=framegrey[:,:,1]
        cv2.imshow('framegrey',grey)
        cv2.waitKey(0)
        framemask=np.zeros((256,424,512),dtype=np.uint8)
        
        for i in range(0,256):
            framemask[i,:,:]=cv2.inRange(grey,i,i)
        
        
      
        print("blabla")
        return 
    
    
    
    


        
       


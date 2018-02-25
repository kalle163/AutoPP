import numpy as np 
from kivy.graphics.texture import Texture
from array import array

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
    
    
    
    
    
    def DepthFrameToPointCloud(self,z,scale=1000):
        C, R = np.indices(z.shape)
        R = np.subtract(R, self.CameraParams['cx'])
        R = np.multiply(R, z)
        R = np.divide(R, self.CameraParams['fx'] * scale)
        C = np.subtract(C, self.CameraParams['cy'])
        C = np.multiply(C, z)
        C = np.divide(C, self.CameraParams['fy'] * scale)
        return z.ravel() / scale, R.ravel(), -C.ravel()
    def AutoFindFloor(self,z):
        max=float(z.max())
        minimax = max-40.0
        s= z<minimax
        s= s.astype(int)
        z=np.multiply(s,z)
        return z
        

        
       


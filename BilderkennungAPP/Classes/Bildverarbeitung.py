import numpy as np 
from kivy.graphics.texture import Texture
from array import array
import cv2
import Kinect.const as const
from imutils import contours
from skimage import measure
import imutils

class Bildverarbeitung(object):

    texturedepth = Texture.create(size=(512,424),colorfmt='bgr')
    texturecolor = Texture.create(size=(1920,1080),colorfmt='bgr')
    def __init__(self, *args, **kwargs):
        self.listofdetectedobjectspixel=list()
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
        for area in const.NoDetectionArea:
            frametherehold[area[1]:area[1]+area[3],area[0]:area[0]+area[2]]=np.zeros((area[3],area[2]),dtype='uint8')
        frametherehold = cv2.erode(frametherehold, None, iterations=2)
        frametherehold = cv2.dilate(frametherehold, None, iterations=4)
        cv2.imshow('frametherehold',frametherehold)
        cv2.waitKey(0)
        cv2.imwrite(const.rootfolder+"/thereholdframe.jpg",frametherehold)
        labels = measure.label(frametherehold,neighbors=8,background=0)
        mask = np.zeros(frametherehold.shape,dtype="uint8")
        for label in np.unique(labels):
	        if label == 0:
		        continue
	        labelMask = np.zeros(frametherehold.shape, dtype="uint8")
	        labelMask[labels == label] = 255
	        numPixels = cv2.countNonZero(labelMask)
	        if numPixels > 30:
		        mask = cv2.add(mask, labelMask)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        cnts = contours.sort_contours(cnts)[0]
        
        for (i, c) in enumerate(cnts):
	        (x,y,w,h) = cv2.boundingRect(c)
                #heightofobject=framemilli[x:x+w,y:y+h]               
                #self.listofdetectedobjectspixel.append(RectanglePixel(x,y,w,h,heightofobject.mean()))
                new_mask[i]=np.zeros(mask.shape,dtype='uint8')
                new_mask[x:x+w,y:y+h]=mask[x:x+w,y:y+h]
        i=0
        for maskf in new_mask:
            k=0
            lowervalue=max(mask)
            while IsHigherValueInArray(maskf,lowervalue) and IsHigherValueInArray(maskf,0):
                area[i,k] = cv2.threshold(maskf,lowervalue-b,255,cv2.THRESH_TOZERO)
                maskf=cv2.threshold(mmaskf,lowervalue-b,255,cv2.THRESH_TOZERO_INV)
                lowervalue=max(mask)
                k+=1
            area[i,k]=maskf
            i+=1
        new_area = np.zeros(mmask.shape(),dtype='uint8')
        for k in range(len(area)-1,0):
            z=GetMeansWithoutZeros(area[k])
            new_area=cv2.bitwise_or(area[k],new_area)
            cnts = cv2.findContours(new_area.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if imutils.is_cv2() else cnts[1]
            cnts = contours.sort_contours(cnts)[0]       
            for (i, c) in enumerate(cnts):
	            (x,y,w,h) = cv2.boundingRect(c)
                    self.listofdetectedobjectspixel.append(RectanglePixel(x,y,w,h,z))
        cv2.imshow('detected',mask)
        cv2.waitKey(0)

        print("blabla")
        return self.listofdetectedobjectspixel


    
class RectanglePixel(object):
    Properties={
        "x":0,
        "y":0,
        "widthx":0,
        "widthy":0,
        "height":0,   #in mm 
        }
    def __init__(self,x,y,widthx,widthy,height):
        self.Properties["x"]=x
        self.Properties["y"]=y
        self.Properties["widthx"]=widthx
        self.Properties["widthy"]=widthy
        self.Properties["height"]=height
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
 
def IsHigherValueInArray(A,thr):
     B=A[A>thr]
     if len(B)>0:
         return True
     else:
         return False

def IsLowerValueInArray(A,thr):
     B=A[A<thr]
     if len(B)>0:
         return True
     else:
         return False
        
def IsHigherValueInArray(A,thr):
     B=A[A>thr]
     if len(B)>0:
         return True
     else:
         return False       

def GetMeansWithoutZeros(matrix):
    matrix=matrix.astype(float)
    matrix[np.where(matrix == 0)] = np.nan
    mean = int(np.nanmean(matrix))  
    return mean
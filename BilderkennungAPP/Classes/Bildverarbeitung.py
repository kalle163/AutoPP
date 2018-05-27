import numpy as np 
from kivy.graphics.texture import Texture
from array import array
import cv2
import Kinect.const as const
from imutils import contours
from skimage import measure
import imutils
import shelve


class RectanglePixel(object):

    def __init__(self,x,y,widthx,widthy,height):
        self.x=x
        self.y=y
        self.widthx=widthx
        self.widthy=widthy
        self.height=height
        return 


class Bildverarbeitung(object):

    texturedepth = Texture.create(size=(512,424),colorfmt='bgr')
    texturecolor = Texture.create(size=(1920,1080),colorfmt='bgr')
    def __init__(self, *args, **kwargs):
        return super(Bildverarbeitung, self).__init__(*args, **kwargs)
    def DetphFrameToKivyPicture(self,depthframe):
        depthframe = cv2.flip(depthframe,0);
        depthframe = depthframe.reshape(424*512)
        depthframe=cv2.cvtColor(depthframe,cv2.COLOR_GRAY2BGR)
        depthframe = depthframe.reshape(424*512*3)
        self.texturedepth.blit_buffer(depthframe,bufferfmt='ubyte',colorfmt='bgr')
        return self.texturedepth
    def ColorFrameToKivyPicture(self,colorframe):
        colorframe = cv2.flip(colorframe,0);
        colorframe = colorframe.reshape(1080*1920*3)
        self.texturecolor.blit_buffer(colorframe,bufferfmt='ubyte',colorfmt='bgr')
        return self.texturecolor 
    def DetectionOfDepthObjects(self,framemilli,framegrey,g):
        #framemilli= UndistortDethFrameMilli(framemilli)
        show = True   #Set to False to Hide Pictures
        framegrey = cv2.flip(framegrey,1);
        framemilli = cv2.flip(framemilli,1);
        a,b=GetMinDistances(g)
        frametherehold = np.zeros(framegrey.shape,dtype='uint8')
        frametherehold = cv2.threshold(framegrey,(255-a),255,cv2.THRESH_TOZERO_INV)
        frametherehold = frametherehold[1]
        for area in const.NoDetectionArea:
            frametherehold[area[1]:area[1]+area[3],area[0]:area[0]+area[2]]=np.zeros((area[3],area[2]),dtype='uint8')
        frametherehold= cv2.medianBlur(frametherehold,5)
        frametherehold = cv2.erode(frametherehold, None, iterations=2)
        frametherehold = cv2.dilate(frametherehold, None, iterations=4)
        if(show):
            cv2.imshow('frametherehold',frametherehold)
            cv2.waitKey(0)
        #cv2.imwrite(const.rootfolder+"/thereholdframe.jpg",frametherehold)
        mask=frametherehold.copy()       
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        cnts = contours.sort_contours(cnts)[0]
        new_mask=[]
        for (i, c) in enumerate(cnts):
	        (x,y,w,h) = cv2.boundingRect(c)
                new_maskf=np.zeros(mask.shape,dtype='uint8')
                new_maskf[y:y+h,x:x+w]=mask[y:y+h,x:x+w]
                new_mask.append(new_maskf)
        i=0
        area=[]
        
        for maskf in new_mask:
            k=0
            lowervalue=maskf.max()
            areawh=[]
            while IsLowerValueInArray(maskf,lowervalue-b):
                m=cv2.threshold(maskf,lowervalue-b,255,cv2.THRESH_TOZERO)
                m=m[1]
                if(show):
                    cv2.imshow('newmask',m)
                    cv2.waitKey(0)
                areawh.append(m)
                maskf=cv2.threshold(maskf,lowervalue-b,255,cv2.THRESH_TOZERO_INV)
                maskf=maskf[1]
                if(show):
                    cv2.imshow('newmask',maskf)
                    cv2.waitKey(0)
                numPixels = cv2.countNonZero(maskf)
                if numPixels<20:
                     break
                lowervalue=maskf.max()
                k+=1
            areawh.append(maskf)
            i+=1
            area.append(areawh)
            listofdetectedobjectspixel=list()
        for areaf in area:
            new_area = np.zeros(mask.shape,dtype='uint8')
            for k in range(len(areaf)-1,-1,-1):                
                cnts = cv2.findContours(areaf[k].copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                cnts = cnts[0] if imutils.is_cv2() else cnts[1]
                cnts = contours.sort_contours(cnts)[0]       
                for (i, c) in enumerate(cnts):
	                (x,y,w,h) = cv2.boundingRect(c)
                        condittion = areaf[k] != 0
                        con = condittion.astype(int)
                        localframemilli = np.multiply(framemilli,con)
                        localframemilli[localframemilli >  np.min(localframemilli[np.nonzero(localframemilli)])+5] =0
                        z=GetMeansWithoutZeros(localframemilli[y:y+h,x:x+w])
                new_area=cv2.bitwise_or(areaf[k],new_area)
                if(show):
                    cv2.imshow('newarea',new_area)
                    cv2.waitKey(0)
                #cv2.imwrite(const.rootfolder+"/newarea"+str(k)+".jpg",new_area)
                cnts = cv2.findContours(new_area.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                cnts = cnts[0] if imutils.is_cv2() else cnts[1]
                cnts = contours.sort_contours(cnts)[0]       
                for (i, c) in enumerate(cnts):
	                (x,y,w,h) = cv2.boundingRect(c)          
                        listofdetectedobjectspixel.append(RectanglePixel(x,y,w,h,z))

        return listofdetectedobjectspixel



def find_squares(img):
    contours, _hierarchy = find_contours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
        area = cv2.contourArea(cnt)
        if len(cnt) == 4  and cv2.isContourConvex(cnt):
            cnt = cnt.reshape(-1, 2)
            max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
            if max_cos < 0.1:
                if (1 - (float(w) / float(h)) <= 0.07 and 1 - (float(h) / float(w)) <= 0.07):
                    squares.append(cnt)
    return squares 

    

    
 
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
     B=A[(A<thr) & (A>0)]
     if len(B)>0:
         return True
     else:
         return False
              

def GetMeansWithoutZeros(matrix):
    matrix=matrix.astype(float)
    if np.count_nonzero(matrix)>0:
        matrix[np.where(matrix == 0)] = np.nan
        mean = int(np.nanmean(matrix))
    else:
        mean =0
    return mean

def UndistortDethFrameMilli(frame):
    irCamera = shelve.open(const.irCameraIntrinsic+"/IR")
    newDepthCameraMatrix, roi=cv2.getOptimalNewCameraMatrix(irCamera['camera_matrix'],irCamera['dist_coefs'],const.ir_image_size[::-1],1,const.ir_image_size[::-1])
    mapx,mapy = cv2.initUndistortRectifyMap(irCamera['camera_matrix'],irCamera['dist_coefs'],None,newDepthCameraMatrix,const.ir_image_size[::-1],5)
    del roi
    frame = cv2.remap(frame,mapx,mapy,cv2.INTER_CUBIC) #undistort frame
    return frame
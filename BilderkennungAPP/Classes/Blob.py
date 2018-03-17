import cv2
import numpy as np
import Kinect.const as const

class Blob(object):
    def __init__(self,listofblobobjects):
        self.listofdetectors=list()        
        if len(listofblobobjects)>=1:
            for blobobject in listofblobobjects:
                params = cv2.SimpleBlobDetector_Params()
                params.minThreshold=0
                params.maxThreshold=255

                #Filter by Color
                params.filterByColor=False

                # Filter by Area.
                params.filterByArea = True
                params.minArea = blobobject.Properties["minarea"]
                if blobobject.Properties["maxarea"]>=0:
                    params.maxArea =blobobject.Properties["maxarea"]

                # Filter by Circularity
                params.filterByCircularity = True
                params.minCircularity = blobobject.Properties["mincircularity"]
                params.maxCircularity = blobobject.Properties["maxcircularity"]
                
                # Filter by Convexity
                params.filterByConvexity = True
                params.minConvexity = blobobject.Properties["minconvexity"]
                params.maxConvexity = blobobject.Properties["maxconvexity"]
    
                # Filter by Inertia
                params.filterByInertia = True
                params.minInertiaRatio = blobobject.Properties["mininertiaratio"]
                params.maxInertiaRatio = blobobject.Properties["maxinertiaratio"]


                detector = Detector(params,blobobject.Properties["minrgb"],blobobject.Properties["maxrgb"],blobobject.Properties["minhsv"],blobobject.Properties["maxhsv"],blobobject.Properties["mingrey"],blobobject.Properties["maxgrey"])
                self.listofdetectors.append(detector)
                
        else:

            params = cv2.SimpleBlobDetector_Params()
            params.minThreshold=0
            params.maxThreshold=256


            #Filter by Color
            params.filterByColor=False

            # Filter by Area.
            params.filterByArea = True
            params.minArea = 0

            # Filter by Circularity
            params.filterByCircularity = True
            params.minCircularity = 0.0
            params.maxCircularity = 1.0

            # Filter by Convexity
            params.filterByConvexity = True
            params.minConvexity = 0.0
            params.maxConvexity = 1.0
    
            # Filter by Inertia
            params.filterByInertia = True
            params.minInertiaRatio = 0.0
            params.maxInertiaRatio = 1.0
            detector = Detector(params,(0,0,0),(255,255,255),(0,0,0),(255,255,255),0,255)
            self.listofdetectors.append(detector)
         
        return

    def blobdetection(self,colorframe,show=False,save=False):
        self.listofkeypoints=list()

        colorframe=cv2.GaussianBlur(colorframe,(3,3),0)
        greyframe = cv2.cvtColor(colorframe,cv2.COLOR_RGBA2GRAY)
        colorframe= cv2.cvtColor(colorframe,cv2.COLOR_RGBA2RGB)

        hsv= cv2.cvtColor(colorframe,cv2.COLOR_RGB2HSV)
        hue = hsv[:,:,0]
        sat = hsv[:,:,1]
        val = hsv[:,:,2]

        if show:
            cv2.imshow('colorrgb',colorframe)
            cv2.waitKey(0)
            cv2.imshow('greyframe',greyframe)
            cv2.waitKey(0)
            cv2.imshow('hsv',hsv)
            cv2.waitKey(0)    
            cv2.imshow('hue',hue)
            cv2.waitKey(0)
            cv2.imshow('sat',sat)
            cv2.waitKey(0)
            cv2.imshow('val',val)
            cv2.waitKey(0)   
        if save:
            cv2.imwrite(const.rootfolder+"/rgb.jpg",colorframe)
            cv2.imwrite(const.rootfolder+"/grey.jpg",greyframe)
            cv2.imwrite(const.rootfolder+"/hsv.jpg",hue)
            cv2.imwrite(const.rootfolder+"/hue.jpg",hue)
            cv2.imwrite(const.rootfolder+"/sat.jpg",sat)
            cv2.imwrite(const.rootfolder+"/val.jpg",val)
            i=0
        for detector in self.listofdetectors:
            i=i+1
            mask = cv2.inRange(hsv,)
            maskcolor= cv2.inRange(colorframe,)
            maskgrey = cv2.inRange(greyframe,)
            fullmask= cv2.bitwise_and(mask,maskcolor)
            fullmask = cv2.bitwise_and(fullmask,maskgrey)       
            fullmask = cv2.erode(fullmask, None, iterations=2)
            fullmask = cv2.dilate(fullmask, None, iterations=4)
            reversemask=255-fullmask

            if show:
                cv2.imshow('mask',mask)
                cv2.waitKey(0)
                cv2.imshow('maskcolor',maskcolor)
                cv2.waitKey(0) 
                cv2.imshow('maskgrey',maskgrey)
                cv2.waitKey(0)
                cv2.imshow('fullmask',fullmask)
                cv2.waitKey(0)    
                cv2.imshow('reversemask',reversemask)
                cv2.waitKey(0)
            if save:
                cv2.imwrite(const.rootfolder+"/maskhsv"+str(i)+".jpg",mask)
                cv2.imwrite(const.rootfolder+"/maskcolor"+str(i)+".jpg",maskcolor)
                cv2.imwrite(const.rootfolder+"/maskgrey"+str(i)+".jpg",maskgrey)
                cv2.imwrite(const.rootfolder+"/fullmask"+str(i)+".jpg",fullmask)
                cv2.imwrite(const.rootfolder+"/reversemask"+str(i)+".jpg",reversemask)
            
            self.listofkeypoints.append(detector.detect(reversemask))
            im_with_keypoints=colorframe
        for keypoints in self.listofkeypoints:
            im_with_keypoints = cv2.drawKeypoints(im_with_keypoints, keypoints, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  
        
        return im_with_keypoints

class Detector(cv2.SimpleBlobDetector):

    def __init__(self,params,minrgb,maxrgb,minhsv,maxhsv,mingrey,maxgrey):
        super(Detector,self).__init__(params)
        self.minrgb=minrgb
        self.maxrgb=maxrgb
        self.minhsv=minhsv
        self.maxhsv=maxhsv
        self.mingrey=mingrey
        self.maxgrey=maxgrey
        return


    



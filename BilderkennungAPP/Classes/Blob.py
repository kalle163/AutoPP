import cv2
import numpy as np
import Kinect.const as const

class Blob(object):
  
    def __init__(self):
        params = cv2.SimpleBlobDetector_Params()
            
        params.minThreshold=0
        params.maxThreshold=256


        #Filter by Color
        params.filterByColor=False
        params.blobColor = 0

        # Filter by Area.
        params.filterByArea = True
        params.minArea = 40

        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = 0.9

        # Filter by Convexity
        params.filterByConvexity = True
        params.minConvexity = 0.8
    
        # Filter by Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.9

        # Create a detector with the parameters
        ver = (cv2.__version__).split('.')
        if int(ver[0]) < 3:
	        self.detector = cv2.SimpleBlobDetector(params)
        else: 
	        self.detector = cv2.SimpleBlobDetector_create(params)

    def blobdetection(self,colorframe):
        
        colorframe=cv2.GaussianBlur(colorframe,(3,3),0)
        cv2.imshow('color',colorframe)
        cv2.waitKey(0)

        greyframe = cv2.cvtColor(colorframe,cv2.COLOR_RGBA2GRAY)
        cv2.imshow('grey',greyframe)
        cv2.waitKey(0)

        ColorMin = (100,100,100)
        ColorMax = (255,255,255)
        HSVMin = (5,0,100)
        HSVMax = (110,80,255)


        colorframe= cv2.cvtColor(colorframe,cv2.COLOR_RGBA2RGB)
        cv2.imshow('colorrgb',colorframe)
        cv2.waitKey(0)
        cv2.imwrite(const.rootfolder+"/rgb.jpg",colorframe)
        hsv= cv2.cvtColor(colorframe,cv2.COLOR_RGB2HSV)
        hue = hsv[:,:,0]
        sat = hsv[:,:,1]
        val = hsv[:,:,2]
        cv2.imshow('hsv',hsv)
        cv2.waitKey(0)

        cv2.imshow('hue',hue)
        cv2.waitKey(0)
        cv2.imwrite(const.rootfolder+"/hue.jpg",hue)
        cv2.imshow('sat',sat)
        cv2.waitKey(0)
        cv2.imwrite(const.rootfolder+"/sat.jpg",sat)
        cv2.imshow('val',val)
        cv2.waitKey(0)
        cv2.imwrite(const.rootfolder+"/val.jpg",val)

        #Sets pixels to white if in purple range, else will be set to black
        mask = cv2.inRange(hsv, HSVMin, HSVMax)
        maskcolor= cv2.inRange(colorframe,ColorMin,ColorMax)
        cv2.imshow('mask',mask)
        cv2.waitKey(0)
        cv2.imshow('maskcolor',maskcolor)
        cv2.waitKey(0)

        # Bitwise-AND of mask and purple only image - only used for display
        #colorframe = cv2.bitwise_and(colorframe, colorframe, mask= mask)
        fullmask= cv2.bitwise_and(mask,maskcolor)
        
        fullmask =cv2.GaussianBlur(mask,(3,3),0)
        fullmask = cv2.dilate(mask, None, iterations=1)
        cv2.imshow('fullmask',fullmask)
        cv2.waitKey(0)
        reversemask=255-fullmask
        cv2.imshow('reversemask',reversemask)
        cv2.waitKey(0)
        # Detect blobs.
        keypoints = self.detector.detect(reversemask)


        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
        # the size of the circle corresponds to the size of blob

        im_with_keypoints = cv2.drawKeypoints(colorframe, keypoints, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        #colorframe = cv2.bitwise_and(colorframe,im_with_keypoints)

        return im_with_keypoints

    



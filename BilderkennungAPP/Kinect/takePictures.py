import cv2
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import const
import time

def ir_frame_to_jpg(IRFrame):
    IRFrame = IRFrame.reshape((const.ir_image_size))
    IRFrame = np.uint8(IRFrame/256)
    jpgIRFrame = np.zeros((const.ir_image_size[0],const.ir_image_size[1],3), np.uint8)
    jpgIRFrame[:,:,0]  =  IRFrame
    jpgIRFrame[:,:,1]  =  IRFrame
    jpgIRFrame[:,:,2]  =  IRFrame
    return jpgIRFrame


def takePicture():
    kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color |
                                             PyKinectV2.FrameSourceTypes_Infrared |
                                         PyKinectV2.FrameSourceTypes_Depth)
    i = 0
    redAlert = np.zeros((const.ir_image_size[0],const.ir_image_size[1],3),np.uint8)
    redAlert[:,:,2] = 255
    #cv2.namedWindow('IR', cv2.WINDOW_NORMAL)
    while(i<const.numberofCalibrations):
       
        
        while(cv2.waitKey(1) != 27):#wait ESC press
            cv2.imshow('IR',ir_frame_to_jpg(kinect.get_last_infrared_frame()))

        #save data
        cv2.imshow('IR',redAlert)
        cv2.waitKey(1)

        
        IRFrame = kinect.get_last_infrared_frame()
        jpgIRFrame = ir_frame_to_jpg(IRFrame)
        irFilePath = const.irFolder + str(i) + '.jpg'
        

        colorFrame = kinect.get_last_color_frame()
        colorFrame = colorFrame.reshape((const.rgb_image_size[0],const.rgb_image_size[1],4))
        rgbFilePath = const.rgbFolder + str(i) + '.jpg'
        

        found1, corners = cv2.findChessboardCorners(colorFrame, const.pattern_size, flags=cv2.CALIB_CB_ADAPTIVE_THRESH)
        found2, corners = cv2.findChessboardCorners(jpgIRFrame, const.pattern_size, flags=cv2.CALIB_CB_ADAPTIVE_THRESH)
        if found1 and found2:

            cv2.imwrite(rgbFilePath, colorFrame)
            cv2.imwrite(irFilePath, jpgIRFrame)
            for j in range(0,const.numberOfDepthFramesForDepthCalibration):
                time.sleep(0.03)
                depthFilePath = const.depthFolder + str(i) + '_' + str(j)  + '.npy'
                depthFrame = kinect.get_last_depth_frame()
                depthFrame = depthFrame.reshape(const.ir_image_size)
                np.save(depthFilePath, depthFrame)

            i = i + 1
            print("ok")
        elif not found1:
            print("Dont found chessboard in rgb frame")
        elif not found2:
            print("Dont found chessboard in ir frame")

    cv2.destroyAllWindows()
    print("measure distance to ground at middele Coordinate")
    while(cv2.waitKey(1) != 27):#wait ESC press
        frame = ir_frame_to_jpg(kinect.get_last_infrared_frame())
        frame[212,256,2] =255
        cv2.imshow('IR',frame)

        #save data
    cv2.imshow('IR',redAlert)
    cv2.waitKey(1)
    DepthFrameMiddle = np.zeros((const.numberofCalibrations),dtype="uint16")
    i=0
    while(i<const.numberofCalibrations):
        DepthFrame = kinect.get_last_depth_frame()
        DepthFrame = DepthFrame.reshape(424,512)
        DepthFrameMiddle[i]=DepthFrame[212,256]
        i+=1
    DistancetoGround=np.mean(DepthFrameMiddle)
    np.save(const.rootfolder+"/distancetoground.npy",DistancetoGround)
    cv2.destroyAllWindows()





















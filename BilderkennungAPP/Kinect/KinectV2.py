import numpy as np
import pykinect2.PyKinectRuntime as PKR
import pykinect2.PyKinectV2 as PKV
import cv2
import os
import time
import const
import shelve

class KinectV2(object):

    def __init__(self):
        self.kinect = PKR.PyKinectRuntime(PKV.FrameSourceTypes_Color | PKV.FrameSourceTypes_Depth)

        #load calibration results
        self.rgbCamera = shelve.open(const.rgbCameraIntrinsic+"/RGB")
        self.rgb_Fx = self.rgbCamera['camera_matrix'][0,0]
        self.rgb_Fy = self.rgbCamera['camera_matrix'][1,1]
        self.rgb_Cx = self.rgbCamera['camera_matrix'][0,2]
        self.rgb_Cy = self.rgbCamera['camera_matrix'][1,2]

        self.irCamera = shelve.open(const.irCameraIntrinsic+"/IR")
        self.depth_Fx = self.irCamera['camera_matrix'][0,0]
        self.depth_Fy = self.irCamera['camera_matrix'][1,1]
        self.depth_Cx = self.irCamera['camera_matrix'][0,2]
        self.depth_Cy = self.irCamera['camera_matrix'][1,2]

        self.stereoCamera = shelve.open(const.rgbToIR+"/rgbToIR")
        distanceFile = shelve.open(const.distanceErrorFunction+"/distanceError")
        self.depthErrorFunction = dict(zip(distanceFile['x'], distanceFile['y']))

        self.numberOfPicture = 0

    def close(self):
        self.kinect.close()


    def takePicture(self):
        #get frames from Kinect
        framedone=False
        while not framedone:
            if self.kinect.has_new_depth_frame() and self.kinect.has_new_color_frame(): 
                depthFrame = self.kinect.get_last_depth_frame()
                colorFrame = self.kinect.get_last_color_frame()
                framedone=True;
        
                   
                   
        

        #reshape to 2-D space
        colorFrame = colorFrame.reshape((const.rgb_image_size[0],const.rgb_image_size[1],4))
        depthFrame = depthFrame.reshape(const.ir_image_size)

        #compensate  lens distortion
        colorFrame = cv2.undistort(colorFrame,self.rgbCamera['camera_matrix'], self.rgbCamera['dist_coefs'])
        depthFrame = cv2.undistort(depthFrame,self.irCamera['camera_matrix'], self.irCamera['dist_coefs'])

        #combine depth, RGB and bodyIndexFrame
        combinedImage,worldCoordinates = self.__align__(colorFrame,depthFrame)

        #self.__saveData__(colorFrame, depthFrame.reshape(const.ir_image_size), combinedImage)
        self.numberOfPicture = self.numberOfPicture + 1

        return combinedImage,worldCoordinates

    def newExperiment(self, folderName=[]):
        if not folderName:
            folderName = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
        self.folderName = const.pictureFolder + folderName + '/'
        if not os.path.exists(self.folderName):
            os.makedirs(self.folderName)
        self.numberOfPicture = 1


    def __saveData__(self,colorFrame, depthArray, combinedImage):
        cv2.imwrite(self.folderName + str(self.numberOfPicture) + '_rgb.jpg',colorFrame)
        cv2.imwrite(self.folderName + str(self.numberOfPicture) + '_combined.jpg',combinedImage)
        depthArray.tofile(self.folderName + str(self.numberOfPicture) + '_depth.dat')

    #colorize depth frame
    def __align__(self,colorFrame,depthFrame):
        combinedImage = np.zeros((const.ir_image_size[0],const.ir_image_size[1],3))
        depthFrame = depthFrame/1000 #from mm to meters

        # From Depth Map to Point Cloud
        #book "Hacking the Kinect" by Jeff Kramer P. 130, 
        worldCoordinates = np.zeros((np.prod(const.ir_image_size),3))
        i = 0
        for depthX in range(1,depthFrame.shape[1]):
            for depthY in range(1, depthFrame.shape[0]):
                z = depthFrame[depthY,depthX]
                if (z > 0):
                    worldCoordinates[i,0] = z*(depthX-self.depth_Cx)/self.depth_Fx #x
                    worldCoordinates[i,1] = z*(depthY-self.depth_Cy)/self.depth_Fy #y
                    worldCoordinates[i,2] = z #z
                i = i + 1

        #Projecting onto the Color Image Plane, Hacking the Kinect, P. 132
        worldCoordinates = np.dot(worldCoordinates, self.stereoCamera['R'].T) + self.stereoCamera['T'].T
        rgbX = np.round(worldCoordinates[:,0]*self.rgb_Fx/worldCoordinates[:,2]+self.rgb_Cx)
        rgbY = np.round(worldCoordinates[:,1]*self.rgb_Fy/worldCoordinates[:,2]+self.rgb_Cy)
        rgbX=rgbX.astype(int)
        rgbY=rgbY.astype(int)

        #colorize depth image
        i=0
        for depthX in range(1,depthFrame.shape[1]):
            for depthY in range(1, depthFrame.shape[0]):
                if ((rgbX[i] >= 0) & (rgbX[i] < const.rgb_image_size[1]) & (rgbY[i] >= 0) & (rgbY[i] < const.rgb_image_size[0])):
                    combinedImage[depthY,depthX,0] = colorFrame[rgbY[i],rgbX[i]][0]
                    combinedImage[depthY,depthX,1] = colorFrame[rgbY[i],rgbX[i]][1]
                    combinedImage[depthY,depthX,2]= colorFrame[rgbY[i],rgbX[i]][2]
                i = i + 1

        combinedImage = np.uint8(combinedImage)
        return combinedImage, worldCoordinates







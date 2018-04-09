#Kinect v2 stereo calibration

import numpy as np
import cv2
import shelve
import os
import const
from glob import glob

def getImagePoints(imageNames):
    img_points = []
    for fileName in imageNames:
        filebla = shelve.open(fileName)
        img_points.append(filebla['img_points'])
    return img_points

def stereocalibrate():

    #load img_points
    rgbImages = glob(const.rgbFolder + '*.dat')
    irImages = glob(const.irFolder+ '*.dat')
    rgb_img_points = getImagePoints(rgbImages)
    ir_img_points = getImagePoints(irImages)

    #create object points for all image pairs
    pattern_points = np.zeros((irImages.__len__(),np.prod(const.pattern_size), 3), np.float32)
    pattern_points[:,:, :2] = np.indices(const.pattern_size).T.reshape(-1, 2)
    pattern_points *= const.square_size

    #load calibration results
    rgbCamera = shelve.open(const.rgbCameraIntrinsic+'/RGB')
    irCamera = shelve.open(const.irCameraIntrinsic+'/IR')

    retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F  = cv2.stereoCalibrate(  pattern_points,
                                                                                                        ir_img_points,
                                                                                                        rgb_img_points,
                                                                                                        irCamera['camera_matrix'],
                                                                                                        irCamera['dist_coefs'],
                                                                                                        rgbCamera['camera_matrix'],
                                                                                                        rgbCamera['dist_coefs'],
                                                                                                        const.ir_image_size)

    print("error:"+ str(retval))

    #save calibration results
    camera_file = shelve.open(const.rgbToIR+'/rgbToIR', 'n')
    camera_file['R'] = R
    camera_file['T'] = T
    camera_file.close()
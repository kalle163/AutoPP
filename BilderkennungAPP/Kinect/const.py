
rootfolder ='D:/Bilderkennung'
rgbFolder = 'D:/Bilderkennung/RGB/'
irFolder = 'D:/Bilderkennung/IR/'
depthFolder = 'D:/Bilderkennung/Depth/'
rgbCameraIntrinsic = 'D:/Bilderkennung/CalibrationResults'
irCameraIntrinsic = 'D:/Bilderkennung/CalibrationResults'
distanceErrorFunction = 'D:/Bilderkennung/CalibrationResults'
pictureFolder = 'D:/KinectData/'
square_size = 0.0618 #metres
pattern_size = (7, 5) #inner coners all coners black on black normal chessboard has 7x5 inner coners 
rgbToIR = 'D:/Bilderkennung/CalibrationResults'
ir_image_size = (424,512)
rgb_image_size = (1920,1080)
indexForBackground = 255
numberOfDepthFramesForDepthCalibration = 100
numberOfDistanceForDepthCalibration = 25
numberofCalibrations = 10
distancefirstobjecttofloor = 150    # in mm
distanceobjecttoobject=  60        # in mm 
NoDetectionArea = [[0,280,512,424-280],[430,120,512-430,424-120],[0,0,120,424]]  # for depth detection in pixel [x,y,width,height] [0,0] = top left corner
fovofkinectv2depth =(60,70.6)  #in degree
fovofkinectv2rgb=(53.8,84.1)   #in degree
screenresolution =(1920,1080)

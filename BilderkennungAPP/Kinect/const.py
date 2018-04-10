
rootfolder ='D:/Chessboard'
rgbFolder = 'D:/Chessboard/RGB/'
irFolder = 'D:/Chessboard/IR/'
depthFolder = 'D:/Chessboard/Depth/'
rgbCameraIntrinsic = 'D:/Chessboard/CalibrationResults'
irCameraIntrinsic = 'D:/Chessboard/CalibrationResults'
distanceErrorFunction = 'D:/Chessboard/CalibrationResults'
pictureFolder = 'D:/KinectData/'
square_size = 0.071 #metres
pattern_size = (7, 5) #inner coners all coners black on black normal chessboard has 7x7 inner coners 
rgbToIR = 'D:/Chessboard/CalibrationResults'
ir_image_size = (424,512)
rgb_image_size = (1080,1920)
indexForBackground = 255
numberOfDepthFramesForDepthCalibration = 100
numberOfDistanceForDepthCalibration = 25
numberofCalibrations = 10
distancefirstobjecttofloor = 270    # in mm
distanceobjecttoobject=  50        # in mm 
NoDetectionArea = [[0,280,512,424-280],[330,120,512-330,424-120],[0,0,120,424]]  # for depth detection in pixel [x,y,width,height] [0,0] = top left corner

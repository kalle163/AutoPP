from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from .Bildverarbeitung import *
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from cameraCV import *
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.clock import Clock
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import Kinect.takePictures as tp
import Kinect.calibrate as cal
import Kinect.const as const
import Kinect.stereoCalibrate as sc
import Kinect.depthCalibration as dc
import shutil
import os
from XMLIO import *
from Kinect.KinectV2 import *
from Blob import *

def ChangeSavePathInConst(path,deletestate):
    if deletestate == 'down':
        if os.path.exists(const.rootfolder):
            shutil.rmtree(const.rootfolder,ignore_errors=True)
    newpath=path+"/Chessboard"
    const.rootfolder = newpath
    const.irFolder =newpath+"/IR/"
    const.rgbFolder= newpath+"/RGB/"
    const.depthFolder=newpath+"/Depth/"
    resultpath= path+"/CalibrationResults"
    const.rgbCameraIntrinsic = resultpath
    const.rgbToIR = resultpath
    const.irCameraIntrinsic = resultpath
    const.distanceErrorFunction= resultpath
    const.pictureFolder= path+"/KincetData/"



class MyPopup(Popup):
    def ChangeSavePath(self,path,deletestate):
        print(path)
        ChangeSavePathInConst(path,deletestate)

class Bildschirm(Widget):
    texture = ObjectProperty(None)
    def Changetexture(self,texture):
        self.texture=texture

class NumericInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        if not from_undo:
            try:
                int(substring)
            except ValueError:
                return
        super(NumericInput, self).insert_text(substring, from_undo)
 

class MyPanel(Screen):
    bg = ListProperty([.27, .64, .25, 1])
    posrec =list([200,100])
    abstandzumboden=3500
    def __init__(self, **kwargs):
        super(MyPanel, self).__init__(**kwargs)
        self.cam =CameraPyKinectCV()
        self.workpic =Bildverarbeitung()
        self.kinect=KinectV2()
        self.blob = Blob()
        self.XMLWriter = XMLWriter()
        self.XMLReader = XMLReader()
        print(self.pos)       
    def GreyBildpressed(self):
        print("pressed")
        combinedframe,worldCoordinates=self.kinect.takePicture()
        texture=self.workpic.DetphFrameToKivyPicture(combinedframe)
        worldCoordinates=worldCoordinates.reshape(const.ir_image_size[0],const.ir_image_size[1],3)
        self.bildschirm.Changetexture(texture)
    def RGBBildpressed(self):
        print("pressed2")
        frame=self.cam.getpicturecolor()
        framewithblob= self.blob.blobdetection(frame) 
        texture=self.workpic.ColorFrameToKivyPicture(framewithblob)
        self.bildschirm.Changetexture(texture)
    def on_text(self,*args):
            self.abstandzumboden=int(args[1])
    def Calibratepressed(self):
        self.calibrate()
    def HeightMapPressed(self):
        framemilli,framegrey = self.cam.getpicturedepth(3500.0)
        texturegrey=self.workpic.DetphFrameToKivyPicture(framegrey)
        self.bildschirm.Changetexture(texturegrey)
        self.workpic.DetectionOfDepthObjects(framemilli,framegrey)
    def neuenOrdneranlegen(newpath):
        if not os.path.exists(newpath):
            os.makedirs(newpath)
    def WriteOutputPressed(self):
        print("write")
    def calibrate(self):
        if os.path.exists(const.rootfolder):
            #shutil.rmtree(const.rootfolder,ignore_errors=True)
            pass

        #neuenOrdneranlegen(const.depthFolder)
        #neuenOrdneranlegen(const.rgbFolder)
        #neuenOrdneranlegen(const.rgbCameraIntrinsic)
        #neuenOrdneranlegen(const.irFolder)
        #tp.takePicture()
        #cal.calibrate(isRGB=True)
        #cal.calibrate(isRGB=False)
        #sc.stereocalibrate()
        #dc.DepthCalibration()        

  

class MyPanelApp(App):
    def build(self):
        return MyPanel()


   
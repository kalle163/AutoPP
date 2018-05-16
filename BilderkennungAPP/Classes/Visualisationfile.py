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
from Blob import *
from _2DImageTo3DCoords import *
from Simple2DImageto3DCoords import *

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

def neuenOrdneranlegen(newpath):
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return


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
    listofblobobjects=list()
    listofdetecteddepthobjects=list()
    listofkeypoints=list();
    def __init__(self, **kwargs):
        super(MyPanel, self).__init__(**kwargs)
        if not os.path.exists(const.rootfolder):
           neuenOrdneranlegen(const.rootfolder)
        if not os.path.exists(const.rootfolder+"/distancetoground.npy"):
            self.calibrate()
        self.cam =CameraPyKinectCV()
        self.workpic =Bildverarbeitung()
        self.XMLWriter = XMLWriter()
        self.XMLReader = XMLReader()
        framemilli,framegrey,self.g = self.cam.getpicturedepth()
        self.XMLReader.readinputfile(const.rootfolder+"/Input.xml")
        self.listofblobobjects=self.XMLReader.getlistofblobobjects()
        self.blob =Blob(self.listofblobobjects)
        self.imageto3D = Simple2DImageto3DCoords() 
     
        return
    def GreyBildpressed(self):
        combinedframe,worldCoordinates=self.kinect.takePicture()
        texture=self.workpic.DetphFrameToKivyPicture(combinedframe)
        worldCoordinates=worldCoordinates.reshape(const.ir_image_size[0],const.ir_image_size[1],3)
        self.bildschirm.Changetexture(texture)
        return

    def RGBBildpressed(self):
        frame=self.cam.getpicturecolor()
        if len(self.listofblobobjects)>0:
            if self.showcheckbox.state =='down':
                show=True
            else:
                show=False
            if self.savecheckbox.state == 'down':
                save=True
            else:
                save=False
            framewithblob,self.listofkeypoints= self.blob.blobdetection(frame,show,save) 
            texture=self.workpic.ColorFrameToKivyPicture(framewithblob)
        else:
            print("There are no Blob objects defined. Define at leat one"+ 
            "Blob Object in input.xml-File and press -Read Input.xml- Button")
            frame= cv2.cvtColor(frame,cv2.COLOR_BGRA2BGR)
            texture=self.workpic.ColorFrameToKivyPicture(frame)
        self.bildschirm.Changetexture(texture)
        framemilli,framegrey,waste = self.cam.getpicturedepth()
        del waste, framegrey
        self.imageto3D.ConvertBalltoCoords(self.listofkeypoints,self.XMLWriter,framemilli)
        return

    def Calibratepressed(self):       
        self.calibrate()
        return
    def HeightMapPressed(self):
        self.listofdetecteddepthobjects = list()
        framemilli,framegrey,self.g = self.cam.getpicturedepth()
        texturegrey=self.workpic.DetphFrameToKivyPicture(framegrey)
        self.bildschirm.Changetexture(texturegrey)
        self.listofdetecteddepthobjects = self.workpic.DetectionOfDepthObjects(framemilli,framegrey,self.g)
        self.imageto3D.ConvertPixQuadertoCoordQuader(self.listofdetecteddepthobjects,self.XMLWriter)
        return
    def WriteOutputPressed(self):
        self.XMLWriter.WriteToXML(const.rootfolder+"/Output.xml")
        return
    def ReadInputPressed(self):
        self.XMLReader.readinputfile(const.rootfolder+"/Input.xml")
        self.listofblobobjects=self.XMLReader.getlistofblobobjects()
        del self.blob
        self.blob=Blob(self.listofblobobjects)
        return
    def calibrate(self):
        tp.takedepth()        
       
  

class MyPanelApp(App):
    def build(self):
        return MyPanel()


   
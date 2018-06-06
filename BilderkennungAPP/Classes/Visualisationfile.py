from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from .Bildverarbeitung import *
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.factory import Factory
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
from man2DImageto3DCoords import *
from SimpleCalibration import *
from SimpleIRCalibration import *
import shelve
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

class MyCaliPopup(Popup):
    def __init__(self, **kwargs):
        self.simcal = SimpleCalibrator()
        self.init = False
        return super(MyCaliPopup, self).__init__(**kwargs)

    def ResetPicture(self):
        if self.checkbox.state == 'down':
            chessboard= True
        else:
            chessboard = False
        self.simcal.takePicture(chessboard)
        self._GetActualValues_()
        texture=self.simcal.PictureWithCross(self.rotvalue,self.xvalue,self.yvalue)
        self.bildschirm.Changetexture(texture)
        self.resetpic.text = "Reset Picture"
        self.init = True
        return
    def SaveCalibration(self):
        if self.checkbox.state == 'down':
            areaofinterest = self.simcal.find_points(self.rotvalue)
            if self.checkbox2.state == 'down':
                self.areaofinterest = areaofinterest
            else:
                self.areaofinterest = 0
            if self.checkbox3.state  == 'down':
                self.xyratio,self.xvalue,self.yvalue  = self.simcal.Distortion(self.xvalue,self.yvalue)
                self.areaofinterest = self.simcal.find_points(self.rotvalue)
                self.xlenperpix,self.ylenperpix = self.simcal.Exit()
            else:
                self.xlenperpix = 0
                self.ylenperpix = 0
            self._SaveResults_()
            self.dismiss()
        return
    def ChessboardChange(self):
        if self.checkbox.state == 'down':
            pass
        else:
            self.checkbox2.state = 'normal'
            self.checkbox3.state = 'normal'
    def OnTouchMove(self):
        if self.init:
            self._SetSilderToNumeric_()
            self._RefreshPicture_()
        return
    def NumericChange(self):
        if self.init:
            self._SetNumericToSlider_()
            self._RefreshPicture_()
        return
    def _GetActualValues_(self):
        x = int(self.sliderhor.value)
        y = int(self.sliderver.value)
        rot = int(self.sliderrot.value)
        y=1079-y
        self.xvalue=x
        self.yvalue=y
        self.rotvalue=rot
        return
    def _RefreshPicture_(self):
        self._GetActualValues_()
        texture=self.simcal.PictureWithCross(self.rotvalue,self.xvalue,self.yvalue)
        self.bildschirm.Changetexture(texture)
        return
    def _SetSilderToNumeric_(self):
        x = int(self.sliderhor.value)
        y = int(self.sliderver.value)
        rot = int(self.sliderrot.value)
        y=1079-y
        self.numerichor.text=str(x)
        self.numericver.text=str(y)
        self.numericrot.text=str(rot)
        return
    def _SetNumericToSlider_(self):
        x = int(self.numerichor.text)
        y = int(self.numericver.text)
        rot = int(self.numericrot.text)
        y=1079-y
        if x > 1920-32:
            x=1920-32
        if x < 31:
            x=31
        if y > 1080-32:
            x=1080-32
        if y < 31:
            y=31
        if rot > 359:
            rot=359
        if rot < 0:
            rot=0
        self.sliderhor.value=x
        self.sliderver.value=y
        self.sliderrot.value=rot
        return
    def _SaveResults_(self):
        caliresult = shelve.open(const.rootfolder+"\CalibrationResults", 'n')
        caliresult['areaofinterest'] = self.areaofinterest
        caliresult['rotation'] =  self.rotvalue
        caliresult['pointzero'] = np.array([self.xvalue,self.yvalue])
        caliresult['lenperpix'] =np.array([self.xlenperpix,self.ylenperpix])
        caliresult['xyratio'] = self.xyratio
        caliresult.close()

        return

class MyIRCaliPopup(Popup):
    def __init__(self, **kwargs):
        self.simcal = SimpleIRCalibrator()
        self.init = False
        return super(MyIRCaliPopup, self).__init__(**kwargs)

    def ResetPicture(self):
        if self.checkbox.state == 'down':
            chessboard= True
        else:
            chessboard = False
        self.simcal.takePicture(chessboard)
        self._GetActualValues_()
        texture=self.simcal.PictureWithCross(self.rotvalue,self.xvalue,self.yvalue)
        self.bildschirm.Changetexture(texture)
        self.resetpic.text = "Reset Picture"
        self.init = True
        return
    def SaveCalibration(self):
        if self.checkbox.state == 'down':
            areaofinterest = self.simcal.find_points(self.rotvalue)
            if self.checkbox2.state == 'down':
                self.areaofinterest = areaofinterest
            else:
                self.areaofinterest = 0
            if self.checkbox3.state  == 'down':
                self.xyratio,self.xvalue,self.yvalue  = self.simcal.Distortion(self.xvalue,self.yvalue)
                self.areaofinterest = self.simcal.find_points(self.rotvalue)
                self.xlenperpix,self.ylenperpix = self.simcal.Exit()
            else:
                self.xlenperpix = 0
                self.ylenperpix = 0
            self.depth = self.simcal.takedepth(self.xvalue,self.yvalue,self.rotvalue)
            self._SaveResults_()
            self._CalculateIRtoRGB_()
            self.dismiss()
        return
    def ChessboardChange(self):
        if self.checkbox.state == 'down':
            pass
        else:
            self.checkbox2.state = 'normal'
            self.checkbox3.state = 'normal'
    def OnTouchMove(self):
        if self.init:
            self._SetSilderToNumeric_()
            self._RefreshPicture_()
        return
    def NumericChange(self):
        if self.init:
            self._SetNumericToSlider_()
            self._RefreshPicture_()
        return
    def _GetActualValues_(self):
        x = int(self.sliderhor.value)
        y = int(self.sliderver.value)
        rot = int(self.sliderrot.value)
        y=423-y
        self.xvalue=x
        self.yvalue=y
        self.rotvalue=rot
        return
    def _RefreshPicture_(self):
        self._GetActualValues_()
        texture=self.simcal.PictureWithCross(self.rotvalue,self.xvalue,self.yvalue)
        self.bildschirm.Changetexture(texture)
        return
    def _SetSilderToNumeric_(self):
        x = int(self.sliderhor.value)
        y = int(self.sliderver.value)
        rot = int(self.sliderrot.value)
        y=423-y
        self.numerichor.text=str(x)
        self.numericver.text=str(y)
        self.numericrot.text=str(rot)
        return
    def _SetNumericToSlider_(self):
        x = int(self.numerichor.text)
        y = int(self.numericver.text)
        rot = int(self.numericrot.text)
        y=423-y
        if x > 512-32:
            x=512-32
        if x < 31:
            x=31
        if y > 424-32:
            x=424-32
        if y < 31:
            y=31
        if rot > 359:
            rot=359
        if rot < 0:
            rot=0
        self.sliderhor.value=x
        self.sliderver.value=y
        self.sliderrot.value=rot
        return
    def _SaveResults_(self):
        caliresult = shelve.open(const.rootfolder+"\IRCalibrationResults", 'n')
        caliresult['areaofinterest'] = self.areaofinterest
        caliresult['rotation'] =  self.rotvalue
        caliresult['pointzero'] = np.array([self.xvalue,self.yvalue])
        caliresult['lenperpix'] =np.array([self.xlenperpix,self.ylenperpix])
        caliresult['xyratio'] = self.xyratio
        caliresult['depth'] = self.depth 
        caliresult.close()

    def _CalculateIRtoRGB_(self):
        ircaliresult = shelve.open(const.rootfolder+"\IRCalibrationResults")
        caliresult = shelve.open(const.rootfolder+"\CalibrationResults")
        irarea = ircaliresult['areaofinterest'] 
        area = caliresult['areaofinterest'] 
        xtransform = (irarea[1][0]-irarea[0][0])/(area[1][0]-area[0][0])
        irxtransform =1/xtransform
        ytransform = (irarea[2][1]-irarea[0][1])/(area[2][1]-area[0][1])
        irytransform =1/ytransform
        caliresult['transform'] = np.array([xtransform,ytransform])
        ircaliresult['transform'] = np.array([irxtransform,irytransform])
        caliresult.close()
        ircaliresult.close()
        return


        return


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
    listofballkeypoints=list();
    listofquaderkeypoints=list();
    def __init__(self, **kwargs):
        super(MyPanel, self).__init__(**kwargs)
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
            framewithblob,self.listofballkeypoints,self.listofquaderkeypoints= self.blob.blobdetection(frame,show,save) 
            texture=self.workpic.ColorFrameToKivyPicture(framewithblob)
        else:
            print("There are no Blob objects defined. Define at leat one"+ 
            "Blob Object in input.xml-File and press -Read Input.xml- Button")
            frame= cv2.cvtColor(frame,cv2.COLOR_BGRA2BGR)
            texture=self.workpic.ColorFrameToKivyPicture(frame)
        self.bildschirm.Changetexture(texture)
        framemilli,framegrey,waste = self.cam.getpicturedepth()
        del waste, framegrey
        self.imageto3D.load()
        self.imageto3D.ConvertBalltoCoords(self.listofballkeypoints,self.XMLWriter,framemilli)
        self.imageto3D.ConvertQuadertoCoords(self.listofquaderkeypoints,self.XMLWriter,framemilli)
        return
    def HeightMapPressed(self):
        self.listofdetecteddepthobjects = list()
        framemilli,framegrey,self.g = self.cam.getpicturedepth()
        texturegrey=self.workpic.DetphFrameToKivyPicture(framegrey)
        self.bildschirm.Changetexture(texturegrey)
        self.listofdetecteddepthobjects = self.workpic.DetectionOfDepthObjects(framemilli,framegrey,self.g)
        self.imageto3D/load()
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
    def CalibratePressed(self):
        Factory.MyIRCaliPopup().open()
        Factory.MyCaliPopup().open()
  
        return
       


class MyPanelApp(App):
    def build(self):
        return MyPanel()


   
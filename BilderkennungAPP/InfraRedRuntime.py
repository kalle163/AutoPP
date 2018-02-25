import numpy as np
import cv2
import openni

import pykinect2.PyKinectRuntime as PKR
import pykinect2.PyKinectV2 as PKV
import pygame

import ctypes
import _ctypes
import sys


class InfraRedRuntime(object):
    def __init__(self):
        pygame.init();
        # Used to manage how fast the screen updates

        self._clock = pygame.time.Clock()



        # Loop until the user clicks the close button.

        self._done = False



        # Used to manage how fast the screen updates

        self._clock = pygame.time.Clock()



        # Kinect runtime object, we want only color and body frames 
       

        self._kinect =  PKR.PyKinectRuntime(PKV.FrameSourceTypes_Color | PKV.FrameSourceTypes_Depth)
      
        # back buffer surface for getting Kinect infrared frames, 8bit grey, width and height equal to the Kinect color frame size

        self._frame_surface = pygame.Surface((self._kinect.depth_frame_desc.Width, self._kinect.depth_frame_desc.Height), 0, 32)

        # here we will store skeleton data 

        self._bodies = None

        

        # Set the width and height of the screen [width, height]

        self._infoObject = pygame.display.Info()

        self._screen = pygame.display.set_mode((self._kinect.depth_frame_desc.Width, self._kinect.depth_frame_desc.Height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)



        pygame.display.set_caption("Kinect for Windows v2 Infrared")

    
    def draw_color_frame(self, frame, target_surface):

        if frame is None:  # some usb hub do not provide the infrared image. it works with Kinect studio though

            return
        
        target_surface.lock()
        
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
            
        del address
            
        target_surface.unlock()

        


            
    def run(self):              

        while not self._done:

            for event in pygame.event.get(): # User did something

                 if event.type == pygame.QUIT: # If user clicked close
                         
                     self._done = True # Flag that we are done so we exit this loop
                 elif event.type == pygame.VIDEORESIZE: # window resized

                     self._screen = pygame.display.set_mode(event.dict['size'], 

                     pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
                   

            # --- Getting frames and drawing  
            
           # if self._kinect.has_new_color_frame():

            #    frame = self._kinect.get_last_color_frame()

             #   self.draw_color_frame(frame, self._frame_surface)

              #  frame = None
            
            if self._kinect.has_new_depth_frame():

                frame = self._kinect.get_last_depth_frame()

                self.draw_color_frame(frame, self._frame_surface)

                frame = None

            self._screen.blit(self._frame_surface, (0,0))

            pygame.display.update()



            # --- Go ahead and update the screen with what we've drawn.

            pygame.display.flip()



            # --- Limit to 60 frames per second

            self._clock.tick(60)



        # Close our Kinect sensor, close the window and quit.

        self._kinect.close()

        pygame.quit()

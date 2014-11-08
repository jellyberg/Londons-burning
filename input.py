# London's burning
# a game by Adam Binks

import pygame, sys
from pygame.locals import *

class Input:
    """A class to handle input accessible by all other classes"""
    constrainMouseMargin = 30
    def __init__(self):
        self.pressedKeys = []
        self.mousePressed = False
        self.mouseUnpressed = False
        self.mousePos = [0, 0]
        

    def get(self, constrainMouse=False):
        """Update variables - mouse position and click state, and pressed keys"""
        self.mouseUnpressed = False
        self.unpressedKeys = []
        self.justPressedKeys = []

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key not in self.pressedKeys:
                    self.justPressedKeys.append(event.key)
                self.pressedKeys.append(event.key)
            elif event.type == KEYUP:
                for key in self.pressedKeys:
                    if event.key == key:
                        self.pressedKeys.remove(key)
                    self.unpressedKeys.append(key)
            elif event.type == MOUSEMOTION:
                self.mousePos = list(event.pos)
            elif event.type == MOUSEBUTTONDOWN:
                self.mousePressed = event.button
                self.mouseUnpressed = False
            elif event.type == MOUSEBUTTONUP:
                self.mousePressed = False
                self.mouseUnpressed = event.button
            elif event.type == QUIT:
                pygame.event.post(event)

        if constrainMouse:
            self.constrainMouse()
        self.checkForQuit()


    def constrainMouse(self):
        """Set the cursor position to a little inside the edge of the window if it goes outside it"""
        for axis in [0, 1]:
            if self.mousePos[axis] < Input.constrainMouseMargin:
                self.mousePos[axis] = Input.constrainMouseMargin
            if self.mousePos[axis] > Input.winSize[axis] - Input.constrainMouseMargin:
                self.mousePos[axis] = Input.winSize[axis] - Input.constrainMouseMargin
        pygame.mouse.set_pos(self.mousePos)



    def checkForQuit(self):
        """Terminate if QUIT events"""
        for event in pygame.event.get(QUIT): # get all the QUIT events
            self.terminate() # terminate if any QUIT events are present
        if K_ESCAPE in self.unpressedKeys:
            self.terminate()


    def terminate(self):
        """Safely end the program"""
        pygame.quit()
        sys.exit()
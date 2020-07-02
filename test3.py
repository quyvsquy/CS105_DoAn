from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
from pyopengltk import OpenGLFrame
from initialization import Init_Global_Para
from tkinter import *

class Draw(Init_Global_Para, OpenGLFrame):
    def __init__(self, shapeObject, isTexture=False, isLighting=-1, typeDraw='face', *args, **kw):
        Init_Global_Para.__init__(self, typeDraw=typeDraw)
        OpenGLFrame.__init__(self, *args, **kw)
        self.object = shapeObject

        ### Begin APHIN ###
        self.aphinType = -1 # 0 is Scale; 1 is Rotate; 2 is Translate
        self.varScale = (DoubleVar(), DoubleVar(), DoubleVar())
        for rate in self.varScale:
            rate.set(1)
        self.mouse = (0.0, 0.0)
        self.moveR = (0.0, 0.0)
        self.moveT = (0.0, 0.0)
        self.preMoveR = (0.0, 0.0)
        self.preMoveT = (0.0, 0.0)
        self.sizeObject = 0.0
        self.isScaleFirst = 0
        self.isTranslateFirst = 0
        self.isRotateFirst = 0
        self.isLightSourceFist = 0
        self.bind('<Button-1>', self.tkRecordMouse)

        if self.aphinType in range(4):
            self.bind('<B1-Motion>', self.tkAphin)
        ### End APHIN ###

        ### Begin LIGHT ###
        self.toggleLight = isLighting
        self.lightSourceT = (0.0, 0.0)
        self.preLightSourceT = (0.0, 0.0)
        ### End LIGHT ###


    def tkSizeObject(self, event):
        self.sizeObject = math.sqrt(math.pow((event.x - self.mouse[0]), 2)+math.pow((event.y-self.mouse[1]), 2))/170

    def tkRecordMouse(self, event):
        if self.aphinType == 0:
            self.mouse = (event.x, event.y)
        elif self.aphinType == 1:
            self.mouse = (event.x - self.preMoveR[0], event.y + self.preMoveR[1])
        elif self.aphinType == 2:
            self.mouse = (event.x - self.preMoveT[0], event.y + self.preMoveT[1])
        elif self.aphinType == 3:
            self.mouse = (event.x - self.preLightSourceT[0], event.y + self.preLightSourceT[1])

        
    def v3distsq(self, a, b):
        d = (a[0] - b[0], a[1] - b[1], a[2] - b[2])
        return d[0] * d[0] + d[1] * d[1] + d[2] * d[2]

    def tkAphin(self, event):
        win_height = max(1, self.winfo_height())
        obj_c = (self.centerX.get(), self.centerY.get(), self.centerZ.get())
        win = gluProject(*obj_c)
        obj = gluUnProject(win[0], win[1] + 0.5 * win_height, win[2])
        dist = math.sqrt(self.v3distsq(obj, obj_c))
        scale = abs(dist / (0.5 * win_height))
        tempX = event.x - self.mouse[0]
        tempY = self.mouse[1] - event.y
        if self.aphinType == 1:
            self.moveR =  (tempX/6, tempY/6)
            self.preMoveR = (tempX, tempY)
        elif self.aphinType == 2:
            self.moveT =  (tempX * scale, tempY * scale)
            self.preMoveT = (tempX, tempY)
        elif self.aphinType == 3:
            self.lightSourceT =  (tempX * scale, tempY * scale)
            self.preLightSourceT = (tempX, tempY)

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        glColor3fv(self.color/255)
        if self.aphinType == 3:
            self.lightPosX, self.lightPosY = self.lightSourceT[0], self.lightSourceT[1]
        self.drawLight()
        self.drawTexture()
        glLoadIdentity()
        self.displayEye()
        glPushMatrix()

        if self.aphinType == 0:
            glScale(self.varScale[0].get(), self.varScale[1].get(), self.varScale[2].get())
            if self.isTranslateFirst:
                glTranslatef(self.moveT[0] , self.moveT[1], 0.0)
            if self.isRotateFirst:
                glRotatef(self.moveR[1], 1, 0, 0)
                glRotatef(self.moveR[0], 0, 1, 0)
            if self.isLightSourceFist:
                self.lightPosX, self.lightPosY = self.lightSourceT[0], self.lightSourceT[1]
        elif self.aphinType == 1:
            if self.isScaleFirst:
                glScale(self.varScale[0].get(), self.varScale[1].get(), self.varScale[2].get())
            if self.isTranslateFirst:
                glTranslatef(self.moveT[0] , self.moveT[1], 0.0)
            glRotatef(self.moveR[1], 1, 0, 0)
            glRotatef(self.moveR[0], 0, 1, 0)
            if self.isLightSourceFist:
                self.lightPosX, self.lightPosY = self.lightSourceT[0], self.lightSourceT[1]
        elif self.aphinType == 2:
            if self.isScaleFirst:
                glScale(self.varScale[0].get(), self.varScale[1].get(), self.varScale[2].get())
            glTranslatef(self.moveT[0] , self.moveT[1], 0.0)
            if self.isRotateFirst:
                glRotatef(self.moveR[1], 1, 0, 0)
                glRotatef(self.moveR[0], 0, 1, 0)
            if self.isLightSourceFist:
                self.lightPosX, self.lightPosY = self.lightSourceT[0], self.lightSourceT[1]
        elif self.aphinType == 3:
            if self.isScaleFirst:
                glScale(self.varScale[0].get(), self.varScale[1].get(), self.varScale[2].get())
            if self.isTranslateFirst:
                glTranslatef(self.moveT[0] , self.moveT[1], 0.0)
            if self.isRotateFirst:
                glRotatef(self.moveR[1], 1, 0, 0)
                glRotatef(self.moveR[0], 0, 1, 0)   
            self.lightPosX, self.lightPosY = self.lightSourceT[0], self.lightSourceT[1]

        if self.toggleRotating != -1:
            glRotatef(self.rotAngle, 1.0, 1.0, 1.0)
            self.rotAngle += 0.25
            
        if self.object == 'cube':
            self.make_cube(self.sizeObject * 0.3)
        elif self.object == 'box':
            self.make_box(self.sizeObject, self.sizeObject * 2, self.sizeObject * 1.5)
        elif self.object == 'teapot':
            self.make_teapot(self.sizeObject * 0.3)
        elif self.object == 'sphere':
            self.make_sphere(self.sizeObject * 0.3)  
        elif self.object == 'cylinder':
            self.make_cylinder(self.sizeObject * 0.25, self.sizeObject * 3 * 0.25)
        elif self.object == 'torus':
            self.make_torus(self.sizeObject * 0.1, self.sizeObject * 2 * 0.25)
        elif self.object == 'cone':
            self.make_cone(self.sizeObject * 0.3, self.sizeObject * 2 * 0.3)
        elif self.object == 'pyramid':
            self.make_pyramid(self.sizeObject * 0.4, self.sizeObject * 0.5)
        elif self.object == 'truncated cone':
            self.make_truncatedCone(self.sizeObject * 0.3, self.sizeObject * 0.6, self.sizeObject * 0.6)
        glPopMatrix()
        glFlush()

    def tkResize(self, evt):
        self.width, self.height = evt.width, evt.height
        if self.height > 0:
            self.asp.set(self.width/self.height)
        else: 
            self.asp.set(1)
        if self.winfo_ismapped():
            glViewport(0, 0, self.width, self.height)
            self.initgl()
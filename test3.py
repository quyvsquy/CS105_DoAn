from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image as Pil_image
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

        self.texture = 0 # save texture to draw
        self.bind('<Triple-Button-2>', self.tkReset)

        ### Begin APHIN ###
        self.aphinType = -1 # 0 is Scale; 1 is Rotate; 2 is Translate
        self.varScale = (DoubleVar(), DoubleVar(), DoubleVar())
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
        self.bind('<Button-3>', self.tkSetAphin3)
        ### End LIGHT ###
    
        
    def tkReset(self, event):
        self.aphinType = 4 # 0 is Scale; 1 is Rotate; 2 is Translate
        self.mouse = (0.0, 0.0)
        self.moveR = (0.0, 0.0)
        self.moveT = (0.0, 0.0)
        self.lightSourceT = (0.0, 0.0)
        self.preMoveR = (0.0, 0.0)
        self.preMoveT = (0.0, 0.0)
        self.preLightSourceT = (0.0, 0.0)

    def tkSetAphin1(self, event):
        self.aphinType = 1
        self.isRotateFirst = 1
        self.bind('<B1-Motion>', self.tkAphin)

    def tkSetAphin2(self, event):
        self.aphinType = 2
        self.isTranslateFirst = 1
        self.bind('<B1-Motion>', self.tkAphin)

    def tkSetAphin3(self, event):
        # self.toggleLight = 1 - self.toggleLight
        self.aphinType = 3
        self.bind('<B1-Motion>', self.tkAphin)

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
        obj_c = (self.centerX, self.centerY, self.centerZ)
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
        if self.toggleLight == 1 or self.toggleLight == 2:
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            light_pos = [0.0, 0.0, 1.0, 0.0 ]
            glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
            ambient = [0.0, 0.5, 0.0, 1.0]
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
            diff_use = [0.5, 0.5, 0.0, 1.0]
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diff_use)
            specular =  [ 1.0, 0.0, 0.0, 1.0 ]
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
            shininess = 100
            glMateriali(GL_FRONT, GL_SHININESS, shininess)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        if self.aphinType == 3:
            self.lightPosX, self.lightPosY = self.lightSourceT[0], self.lightSourceT[1]
            print(self.lightPosX, self.lightPosY)
        self.drawLight()
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

        glColor3fv([1, 1, 1])
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
            self.make_torus(self.sizeObject * 0.3, self.sizeObject * 3 * 0.3)
        elif self.object == 'cone':
            self.make_cone(self.sizeObject * 0.3, self.sizeObject * 2 * 0.3)
        # glRotatef(self.rota, 1.0, 1.0, 1.0)
        # self.make_cube(self.sizeObject)
        # self.make_box(self.sizeObject, self.sizeObject*2, self.sizeObject*1.5)
        # self.make_sphere(self.sizeObject)
        # self.make_cone(self.sizeObject, self.sizeObject*3)
        # self.make_cylinder(self.sizeObject, self.sizeObject*3)
        # self.make_torus(self.sizeObject, self.sizeObject*3)
        # self.make_teapot(self.sizeObject)
        # self.make_teapot(2)
        # self.make_truncatedCone(self.sizeObject, self.sizeObject*2, self.sizeObject*2)
        # self.make_pyramid(self.sizeObject*2, self.sizeObject*3)
        self.drawAxes()

        glPopMatrix()
        glFlush()


    def tkResize(self, evt):
        self.width, self.height = evt.width, evt.height
        self.asp =  self.width/self.height if self.height > 0 else 1
        if self.winfo_ismapped():
            glViewport(0, 0, self.width, self.height)
            self.initgl()
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image as Pil_image
import numpy as np
import math
from pyopengltk import OpenGLFrame
from initialization import Init_Global_Para
from tkinter import *

class Draw(Init_Global_Para,OpenGLFrame):
    def __init__(self, shapeObject, isTexture=None, typeDraw='solids',*args, **kw):
        Init_Global_Para.__init__(self, typeDraw=typeDraw)
        OpenGLFrame.__init__(self,*args,**kw)
        self.object = shapeObject

        self.texture = 0 # save texture to draw
        self.bind('<Triple-Button-2>',self.tkReset)

        ### Begin APHIN ###
        self.aphinType = 3 # 0 is Scale; 1 is Rotate; 2 is Translate
        self.varScale = (DoubleVar(), DoubleVar(), DoubleVar())
        self.mouse = (0.0,0.0)
        self.moveR = (0.0,0.0)
        self.moveT = (0.0,0.0)
        self.preMoveR = (0.0,0.0)
        self.preMoveT = (0.0,0.0)
        self.sizeObject = 0.0
        self.isScaleFirst = 0
        self.isTranslateFirst = 0
        self.isRotateFirst = 0
        self.isLightSourceFist = 0
        # self.bind('<Button-2>', self.tkSetAphin1)
        # self.bind('<Double-Button-2>', self.tkSetAphin2)
        self.bind('<Button-1>', self.tkRecordMouse)
        # self.bind('<Shift-B1-Motion>', self.tkSizeObject)

        if self.aphinType in range(4):
            self.bind('<B1-Motion>', self.tkAphin)
        ### End APHIN ###

        ### Begin LIGHT ###
        self.toggleLight = 1
        self.lightSourceT = (0.0,0.0)
        self.preLightSourceT = (0.0,0.0)
        self.bind('<Button-3>', self.tkSetAphin3)
        ### End LIGHT ###
    
        
    def tkReset(self, event):
        self.aphinType = 4 # 0 is Scale; 1 is Rotate; 2 is Translate
        self.mouse = (0.0,0.0)
        self.moveR = (0.0,0.0)
        self.moveT = (0.0,0.0)
        self.lightSourceT = (0.0,0.0)
        self.preMoveR = (0.0,0.0)
        self.preMoveT = (0.0,0.0)
        self.preLightSourceT = (0.0,0.0)

    def tkSetAphin1(self, event):
        self.aphinType = 1
        self.isRotateFirst = 1
        self.bind('<B1-Motion>', self.tkAphin)
        print(self.aphinType)

    def tkSetAphin2(self, event):
        self.aphinType = 2
        self.isTranslateFirst = 1
        self.bind('<B1-Motion>', self.tkAphin)
        print(self.aphinType)

    def tkSetAphin3(self,event):
        # self.toggleLight = 1- self.toggleLight
        self.aphinType = 3
        self.bind('<B1-Motion>', self.tkAphin)
        print(self.aphinType)

    def tkSizeObject(self, event):
        self.sizeObject = math.sqrt(math.pow((event.x - self.mouse[0]),2)+math.pow((event.y-self.mouse[1]),2))/170

    def tkRecordMouse(self, event):
        if self.aphinType == 1:
            self.mouse = (event.x - self.preMoveR[0],event.y + self.preMoveR[1])
        elif self.aphinType == 2:
            self.mouse = (event.x - self.preMoveT[0],event.y + self.preMoveT[1])
        elif self.aphinType == 3:
            self.mouse = (event.x - self.preLightSourceT[0],event.y + self.preLightSourceT[1])
        else:
            self.mouse = (event.x, event.y)
        
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
            self.moveR =  (tempX/6,tempY/6)
            self.preMoveR = (tempX,tempY)
        elif self.aphinType == 2:
            self.moveT =  (tempX * scale,tempY * scale)
            self.preMoveT = (tempX,tempY)
        elif self.aphinType == 3:
            self.lightSourceT =  (tempX * scale,tempY * scale)
            self.preLightSourceT = (tempX,tempY)

    def Init(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        if self.isTexture:
            glEnable(GL_TEXTURE_2D)
            glEnable(GL_LIGHT0) #Cho vào khi auto xoay thì k bị nhiễu
            image = Pil_image.open("./textures/brick.jpg")
            # image = Pil_image.open("./textures/smiley.png")
            self.image = image.transpose(Pil_image.FLIP_TOP_BOTTOM)
            self.img_data = image.convert("RGBA").tobytes()
            self.LoadGLTextures()
        if self.toggleLight:
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

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        if self.aphinType == 3:
            self.lightPosX, self.lightPosY = self.lightSourceT[0],self.lightSourceT[1]
            
        self.drawLight()

        glLoadIdentity()
        # gluLookAt(0.0, 0.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0) #void gluLookAt(GLdouble eyeX,GLdouble eyeY,GLdouble eyeZ,GLdouble centerX,GLdouble centerY,GLdouble centerZ,GLdouble upX,GLdouble upY,GLdouble upZ);
        # gluLookAt(self.eyeX, self.eyeY, self.eyeZ, self.centerX, self.centerY, self.centerZ, self.upX, self.upY, self.upZ) #void gluLookAt(GLdouble eyeX,GLdouble eyeY,GLdouble eyeZ,GLdouble centerX,GLdouble centerY,GLdouble centerZ,GLdouble upX,GLdouble upY,GLdouble upZ);
        self.displayEye()
        glPushMatrix()

        if self.aphinType == 0:
            glScale(self.varScale[0].get(), self.varScale[1].get(), self.varScale[2].get())
            if self.isRotateFirst:
                glRotatef(self.moveR[1], 1, 0, 0)
                glRotatef(self.moveR[0], 0, 1, 0)
            if self.isTranslateFirst:
                glTranslatef(self.moveT[0] , self.moveT[1], 0.0)
            if self.isLightSourceFist:
                self.lightPosX, self.lightPosY = self.lightSourceT[0],self.lightSourceT[1]
        elif self.aphinType == 1:
            if self.isScaleFirst:
                glScale(self.varScale[0].get(), self.varScale[1].get(), self.varScale[2].get())
            glRotatef(self.moveR[1], 1, 0, 0)
            glRotatef(self.moveR[0], 0, 1, 0)
            if self.isTranslateFirst:
                glTranslatef(self.moveT[0] , self.moveT[1], 0.0)
            if self.isLightSourceFist:
                self.lightPosX, self.lightPosY = self.lightSourceT[0],self.lightSourceT[1]
        elif self.aphinType == 2:
            if self.isScaleFirst:
                glScale(self.varScale[0].get(), self.varScale[1].get(), self.varScale[2].get())
            if self.isRotateFirst:
                glRotatef(self.moveR[1], 1, 0, 0)
                glRotatef(self.moveR[0], 0, 1, 0)
            glTranslatef(self.moveT[0] , self.moveT[1], 0.0)
            if self.isLightSourceFist:
                self.lightPosX, self.lightPosY = self.lightSourceT[0],self.lightSourceT[1]
        elif self.aphinType == 3:
            if self.isScaleFirst:
                glScale(self.varScale[0].get(), self.varScale[1].get(), self.varScale[2].get())
            if self.isRotateFirst:
                glRotatef(self.moveR[1], 1, 0, 0)
                glRotatef(self.moveR[0], 0, 1, 0)   
            if self.isTranslateFirst:
                glTranslatef(self.moveT[0] , self.moveT[1], 0.0)
            self.lightPosX, self.lightPosY = self.lightSourceT[0],self.lightSourceT[1]

        if self.object == 'cube':
            self.make_cube(self.sizeObject)
        elif self.object == 'box':
            self.make_box(1, 2, 3)
        elif self.object == 'teapot':
            self.make_teapot(self.sizeObject)
        elif self.object == 'sphere':
            self.make_sphere(self.sizeObject)  

        # glRotatef(self.rota, 1.0, 1.0, 1.0)
        # self.make_cube(self.sizeObject)
        # self.make_box(self.sizeObject,self.sizeObject*2,self.sizeObject*1.5)
        # self.make_sphere(self.sizeObject)
        # self.make_cone(self.sizeObject,self.sizeObject*3)
        # self.make_cylinder(self.sizeObject,self.sizeObject*3)
        # self.make_torus(self.sizeObject,self.sizeObject*3)
        # self.make_teapot(self.sizeObject)
        # self.make_teapot(2)
        # self.make_truncatedCone(self.sizeObject,self.sizeObject*2,self.sizeObject*2)
        # self.make_pyramid(self.sizeObject*2,self.sizeObject*3)
        self.drawAxes()

        # self.PrintAt(5,5,f"View Angle (th, ph) =({self.th}, {self.ph})")
        # self.PrintAt(5,25,f"toggleProjection =({self.toggleProjection})")
        # self.PrintAt(5,45,f"toggleProjection_Perspective =({self.toggleProjection_Perspective})")
        # self.PrintAt(5,65,f"toggleProjection_LookAt_Eye =({self.toggleProjection_LookAt_Eye})")
        # self.PrintAt(5,85,f"toggleProjection__LookAt_Center =({self.toggleProjection__LookAt_Center})")
        # self.PrintAt(5,105,f"toggleProjection__LookAt_Up =({self.toggleProjection__LookAt_Up})")
        glPopMatrix()
        glFlush()


    def tkResize(self,evt):
        self.width, self.height = evt.width, evt.height
        self.asp =  self.width/self.height if self.height > 0 else 1
        if self.winfo_ismapped():
            glViewport(0, 0, self.width, self.height)
            self.initgl()

    # def initgl(self):
    #     self.Init()
    #     glMatrixMode(GL_PROJECTION)
    #     glLoadIdentity()
    #     gluPerspective(self.fov,self.asp,self.zNear,self.zFar) #void gluPerspective(	GLdouble fovy, GLdouble aspect,GLdouble zNear, 	GLdouble zFar);
    #     glMatrixMode(GL_MODELVIEW)
    #     glLoadIdentity()
    
    def LoadGLTextures(self):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.image.width, self.image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.img_data)
        # glBindTexture( GL_TEXTURE_2D, 0 )

    # def SetMaterialColor(self,ambient,diff_use):
    #     glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
    #     glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diff_use)


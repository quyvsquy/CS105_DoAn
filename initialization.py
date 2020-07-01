from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
from shape import drawObject
from PIL import Image
from tkinter import *

class Init_Global_Para(drawObject):
    def __init__(self, typeDraw="face"):
        drawObject.__init__(self)
        self.isTexture = 0
        self.typeDraw = typeDraw # points, lines, face

        ###  TOGGLE DRAW DISPLAYS  ###
        self.toggleAxes = 0
        self.toggleParams = 1


        ###  Begin PROJECTION  ###
        self.toggleProjection = 1 # 0 is off; 1 is on

        # Perspective
        self.toggleProjection_Perspective = 1 # 0 is off; 1 is on
        
        # self.fov = DoubleVar() # field of view for perspective 
        # self.asp = DoubleVar()  # aspect ratio; field of view for perspective
        # self.zNear = DoubleVar() # field of view for perspective
        # self.zFar = DoubleVar() # field of view for perspective
        # print(self.fov)
        # self.fov.set(45) # field of view for perspective 
        # self.asp.set(1)  # aspect ratio;field of view for perspective
        # self.zNear.set(1.0) # field of view for perspective
        # self.zFar.set(100.0) # field of view for perspective

        self.fov = 45 # field of view for perspective 
        self.asp = 1  # aspect ratio;field of view for perspective
        self.zNear = 1 # field of view for perspective
        self.zFar = 100 # field of view for perspective
        
        
        #------------#
        self.toggleProjection_LookAt_Eye = 0 # 0 is off; 1 is on
        self.toggleProjection__LookAt_Center = 0 # 0 is off; 1 is on
        self.toggleProjection__LookAt_Up = 0 # 0 is off; 1 is on
        # can multi choice #
        self.eyeX = DoubleVar()
        self.eyeY = DoubleVar()
        self.eyeZ = DoubleVar()
        self.eyeX.set(0)
        self.eyeY.set(0)
        self.eyeZ.set(10)

        self.centerX = DoubleVar()
        self.centerY = DoubleVar()
        self.centerZ = DoubleVar()
        self.centerX.set(0.0)
        self.centerY.set(0.0)
        self.centerZ.set(0.0)

        self.upX = DoubleVar()
        self.upY = DoubleVar()
        self.upZ = DoubleVar()
        self.upX.set(0.0)
        self.upY.set(1.0)
        self.upZ.set(0.0)
        ###  End PROJECTION  ###

        ###  LIGHTING  ###
        self.toggleLight = -1
        self.lightPosX = 0
        self.lightPosY = 0
        self.ambient = 35
        self.diffuse = 100
        self.emission = 0
        self.specular = 0
        self.shininess = 0
        self.shinyvec = [0,1]
        self.lightY = 0
        self.white = [1,1,1]
        self.lightPh = 90

        ### BEGIN TEXTURES  ###
        self.toggleTextures = -1
        self.imageWHTex = None #Load image with PIL
        self.textureDraw = None
        self.imgDataTex = None
        # self.currentTexture = 0
        ### END TEXTURES  ###

        # ###  ANIMATION  ###
        # self.toggleAnimation = DEF_ANIMATE
        # self.cubeRotation = DEF_CUBE_ROTATION
        ###  EFFECT  ###
        # self.cubeRotation = DEF_CUBE_ROTATION
        self.toggleRotating = -1
        self.rotAngle = 0.0

    def displayInit(self):
        glClearColor(0.0,0.0,0.0,0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glShadeModel(GL_SMOOTH)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

    def displayEye(self):
        gluLookAt(self.eyeX.get(), self.eyeY.get(), self.eyeZ.get(), self.centerX.get(), self.centerY.get(), self.centerZ.get(), self.upX.get(), self.upY.get(), self.upZ.get()) #void gluLookAt(GLdouble eyeX,GLdouble eyeY,GLdouble eyeZ,GLdouble centerX,GLdouble centerY,GLdouble centerZ,GLdouble upX,GLdouble upY,GLdouble upZ);

    def displayReshape(self, evt, width, height): #==tkResize in base.py
        glViewport(0,0, width,height)
        self.displayProject(self.fov, self.asp, self.zNear, self.zFar)

    def displayProject(self, fov, asp, zNear, zFar):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        print(fov)
        gluPerspective(fov, asp, zNear, zFar) #void gluPerspective(	GLdouble fovy, GLdouble aspect,GLdouble zNear, 	GLdouble zFar);
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def initgl(self):
        glutInit()
        self.displayInit()
        self.displayProject(self.fov, self.asp, self.zNear, self.zFar)


    def redisplayAll(self):
        self.displayReshape(1024, 768)
        glutPostRedisplay()

    # def drawAxes(self):
    #     if (self.toggleAxes):
    #         ###  Length of axes ###
    #         len = 5.0
    #         glDisable(GL_LIGHTING)
    #         glBegin(GL_LINES)
    #         glColor3f(1.0, 0.0, 0.0)
    #         glVertex3f(-len, 0.0, 0.0)
    #         glVertex3f(len, 0.0, 0.0)
    #         glEnd()
    #         glBegin(GL_LINES)
    #         glColor3f(0.0, 1.0, 0.0)
    #         glVertex3f(0.0, -len, 0.0)
    #         glVertex3f(0.0, len, 0.0)
    #         glEnd()
    #         glBegin(GL_LINES)
    #         glColor3f(0.0, 0.0, 1.0)
    #         glVertex3f(0.0, 0.0, -len)
    #         glVertex3f(0.0, 0.0, len)
    #         glEnd()
    #         ###  Label axes ###
    #         glColor3fv(self.white)
    #         glRasterPos3d(len,0,0)
    #         glRasterPos3d(0,len,0)
    #         glRasterPos3d(0,0,len)
    #         if self.toggleLight:
    #             glEnable(GL_LIGHTING)

    def drawLight(self):
        ###  Light switch ###
        if self.toggleLight != -1:
            ###  Translate intensity to color vectors ###
            Ambient    =[0.01*self.ambient ,0.01*self.ambient ,0.01*self.ambient ,1.0]
            Diffuse    =[0.01*self.diffuse ,0.01*self.diffuse ,0.01*self.diffuse ,1.0]
            Specular   =[0.01*self.specular,0.01*self.specular,0.01*self.specular,1.0]
            if self.toggleLight == 1:
                Position   = [-10, 10, 5, 1.0]
            else:
                Position  = [self.lightPosX, self.lightPosY, 3.0, 1.0]
            ###  Draw light position as sphere (still no lighting here) ###
            glPushMatrix()
            glColor3fv(self.white)
        
            glDisable(GL_LIGHTING)
            glTranslate(Position[0], Position[1], Position[2])
            glDisable(GL_TEXTURE_2D)
            self.make_light_source_shape()
            glPopMatrix()
            ###  Set ambient, diffuse, specular components and position of light 0 ###
            glLightfv(GL_LIGHT0,GL_AMBIENT, Ambient)
            glLightfv(GL_LIGHT0,GL_DIFFUSE, Diffuse)
            glLightfv(GL_LIGHT0,GL_POSITION,Position)
            # shininess = [100.0]
            # glMaterialfv(GL_FRONT, GL_SHININESS, shininess)
            #########################if (screencastID != 13) {
            glLightfv(GL_LIGHT0,GL_SPECULAR,Specular)
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE)
            #########################}
            glEnable(GL_NORMALIZE)
            glEnable(GL_LIGHTING) 
            glEnable(GL_LIGHT0)
        else:
            glDisable(GL_LIGHTING)

    def drawTexture(self):
        if self.toggleTextures != -1:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textureDraw)
            # Set the texture wrapping parameters
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            # Set texture filtering parameters
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
            glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.imageWHTex[0], self.imageWHTex[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, self.imgDataTex)
        else:
            glDisable(GL_TEXTURE_2D)

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

        self.color = np.array([255, 255, 255])

        ###  Begin PROJECTION  ###
        
        self.fov = DoubleVar() # field of view for perspective 
        self.asp = DoubleVar()  # aspect ratio; field of view for perspective
        self.zNear = DoubleVar() # field of view for perspective
        self.zFar = DoubleVar() # field of view for perspective
        
        self.fov.set(45.0) 
        self.asp.set(1.48) 
        self.zNear.set(1.0) 
        self.zFar.set(100.0)        
        
        self.fov_tmp = DoubleVar() 
        self.asp_tmp = DoubleVar()  
        self.zNear_tmp = DoubleVar() 
        self.zFar_tmp = DoubleVar() 
        
        self.fov_tmp.set(45.0) 
        self.asp_tmp.set(1.48) 
        self.zNear_tmp.set(1.0) 
        self.zFar_tmp.set(100.0)    

        # can multi choice #
        self.eyeX = DoubleVar()
        self.eyeY = DoubleVar()
        self.eyeZ = DoubleVar()
        
        self.eyeX.set(0.0)
        self.eyeY.set(0.0)
        self.eyeZ.set(10.0)
        
        self.eyeX_tmp = DoubleVar()
        self.eyeY_tmp = DoubleVar()
        self.eyeZ_tmp = DoubleVar()
        
        self.eyeX_tmp.set(0.0)
        self.eyeY_tmp.set(0.0)
        self.eyeZ_tmp.set(10.0)

        self.centerX = DoubleVar()
        self.centerY = DoubleVar()
        self.centerZ = DoubleVar()
        
        self.centerX.set(0.0)
        self.centerY.set(0.0)
        self.centerZ.set(0.0)

        self.centerX_tmp = DoubleVar()
        self.centerY_tmp = DoubleVar()
        self.centerZ_tmp = DoubleVar()
        
        self.centerX_tmp.set(0.0)
        self.centerY_tmp.set(0.0)
        self.centerZ_tmp.set(0.0)

        self.upX = DoubleVar()
        self.upY = DoubleVar()
        self.upZ = DoubleVar()
        
        self.upX.set(0.0)
        self.upY.set(1.0)
        self.upZ.set(0.0)

        self.upX_tmp = DoubleVar()
        self.upY_tmp = DoubleVar()
        self.upZ_tmp = DoubleVar()
        
        self.upX_tmp.set(0.0)
        self.upY_tmp.set(1.0)
        self.upZ_tmp.set(0.0)
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
        self.lightPh = 90

        ### BEGIN TEXTURES  ###
        self.toggleTextures = -1
        self.imageWHTex = None #Load image with PIL
        self.textureDraw = None
        self.imgDataTex = None
        ### END TEXTURES  ###

        ###  EFFECT  ###
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
        gluPerspective(fov.get(), asp.get(), zNear.get(), zFar.get()) #void gluPerspective(	GLdouble fovy, GLdouble aspect,GLdouble zNear, 	GLdouble zFar);
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def initgl(self):
        glutInit()
        self.displayInit()
        self.displayProject(self.fov, self.asp, self.zNear, self.zFar)


    def redisplayAll(self):
        self.displayReshape(1024, 768)
        glutPostRedisplay()

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
                glDisable(GL_LIGHTING)
                glColor3fv([1,1,1])
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
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image as Pil_image
import numpy as np
import math
from drawobject import drawObject
from pyopengltk import OpenGLFrame
from tkinter import *

class Draw(drawObject, OpenGLFrame):
    def __init__(self, obj, isTexture=None, isLight=None, shape='face', *args, **kw):
        drawObject.__init__(self,isTexture=isTexture, shape=shape)
        OpenGLFrame.__init__(self, *args, **kw)
        self.animate = 0
        self.cb = None
        self.rota = 0.0
        self.isLight = isLight
        self.texture = 0 # save texture to draw

        ### Begin for aphin ###
        self.aphinType = -1 # 0 is Scale; 1 is Rotate; 2 is Translate
        self.mouse = (0.0, 0.0)
        self.moveR = (0.0, 0.0)
        self.moveT = (0.0, 0.0)
        self.preMoveR = (0.0, 0.0)
        self.preMoveT = (0.0, 0.0)
        self.sizeObject = 0.0 # Object Size
        self.isTranslateFirst = 0
        self.isRotateFirst = 0
        self.bind('<Button-1>', self.tkRecordMouse)
        if self.aphinType in range(3):
            self.bind('<B1-Motion>', self.tkAphin)

        self.dim = 6.0 # dimension of orthogonal box
        self.th = 0   # azimuth of view angle 
        self.ph = 0   # elevation of view angle 

        # Object
        self.object = obj
        # Scale
        self.varScaleX = DoubleVar()
        self.varScaleY = DoubleVar()
        self.varScaleZ = DoubleVar()
        ### For Projection ###
        self.toggleProjection = 0 # 0 is off; 1 is on
        # can multi choice #
        self.toggleProjection_Perspective = 0 # 0 is off; 1 is on
        self.toggleProjection_LookAt_Eye = 0 # 0 is off; 1 is on
        self.toggleProjection__LookAt_Center = 0 # 0 is off; 1 is on
        self.toggleProjection__LookAt_Up = 0 # 0 is off; 1 is on
        # can multi choice #
        self.fov = 45.0 # field of view for perspective 
        self.asp = 1.0  # aspect ratio;field of view for perspective
        self.zNear = 1.0 # field of view for perspective
        self.zFar = 100.0 # field of view for perspective
        self.eyeX = 0.0
        self.eyeY = 0.0
        self.eyeZ = 10.0
        self.centerX = 0.0
        self.centerY = 0.0
        self.centerZ = 0.0
        self.upX = 0.0
        self.upY = 1.0
        self.upZ = 0.0
        ### For Projection ###
        self.g_is_rotate = 0 # 0 is off; 1 is on
        glutInit()

    # def tkTestSetAphin1(self, event):
    #     self.aphinType = 1
    #     self.isRotateFirst = 1
    #     self.bind('<B1-Motion>', self.tkAphin)
    #     print(self.aphinType)


    # def tkTestSetAphin2(self, event):
    #     self.aphinType = 2
    #     self.isTranslateFirst = 1
    #     self.bind('<B1-Motion>', self.tkAphin)
    #     print(self.aphinType)

    def tkSizeObject(self, event): # Get object size
        self.sizeObject = math.sqrt(math.pow((event.x - self.mouse[0]), 2) + math.pow((event.y - self.mouse[1]), 2))/150

    def tkRecordMouse(self, event):
        if self.aphinType == 1:
            self.mouse = (event.x - self.preMoveR[0],event.y + self.preMoveR[1])
        elif self.aphinType == 2:
            self.mouse = (event.x - self.preMoveT[0],event.y + self.preMoveT[1])
        elif self.aphinType == 0:
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

    def Init(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        if self.isTexture:
            glEnable(GL_TEXTURE_2D)
            #read image to byte
            image = Pil_image.open("./textures/brick.jpg")
            # image = Image.open("./textures/smiley.png")
            self.image = image.transpose(Pil_image.FLIP_TOP_BOTTOM)
            self.img_data = image.convert("RGBA").tobytes()
            self.LoadGLTextures()
        if self.isLight:
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            light_pos = [0.0, 0.0, 1.0, 0.0 ]
            glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
            ambient = [0.0, 0.5, 0.0, 1.0]
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
            diff_use = [0.5, 0.5, 0.0, 1.0]
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diff_use)
            specular =  [ 1.0, 1.0, 0.5, 1.0 ]
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
            shininess = 45
            glMateriali(GL_FRONT, GL_SHININESS, shininess)


    def redraw(self):
        self.rota += 0.5
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(self.eyeX, self.eyeY, self.eyeZ, self.centerX, self.centerY, self.centerZ, self.upX, self.upY, self.upZ)
        glPushMatrix()
        if self.aphinType == 0:
            glScale(self.varScaleX.get(), self.varScaleY.get(),self.varScaleZ.get())
        elif self.aphinType == 1:
            glRotatef(self.moveR[1], 1, 0, 0)
            glRotatef(self.moveR[0], 0, 1, 0)
            if self.isTranslateFirst:
                glTranslatef(self.moveT[0] , self.moveT[1], 0.0)
        elif self.aphinType == 2 :
            if self.isRotateFirst:
                glRotatef(self.moveR[1], 1, 0, 0)
                glRotatef(self.moveR[0], 0, 1, 0)
            glTranslatef(self.moveT[0] , self.moveT[1], 0.0)    
        if self.object == 'cube':
            self.make_cube(self.sizeObject)
        elif self.object == 'box':
            self.make_box(1, 2, 3)
        elif self.object == 'teapot':
            self.make_teapot(self.sizeObject)
        elif self.object == 'sphere':
            self.make_sphere(self.sizeObject)
        # self.make_cone(1,3)
        # self.make_cylinder(1,2)
        # self.make_torus(1,2)
        # self.make_teapot(2)
        # self.make_truncatedCone(1,2,2)
        # self.make_pyramid(3,3)
        glPopMatrix()
        glFlush()


    def tkResize(self, evt):
        self.width, self.height = evt.width, evt.height
        self.asp =  self.width/self.height if self.height > 0 else 1
        if self.winfo_ismapped():
            glViewport(0, 0, self.width, self.height)
            self.initgl()

    # initgl
    def initgl(self):
        self.Init()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, self.asp, self.zNear, self.zFar)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    # Load Texture
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

    def SetMaterialColor(self, ambient, diff_use):
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diff_use)

    # Giữ nguyên hàm run
    def run(self):
        glutDisplayFunc(self.Draw)
        glutReshapeFunc(self.ReShape)
        glutKeyboardFunc(self.WindowKey)
        glutSpecialFunc(self.WindowSpecial)


# def MouseButton(type_button, state, x, y):
#     if (type_button == GLUT_LEFT_BUTTON):
#         if (state == GLUT_UP):
#             pass 
#         else:
#             pass
#     elif(type_button == GLUT_RIGHT_BUTTON):
#         if (state == GLUT_UP):
#           self.g_is_rotate = 0
#         else:
#           self.g_is_rotate = 1
#     else:
#         pass
# def MouseMove(int x,)

# if __name__ == "__main__":
    # root = Tk()
    # root.geometry("1024x768")
    # # root.attributes("-fullscreen", True)

    # sub_frame = Frame(root)
    # sub_frame.place(relwidth = 0.9, relheight=1)

    # app = Draw('cube', False, False, 'face', sub_frame)
    # app.animate = 1
    # app.place(relwidth = 1, relheight=1)
    # scaleX = Scale(sub_frame, variable = app.varScaleX , from_ =1, to=10, resolution=0.1)
    # scaleX.pack(anchor = NW)
    # scaleY = Scale(sub_frame, variable = app.varScaleY , from_ =1, to=10, resolution=0.1)
    # scaleY.pack(anchor = N)
    # scaleZ = Scale(sub_frame, variable = app.varScaleZ , from_ =1, to=10, resolution=0.1)
    # scaleZ.pack(anchor = NE)
    
    # root.mainloop()
    

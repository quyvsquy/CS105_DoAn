from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import math
from drawobject import drawObject

dO = drawObject(False,"points")
dO = drawObject(True,"lines")
# dO = drawObject(True,"solids")

GLUT_LEFT_BUTTON = 0
GLUT_MIDDLE_BUTTON = 1
GLUT_RIGHT_BUTTON = 2

rota = 45.0
texture = 0

#read image to byte
image = Image.open("./textures/brick.jpg")
# image = Image.open("./textures/cat.png")
image = image.transpose(Image.FLIP_TOP_BOTTOM)
img_data = image.convert("RGBA").tobytes()

def Init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    LoadGLTextures()


def draw():
    global rota
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # teapot
    glPushMatrix()
    glTranslatef(-2.5, 0.0, 0.0)
    # Init([ 1.0, 0.0, 0.0, 1.0 ])
    glRotatef(rota, 1.0, 1.0, 1.0)
    # glTexGeni(GL_S, GL_TEXTURE_GEN_MODE,  GL_OBJECT_LINEAR)
    # glTexGeni(GL_T, GL_TEXTURE_GEN_MODE,  GL_OBJECT_LINEAR)
    # glEnable(GL_TEXTURE_GEN_S)
    # glEnable(GL_TEXTURE_GEN_T)

    # glDisable(GL_TEXTURE_GEN_S)
    # glDisable(GL_TEXTURE_GEN_T)
    # dO.MakeCube(2)
    # dO.MakeBox(3,3,3)
    # dO.MakeSphere(1)
    # dO.MakeCone(1,3)
    # dO.MakeCylinder(1,2)
    # dO.MakeTorus(1,2)
    # dO.MakeTeapot(2)
    dO.MakeTruncatedCone(1,2,2)
    # MakePyramid(2,2)

    glPopMatrix()

    # # Cone
    # glPushMatrix()
    # glTranslatef(0.0, -0.3, 0.0)
    # glRotatef(-90.0, 1.0, 0.0, 0.0)
    # glRotatef(rota, 1.0, -1.0, 1.0)
    # # glutSolidCone(1, 2.5, 10, 16)
    # MakeCone(1,2.5)
    # glPopMatrix()


    # # # Torus
    # glPushMatrix()
    # glTranslatef(2.5, 0.0, 0.0)
    # # # glColor3f(0.0, 0.0, 1.0)
    # glRotatef(45, -1.0, 0.0, 0.0)
    # glRotatef(rota, 1.0, 1.0, -1.0)
    # glTexGeni(GL_S, GL_TEXTURE_GEN_MODE,  GL_OBJECT_LINEAR)
    # glTexGeni(GL_T, GL_TEXTURE_GEN_MODE,  GL_OBJECT_LINEAR)
    # glEnable(GL_TEXTURE_GEN_S)
    # glEnable(GL_TEXTURE_GEN_T)
    # glutSolidTorus(0.5,1,16,16)
    # glDisable(GL_TEXTURE_GEN_S)
    # glDisable(GL_TEXTURE_GEN_T)
    # glPopMatrix()

    glutSwapBuffers()
    rota += 0.5
 
def ReShape(width,height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-6, 6, -6, 6, 1, 25)
    glMatrixMode(GL_MODELVIEW)

def timer(value):
    glutPostRedisplay()
    glutTimerFunc(1, timer, 0)

def LoadGLTextures():
    global texture
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)



def MouseButton(type_button, state, x, y):
    if (type_button == GLUT_LEFT_BUTTON):
        if (state == GLUT_UP):
            pass 
        else:
            pass
    elif(type_button == GLUT_RIGHT_BUTTON):
        if (state == GLUT_UP):
            pass
    else:
        pass

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH | GLUT_RGB)
glutInitWindowSize(1024, 768)
glutInitWindowPosition(0, 0)
glutCreateWindow("Lab3_17520960")
glutTimerFunc(0, timer, 0)
Init()

glutDisplayFunc(draw)
glutReshapeFunc(ReShape)

glutMainLoop()

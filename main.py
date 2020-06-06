from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import math
from drawobject import drawObject

class Main(drawObject):
    def __init__(self, isTexture=None, typeDraw='solids'):
        super().__init__(isTexture=isTexture, typeDraw=typeDraw)
        self.rota = 45.0
        self.texture = 0 #save texture to draw
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH | GLUT_RGB)
        glutInitWindowSize(1024, 768)
        glutInitWindowPosition(0, 0)
        glutCreateWindow("Lab3_17520960")

    def Init(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        if self.isTexture:
            glEnable(GL_TEXTURE_2D)
            #read image to byte
            image = Image.open("./textures/brick.jpg")
            # image = Image.open("./textures/cat.png")
            self.image = image.transpose(Image.FLIP_TOP_BOTTOM)
            self.img_data = image.convert("RGBA").tobytes()
            self.LoadGLTextures()

    def Draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        glPushMatrix()
        glTranslatef(-2.5, 0.0, 0.0)
        # Init([ 1.0, 0.0, 0.0, 1.0 ])
        glRotatef(self.rota, 1.0, 1.0, 1.0)
        # self.make_cube(2)
        # self.make_box(1,2,3)
        # self.make_sphere(1)
        # self.make_cone(1,3)
        # self.make_cylinder(1,2)
        self.make_torus(1,2)
        # self.make_teapot(2)
        # self.make_truncatedCone(1,2,2)
        # self.make_pyramid(2,2)

        glPopMatrix()


        glutSwapBuffers()
        self.rota += 0.5
 
    def ReShape(self,width,height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-6, 6, -6, 6, 1, 25)
        glMatrixMode(GL_MODELVIEW)

    def Timer(self, value):
        glutPostRedisplay()
        glutTimerFunc(1, self.Timer, 0)

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

    def run(self):
        glutTimerFunc(0, self.Timer, 0)
        self.Init()
        glutDisplayFunc(self.Draw)
        glutReshapeFunc(self.ReShape)
        glutMainLoop()

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

if __name__ == "__main__":
    # main = Main(False,"points")
    # main = Main(True,"lines")
    main = Main(False,"solid")
    main.run()
    

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import math
from drawobject import drawObject

class Main(drawObject):
    def __init__(self, isTexture=None, isLight=None, typeDraw='solids'):
        self.isLight = isLight
        super().__init__(isTexture=isTexture, typeDraw=typeDraw)
        self.toggleMode = 0 # projection mode; perspective if ==1 else == orthogonal
        # self.rota = 45.0
        self.texture = 0 # save texture to draw
        self.dim= 6.0 # dimension of orthogonal box
        self.th = 0   # azimuth of view angle 
        self.ph = 0   # elevation of view angle 
        self.fov = 55 # field of view for perspective 
        self.asp = 1  # aspect ratio 

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH | GLUT_RGB )
        glutInitWindowSize(1024, 768)
        glutInitWindowPosition(0, 0)
        glutCreateWindow("CS105_17520941_17520960_17521055")

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
            # image = Image.open("./textures/smiley.png")
            self.image = image.transpose(Image.FLIP_TOP_BOTTOM)
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

    def Draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # gluLookAt(0.0, 0.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        glPushMatrix()
        #  Perspective - set eye position 
        if (self.toggleMode):
            Ex = -2*self.dim*math.sin(self.th)*math.cos(self.ph)
            Ey = +2*self.dim        *math.sin(self.ph)
            Ez = +2*self.dim*math.cos(self.th)*math.cos(self.ph)
            # camera/eye position, aim of camera lens, up-vector 
            gluLookAt(Ex,Ey,Ez , 0,0,0 , 0,math.cos(self.ph),0)
        #  Orthogonal - set world orientation 
        else:
            glRotatef(self.ph,1,0,0)
            glRotatef(self.th,0,1,0)

        # glTranslatef(-2.5, 0.0, 0.0)
        # glRotatef(self.rota, 1.0, 1.0, 1.0)
        # self.make_cube(2)
        # self.make_box(1,2,3)
        # self.make_sphere(1)
        # self.make_cone(1,3)
        # self.make_cylinder(1,2)
        # self.make_torus(1,2)
        # self.make_teapot(2)
        # self.make_truncatedCone(1,2,2)
        # print(self.toggleMode)
        self.PrintAt(5,5,f"View Angle (th, ph) =({self.th}, {self.ph})")
        self.PrintAt(5,25,f"Projection mode =({'Perspective' if self.toggleMode==1 else 'Orthogonal'})")
        # self.make_pyramid(3,3)
        self.make_teapot(2)
        glPopMatrix()

        glFlush()
        glutSwapBuffers()
        # self.rota += 0.5
 
    def ReShape(self,width,height):
        self.asp =  int(width/height) if height > 0 else 1
        glViewport(0, 0, width, height)
        self.Project()

    def Project(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if (self.toggleMode):
            # perspective 
            gluPerspective(self.fov,self.asp,self.dim/4,4*self.dim) #void gluPerspective(	GLdouble fovy, GLdouble aspect,GLdouble zNear, 	GLdouble zFar);
        else:
            # orthogonal projection
            glOrtho(-self.dim*self.asp,+self.dim*self.asp, -self.dim,+self.dim, -self.dim,+self.dim*6)
        # glOrtho(-6, 6, -6, 6, 1, 25)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def Timer(self, value):
        glutPostRedisplay()
        glutTimerFunc(1, self.Timer, 0)

    def WindowKey(self, key, x, y):
        #  Exit on ESC 
        key = key.decode("utf-8")
        if (key == chr(27)): exit(0)
        elif (key == 'm' or key == 'M'): self.toggleMode = 1-self.toggleMode
        #  Change field of view angle 
        elif (key == '-' and ord(key)>1)  : self.fov -= 1
        elif (key == '+' and ord(key)<179): self.fov += 1
        #  Change dimensions 
        elif (key == 'D'): self.dim += 0.1
        elif (key == 'd' and self.dim>1): self.dim -= 0.1
        self.Project()
        glutPostRedisplay()
        
    
    def WindowSpecial(self, key, x, y):
        #  Right arrow key - increase azimuth by 5 degrees 
        if (key == GLUT_KEY_RIGHT): self.th += 5
        #  Left arrow key - decrease azimuth by 5 degrees 
        elif (key == GLUT_KEY_LEFT): self.th -= 5
        #  Up arrow key - increase elevation by 5 degrees 
        elif (key == GLUT_KEY_UP): self.ph += 5
        #  Down arrow key - decrease elevation by 5 degrees 
        elif (key == GLUT_KEY_DOWN): self.ph -= 5

        #  Keep angles to +/-360 degrees 
        self.th %= 360
        self.ph %= 360

        self.Project()
        glutPostRedisplay()

    def WindowMenu(self, value):
        self.WindowKey(value,0,0)

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

    def SetMaterialColor(self,ambient,diff_use):
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diff_use)

    def PrintAt(self, x, y, *args):
        glWindowPos2i(x,y)
        for ia in args:
            for ch in ia:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18 , ctypes.c_int( ord(ch)))

    def run(self):
        self.Init()
        # glutTimerFunc(0, self.Timer, 0)
        glutDisplayFunc(self.Draw)
        glutReshapeFunc(self.ReShape)

        glutKeyboardFunc(self.WindowKey)
        glutSpecialFunc(self.WindowSpecial)
        # glutCreateMenu(self.WindowMenu)
        # glutAddMenuEntry("Toggle Mode [m]",ord("m"))
        # glutAttachMenu(GLUT_RIGHT_BUTTON)

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
    main = Main(True,True,"solid")
    main.run()
    

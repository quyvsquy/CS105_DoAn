from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from shape import  drawObject

class Init_Global_Para(drawObject):
    def __init__(self, typeDraw="face"):
        drawObject.__init__(self)
        self.isTexture = 0
        self.typeDraw = typeDraw # points, lines, face

        ###  TOGGLE DRAW DISPLAYS  ###
        self.toggleAxes = False
        self.toggleParams = 1

        ###  Begin PROJECTION  ###
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
        ###  End PROJECTION  ###

        ###  LIGHTING  ###
        self.toggleLight = True
        # self.distance = 5
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

        # ###  TEXTURES  ###
        # self.textures = None
        # self.currentTexture = 0

        # ###  ANIMATION  ###
        # self.toggleAnimation = DEF_ANIMATE
        # self.cubeRotation = DEF_CUBE_ROTATION

    def displayInit(self):
        glClearColor(0.0,0.0,0.0,0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glShadeModel(GL_SMOOTH)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

    def displayEye(self):
        gluLookAt(self.eyeX, self.eyeY, self.eyeZ, self.centerX, self.centerY, self.centerZ, self.upX, self.upY, self.upZ) #void gluLookAt(GLdouble eyeX,GLdouble eyeY,GLdouble eyeZ,GLdouble centerX,GLdouble centerY,GLdouble centerZ,GLdouble upX,GLdouble upY,GLdouble upZ);

    def displayReshape(self, evt, width, height): #==tkResize in base.py
        glViewport(0,0, width,height)
        self.displayProject(self.fov,self.asp,self.zNear,self.zFar)

    def displayProject(self,fov,asp,zNear,zFar):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fov,asp,zNear,zFar) #void gluPerspective(	GLdouble fovy, GLdouble aspect,GLdouble zNear, 	GLdouble zFar);
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def initgl(self):
        glutInit()
        self.displayInit()
        # self.displayEye()
        self.displayProject(self.fov,self.asp,self.zNear,self.zFar)
        # self.drawLight()


    def redisplayAll(self):
        self.displayReshape(1024, 768)
        glutPostRedisplay()

    def drawAxes(self):
        if (self.toggleAxes):
            ###  Length of axes ###
            len = 5.0
            glDisable(GL_LIGHTING)
            glBegin(GL_LINES)
            glColor3f(1.0, 0.0, 0.0)
            glVertex3f(-len, 0.0, 0.0)
            glVertex3f(len, 0.0, 0.0)
            glEnd()
            glBegin(GL_LINES)
            glColor3f(0.0, 1.0, 0.0)
            glVertex3f(0.0, -len, 0.0)
            glVertex3f(0.0, len, 0.0)
            glEnd()
            glBegin(GL_LINES)
            glColor3f(0.0, 0.0, 1.0)
            glVertex3f(0.0, 0.0, -len)
            glVertex3f(0.0, 0.0, len)
            glEnd()
            ###  Label axes ###
            glColor3fv(self.white)
            glRasterPos3d(len,0,0)
            glRasterPos3d(0,len,0)
            glRasterPos3d(0,0,len)
            if self.toggleLight:
                glEnable(GL_LIGHTING)

    def drawLight(self):
        ###  Light switch ###
        if self.toggleLight:
            ###  Translate intensity to color vectors ###
            Ambient    =[0.01*self.ambient ,0.01*self.ambient ,0.01*self.ambient ,1.0]
            Diffuse    =[0.01*self.diffuse ,0.01*self.diffuse ,0.01*self.diffuse ,1.0]
            Specular   =[0.01*self.specular,0.01*self.specular,0.01*self.specular,1.0]
            # Position  = [self.lightPosX, self.lightPosY, 0.0, 1.0]
            Position   = [0, 0, 5, 1.0]
            ###  Draw light position as sphere (still no lighting here) ###
            glPushMatrix()
            glColor3fv([1,0,0])
            glDisable(GL_LIGHTING)
            glTranslate(Position[0], Position[1], Position[2])
            # self.make_sphere(0.3)
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
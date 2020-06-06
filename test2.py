import math
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *


rota = 45.0


def draw():
    global rota
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(4.0, 4.0, 15.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # Cube
    glPushMatrix()
    DrawCoordinate()
    SetMaterialColor([1,0,0,1],[1,0,0,1])
    glRotatef(rota, 0.0, 0.0, 1.0)
    # MakeCube(1)
    glutSolidTeapot(1)
    glPopMatrix()

    # Box
    glPushMatrix()
    glTranslatef(-6.0, 0.0, 0.0)
    SetMaterialColor([0,1,0,1],[0,1,0,1])
    glRotatef(rota, 0.0, 0.0, 1.0)
    MakeBox(1,2,3)
    glPopMatrix()

    # Sphere
    glPushMatrix()
    glTranslatef(3.0, 0.0, 0.0)
    SetMaterialColor([1,1,0,1],[1,1,0,1])
    glRotatef(rota, 0.0, 0.0, 1.0)
    MakeSphere(1)
    glPopMatrix()

    # Cylinder
    glPushMatrix()
    glTranslatef(-3.0, 0.0, 0.0)
    SetMaterialColor([0,0,1,1],[0,0,1,1])
    glRotatef(rota, 0.0, 0.0, 1.0)
    MakeCylinder(1, 5)
    glPopMatrix()

    # TruncatedCone
    glPushMatrix()
    glTranslatef(-2.8, -1.5, 4.0)
    SetMaterialColor([1, 0.6, 0.0, 1.0], [1, 0.6, 0.0, 1.0])
    glRotatef(rota, 1.0, 0.0, 0.0)
    MakeTruncatedCone(1, 2, 4)
    glPopMatrix()

    # Cone
    glPushMatrix()
    glTranslatef(0, -5.0, -2.0)
    SetMaterialColor([1, 0.6, 0.0, 1.0], [1, 0.6, 0.0, 1.0])
    glRotatef(-60.0, 1.0, 0.0, 0.0)
    glRotatef(rota, 1.0, 0.0, 0.0)
    MakeCone(1.5, 3.4)
    glPopMatrix()

    # Pyramid
    glPushMatrix()
    glTranslatef(0.0, 1.0, -4.0)
    SetMaterialColor([0.5, 0.3, 0.7, 1.0], [0.5, 0.2, 0.4, 1.0])
    glRotatef(rota, 0.0, 0.0, 1.0)
    MakePyramid(2, 5)
    glPopMatrix()

    # FrustumShape
    glPushMatrix()
    glTranslatef(5, -5.0, -2.0)
    SetMaterialColor([0.5, 0.2, 1.0, 1.0], [0.5, 0.2, 1.0, 1.0])
    glRotatef(rota, 0.0, 0.0, 1.0)
    MakeFrustumShape(2, 1, 4)
    glPopMatrix()

    # Octagon
    glPushMatrix()
    glTranslatef(6, 5.0, 2.0)
    SetMaterialColor([0.5, 1, 0.1, 1.0], [0.5, 1, 0.1, 1.0])
    glRotatef(rota, 0.0, 1.0, 0.0)
    MakeOctagon(1, 2)
    glPopMatrix()

    glutSwapBuffers()
    rota += 0.5

def Init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)

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


def ReShape(width,height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-10, 10, -10, 10, 1, 20)
    glMatrixMode(GL_MODELVIEW)

def timer(value):
    glutPostRedisplay()
    glutTimerFunc(1, timer, 0)


def DrawCoordinate():
    glDisable(GL_LIGHTING)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(10.0, 0.0, 0.0)
    glEnd()

    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 10.0, 0.0)
    glEnd()

    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 30.0)
    glEnd()

    glEnable(GL_LIGHTING)


def SetMaterialColor(ambient,diff_use):
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diff_use)    

def MakeCube(size):
    # glBegin(GL_LINES)
    # glBegin(GL_POINTS)
    glBegin(GL_QUADS)
    # Front Face
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(-size, -size, size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)
    # Back Face
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, -size, -size)
    # Top Face
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-size, size, -size)
    glVertex3f(-size, size, size)
    glVertex3f(size, size, size)
    glVertex3f(size, size, -size)
    # Bottom Face
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-size, -size, -size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, -size, size)
    glVertex3f(-size, -size, size)
    # Right face
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(size, -size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, size, size)
    glVertex3f(size, -size, size)
    # Left Face
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, -size, size)
    glVertex3f(-size, size, size)
    glVertex3f(-size, size, -size)

    glEnd()

def MakeBox(length, width, height):
    x = length
    y = height
    z = width

    # Back
    glBegin(GL_QUADS)
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(0, 0, 0)
    glVertex3f(x, 0, 0)
    glVertex3f(x, y, 0)
    glVertex3f(0, y, 0)
    glEnd()

    #  left
    glBegin(GL_QUADS)
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, z)
    glVertex3f(0, y, z)
    glVertex3f(0, y, 0)
    glEnd()

    # front
    glBegin(GL_QUADS)
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(0, 0, z)
    glVertex3f(0, y, z)
    glVertex3f(x, y, z)
    glVertex3f(x, 0, z)
    glEnd()

    # right
    glBegin(GL_QUADS)
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(x, 0, z)
    glVertex3f(x, 0, 0)
    glVertex3f(x, y, 0)
    glVertex3f(x, y, z)
    glEnd()

    # Top
    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(0, y, 0)
    glVertex3f(x, y, 0)
    glVertex3f(x, y, z)
    glVertex3f(0, y, z)
    glEnd()

    # Bottom
    glBegin(GL_QUADS)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(0, 0, 0)
    glVertex3f(x, 0, 0)
    glVertex3f(x, 0, z)
    glVertex3f(0, 0, z)
    glEnd()

def MakeSphere(radius):
    glutSolidSphere(radius, 64, 64)

def MakeCylinder(radius, length):
    quadratic_obj = gluNewQuadric()
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluCylinder(quadratic_obj, radius, radius, length, 32, 32)

def MakeTruncatedCone(base_rad, top_rad, length):
    quadratic_obj = gluNewQuadric()
    gluCylinder(quadratic_obj, base_rad, top_rad, length, 32, 32)

def MakeCone(base_rad, length):
    quadratic_obj = gluNewQuadric()
    gluCylinder(quadratic_obj, base_rad, 0.0, length, 32, 32)

def MakePyramid(size, height):
    half_size = size * 0.5
    glBegin(GL_TRIANGLES)
    # Front face
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, height, 0.0)
    glVertex3f(-half_size, 0, half_size)
    glVertex3f(half_size, 0, half_size)

    # left face
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(0.0, height, 0.0)
    glVertex3f(-half_size, 0.0, -half_size)
    glVertex3f(-half_size, 0.0, half_size)

    # back face
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(0.0, height, 0.0)
    glVertex3f(-half_size, 0, -half_size)
    glVertex3f(half_size, 0, -half_size)

    # Right face
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, height, 0.0)
    glVertex3f(half_size, 0.0, -half_size)
    glVertex3f(half_size, 0.0, half_size)
    glEnd()

    # Bottom face
    glBegin(GL_QUADS)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(half_size, 0.0, half_size)
    glVertex3f(half_size, 0.0, -half_size)
    glVertex3f(-half_size, 0.0, -half_size)
    glVertex3f(-half_size, 0.0, half_size)
    glEnd()

def MakeFrustumShape(bottom_size, top_size, height):
    half_bottom_size = 0.5 * bottom_size
    half_top_size = 0.5 * top_size

    glBegin(GL_QUADS)
    # Front Face
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(-half_bottom_size, 0.0, half_bottom_size)
    glVertex3f(half_bottom_size, 0.0, half_bottom_size)
    glVertex3f(half_top_size, height, half_top_size)
    glVertex3f(-half_top_size, height, half_top_size)
    # Back Face
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(-half_bottom_size, 0.0, -half_bottom_size)
    glVertex3f(half_bottom_size, 0.0, -half_bottom_size)
    glVertex3f(half_top_size, height, -half_top_size)
    glVertex3f(-half_top_size, height, -half_top_size)

    # Top Face
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-half_top_size, height, -half_top_size)
    glVertex3f(-half_top_size, height, half_top_size)
    glVertex3f(half_top_size, height, half_top_size)
    glVertex3f(half_top_size, height, -half_top_size)
    # Bottom Face
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-half_bottom_size, 0.0, -half_bottom_size)
    glVertex3f(half_bottom_size, 0.0, -half_bottom_size)
    glVertex3f(half_bottom_size, 0.0, half_bottom_size)
    glVertex3f(-half_bottom_size, 0.0, half_bottom_size)
    # Right face
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(half_bottom_size, 0.0, -half_bottom_size)
    glVertex3f(half_bottom_size, 0.0, half_bottom_size)
    glVertex3f(half_top_size, height, half_top_size)
    glVertex3f(half_top_size, height, -half_top_size)
    # Left Face
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(-half_bottom_size, 0.0, -half_bottom_size)
    glVertex3f(-half_bottom_size, 0.0, half_bottom_size)
    glVertex3f(-half_top_size, height, half_top_size)
    glVertex3f(-half_top_size, height, -half_top_size)
    glEnd()

def MakeOctagon(side, thickness):
    anpha = math.pi / 4.0
    x = math.sin(anpha) * side
    y = 0.5 * side

    z = thickness
    center_to_mid_size = x + y
    for j in range(8):
        glPushMatrix()
        glTranslatef(-center_to_mid_size, 0.0, 0.0)
        #Draw 8 rectangle side
        glBegin(GL_QUADS)
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(0.0, -y, z)
        glVertex3f(0.0, y, z)
        glVertex3f(0.0, y, 0)
        glVertex3f(0.0, -y, 0)
        glEnd()
        glPopMatrix()

        glBegin(GL_TRIANGLES)
        glNormal3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, z)
        glVertex3f(-center_to_mid_size, -y, z)
        glVertex3f(-center_to_mid_size, y, z)

        glNormal3f(0.0, 0.0, -1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(-center_to_mid_size, y, 0.0)
        glVertex3f(-center_to_mid_size, -y, 0.0)
        glEnd()

        glRotatef(45.0, 0.0, 0.0, 1.0)




glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(1024, 768)
glutInitWindowPosition(0, 0)
glutCreateWindow("Lab3_17520960")
Init()
# glutTimerFunc(0, timer, 0)
glutDisplayFunc(draw)
glutReshapeFunc(ReShape)

glutMainLoop()
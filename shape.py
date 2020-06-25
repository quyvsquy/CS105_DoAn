from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *


class drawObject:
    def __init__(self):
        self.indexCoord2f = (
                                (0.0, 0.0), 
                                (0.0, 1.0), 
                                (1.0, 1.0), 
                                (1.0, 0.0), 
                                (0.5, 1.0), 
        )
    def set_vertices(self, x, y, z): # for cube, box
        self.vertices =  [            
                            [x, -y, -z], 
                            [x, y, -z], 
                            [-x, y, -z], 
                            [-x, -y, -z], 
                            [x, -y, z], 
                            [x, y, z], 
                            [-x, -y, z], 
                            [-x, y, z], 
        ]
        self.edges = (
                        (0, 1), 
                        (0, 3), 
                        (0, 4), 
                        (2, 1), 
                        (2, 3), 
                        (2, 7), 
                        (6, 3), 
                        (6, 4), 
                        (6, 7), 
                        (5, 1), 
                        (5, 4), 
                        (5, 7)
                     )
        self.surfaces = (
                            (0, 1, 2, 3), 
                            (3, 2, 7, 6), 
                            (6, 7, 5, 4), 
                            (4, 5, 1, 0), 
                            (1, 5, 7, 2), 
                            (4, 0, 3, 6), 
                        )
    def init_pyramid(self, size, height):
        half_size = size * 0.5
        self.verPy = [
                        [0.0, height, 0.0], 
                        [-half_size, 0.0, half_size], 
                        [half_size, 0.0, half_size], 
                        [-half_size, 0.0, -half_size], 
                        [half_size, 0.0, -half_size], 
        ]
        self.indexPy = [
            [0, 1, 2], # Front face
            [0, 3, 1], # Left face
            [0, 3, 4], # Back face
            [0, 4, 2], # Right face
            [2, 4, 3, 1], # Bottom face
        ]
    def make_cube(self, size):
        self.set_vertices(size, size, size)
        if self.typeDraw == "points":
            glBegin(GL_POINTS)
            for edge in self.edges:
                for vertex in edge:
                    glVertex3fv(self.vertices[vertex])
        elif self.typeDraw == "lines":
            glBegin(GL_LINES)
            for edge in self.edges:
                for vertex in edge:
                    glVertex3fv(self.vertices[vertex])
        else:
            glBegin(GL_QUADS)
            if self.isTexture:
                for surface in self.surfaces:
                    for ia, vertex in enumerate(surface):
                        glTexCoord2fv(self.indexCoord2f[ia])
                        glVertex3fv(self.vertices[vertex])
            else:
                for surface in self.surfaces:
                    for vertex in surface:
                        glVertex3fv(self.vertices[vertex])
        glEnd()

    def make_box(self, length, width, height):
        self.set_vertices(length, width, height)
        if self.typeDraw == "points":
            glBegin(GL_POINTS)
            for edge in self.edges:
                for vertex in edge:
                    glVertex3fv(self.vertices[vertex])
        elif self.typeDraw == "lines":
            glBegin(GL_LINES)
            for edge in self.edges:
                for vertex in edge:
                    glVertex3fv(self.vertices[vertex])
        else:
            glBegin(GL_QUADS)
            if self.isTexture:
                for surface in self.surfaces:
                    for ia, vertex in enumerate(surface):
                        glTexCoord2fv(self.indexCoord2f[ia])
                        glVertex3fv(self.vertices[vertex])
            else:
                for surface in self.surfaces:
                    for vertex in surface:
                        glVertex3fv(self.vertices[vertex])
        glEnd()   


    def make_sphere(self, radius):
        if self.typeDraw == "points":
            print("cc")
            obj = gluNewQuadric()
            gluQuadricDrawStyle(obj, GLU_POINT)
            gluSphere(obj, radius, 32, 32)
        elif self.typeDraw == "lines":
            glutWireSphere(radius, 32, 32)
        else:
            if self.isTexture:
                quadratic_obj = gluNewQuadric()
                gluQuadricTexture(quadratic_obj, GL_TRUE)
                gluSphere(quadratic_obj, radius, 32, 32)
            else:
                glutSolidSphere(radius, 32, 32)
    
    def make_light_source_shape(self):
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        glutSolidSphere(0.2, 32, 32)


    def make_cone(self, base_rad, length):
        if self.typeDraw == "points":
            obj = gluNewQuadric()
            gluQuadricDrawStyle(obj, GLU_POINT)
            gluCylinder(obj, base_rad, 0.0, length, 32, 32)
        elif self.typeDraw == "lines":
            glutWireCone(base_rad, length, 32, 32)
        else:
            if self.isTexture:
                quadratic_obj = gluNewQuadric()
                gluQuadricTexture(quadratic_obj, GL_TRUE)
                gluCylinder(quadratic_obj, base_rad, 0.0, length, 32, 32)
            else:
                glutSolidCone(base_rad, length, 32, 32)


    def make_cylinder(self, radius, length):
        #Hinh Tru
        if self.typeDraw == "points":
            obj = gluNewQuadric()
            gluQuadricDrawStyle(obj, GLU_POINT)
            gluCylinder(obj, radius, radius, length, 32, 32)
        elif self.typeDraw == "lines":
            glutWireCylinder(radius, length, 32, 32)
        else:
            if self.isTexture:
                quadratic_obj = gluNewQuadric()
                gluQuadricTexture(quadratic_obj, GL_TRUE)
                glRotatef(-90, 1.0, 0.0, 0.0)
                gluCylinder(quadratic_obj, radius, radius, length, 32, 32)
            else:
                glutSolidCylinder(radius, length, 32, 32)

    def make_torus(self, innerRadius, outerRadious):
        if self.typeDraw == "points":
            glPolygonMode(GL_FRONT_AND_BACK, GL_POINT)
            glutSolidTorus(innerRadius, outerRadious, 32, 32)
        elif self.typeDraw == "lines":
            glutWireTorus(innerRadius, outerRadious, 32, 32)
        else:
            if self.isTexture:
                glTexGeni(GL_S, GL_TEXTURE_GEN_MODE,  GL_OBJECT_LINEAR)
                glTexGeni(GL_T, GL_TEXTURE_GEN_MODE,  GL_OBJECT_LINEAR)
                glEnable(GL_TEXTURE_GEN_S)
                glEnable(GL_TEXTURE_GEN_T)
                glutSolidTorus(innerRadius, outerRadious, 32, 32)
                glDisable(GL_TEXTURE_GEN_S)
                glDisable(GL_TEXTURE_GEN_T)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                glutSolidTorus(innerRadius, outerRadious, 32, 32)

                
    def make_teapot(self, size):
        if self.typeDraw == "points":
            glPolygonMode(GL_FRONT_AND_BACK, GL_POINT)
            glutSolidTeapot(size)
        elif self.typeDraw == "lines":
            glutWireTeapot(size)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glutSolidTeapot(size)

    def make_truncatedCone(self, base_rad, top_rad, length):
        #Non cut
        if self.typeDraw == "points":
            obj = gluNewQuadric()
            gluQuadricDrawStyle(obj, GLU_POINT)
            gluCylinder(obj, base_rad, top_rad, length, 32, 32)
        elif self.typeDraw == "lines":
            obj = gluNewQuadric()
            gluQuadricDrawStyle(obj, GLU_LINE)
            gluCylinder(obj, base_rad, top_rad, length, 32, 32)
        else:
            if self.isTexture:
                quadratic_obj = gluNewQuadric()
                gluQuadricTexture(quadratic_obj, GL_TRUE)
                glRotatef(-90, 1.0, 0.0, 0.0)
                gluCylinder(quadratic_obj, base_rad, top_rad, length, 32, 32)
            else:
                quadratic_obj = gluNewQuadric()
                gluCylinder(quadratic_obj, base_rad, top_rad, length, 32, 32)

    def make_pyramid(self, size, height):
        self.init_pyramid(size, height)
        if self.typeDraw == "points":
            glBegin(GL_POINTS)
            for ia in range(len(self.indexPy)-1):
                for ib in self.indexPy[ia]:
                    glVertex3fv(self.verPy[ib])
            glEnd()
            glBegin(GL_POINTS)
            for ia in self.indexPy[-1]:
                glVertex3fv(self.verPy[ia])
            glEnd()
        elif self.typeDraw == "lines":
            glBegin(GL_LINES)
            for ia in range(len(self.indexPy)-1):
                for ib in self.indexPy[ia]:
                    glVertex3fv(self.verPy[ib])
            glEnd()
            glBegin(GL_LINE_LOOP)
            for ia in self.indexPy[-1]:
                glVertex3fv(self.verPy[ia])
            glEnd()
        else:
            glBegin(GL_TRIANGLES)
            for ia in range(len(self.indexPy)-1):
                tempInt = 0
                for ib in self.indexPy[ia]:
                    if ib == 0:
                        glTexCoord2fv(self.indexCoord2f[-1])
                    else:
                        glTexCoord2fv(self.indexCoord2f[3]) if tempInt % 2 ==0 \
                            else glTexCoord2fv(self.indexCoord2f[0])
                    tempInt += 1
                    glVertex3fv(self.verPy[ib])
            glEnd()
            glBegin(GL_QUADS)
            for id, ia in enumerate(self.indexPy[-1]):
                glTexCoord2fv(self.indexCoord2f[id])
                glVertex3fv(self.verPy[ia])
            glEnd()
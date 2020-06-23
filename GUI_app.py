from tkinter import *
from drawobject import drawObject
from pyopengltk import OpenGLFrame
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from test3 import Draw
font = 'mincho 12'
##############
class App3D:
    def __init__(self):
        self.root = Tk()
        self.root.attributes("-fullscreen", True)

        self.object_drawing = None

        self.frame_options_1 = Frame(self.root, bg='#EBE5E9')
        self.frame_options_1.place(relx=0.01, rely=0.1, relwidth=0.08, relheight=0.89)
        self.frame_options_2 = Frame(self.root, bg='#EBE5E9')
        self.frame_options_2.place(relx=0.1, rely=0.1, relwidth=0.14, relheight=0.89)
        self.frames_using = []
        # Transform Buttons (root): Scale, Rotate, Translate
        # Scale
        self.scale_mode = 0
        self.button_scale = Button(self.root, bg='#fffc33', text='SCALE', command=self.load_scale_board)
        # Rotate
        self.button_rotate = Button(self.root, bg='#8fd6de', text='ROTATE', command=self.rotate)
        # Translate
        self.button_translate = Button(self.root, bg='#ed7686', text='TRANSLATE', command=self.translate)
        """=========================================="""
        # Objects Buttons (options 1): Teapot  
        # Teapot   
        self.button_teapot = Button(self.frame_options_1, command=lambda:self.make_object('teapot'))
        self.button_cube = Button(self.frame_options_1, command=lambda:self.make_object('cube'))
        self.button_sphere = Button(self.frame_options_1, command=lambda:self.make_object('sphere'))
        self.button_teapot3 = Button(self.frame_options_1, command=lambda:self.make_object('teapot'))
        self.button_teapot4 = Button(self.frame_options_1, command=lambda:self.make_object('teapot'))
        self.button_teapot5 = Button(self.frame_options_1, command=lambda:self.make_object('teapot'))
        self.button_teapot6 = Button(self.frame_options_1, command=lambda:self.make_object('teapot'))
        self.button_teapot7 = Button(self.frame_options_1, command=lambda:self.make_object('teapot'))
        """=========================================="""
        # Shape Options (options 2): Line, Point, Face
        def test():
            print(var.get())
        var = IntVar()
        self.frame_shape = LabelFrame(self.frame_options_2, bg='#EBE5E9', text='Shape')
        point = Radiobutton(self.frame_shape, bg='#EBE5E9', text="Point", variable=var, value=1, command=test)
        point.place(relx=0.2, rely=0.07, relheight=0.2)
        line = Radiobutton(self.frame_shape, bg='#EBE5E9', text="Line", variable=var, value=2, command=test)
        line.place(relx=0.2, rely = 0.4, relheight=0.2)
        face = Radiobutton(self.frame_shape, bg='#EBE5E9', text="Face", variable=var, value=3, command=test)
        face.place(relx=0.2, rely = 0.73, relheight=0.2)
        """=========================================="""
        # Projection Options (options 2): Perspective, Look At (Eye), Look At (Center), Look At(Up)
        self.frame_projection = LabelFrame(self.frame_options_2, bg='#EBE5E9', text='Projection')
        perspective = Radiobutton(self.frame_projection, bg='#EBE5E9', text="Perspective", variable=var, value=1, command=test)
        perspective.place(relx=0.2, rely=0.07, relheight=0.2)
        lookat_eye = Radiobutton(self.frame_projection, bg='#EBE5E9', text="Look At (Eye)", variable=var, value=2, command=test)
        lookat_eye.place(relx=0.2, rely=0.29, relheight=0.2)
        lookat_center = Radiobutton(self.frame_projection, bg='#EBE5E9', text="Look At (Center)", variable=var, value=3, command=test)
        lookat_center.place(relx=0.2, rely=0.51, relheight=0.2)
        lookat_up = Radiobutton(self.frame_projection, bg='#EBE5E9', text="Look At (Up)", variable=var, value=3, command=test)
        lookat_up.place(relx=0.2, rely=0.73, relheight=0.2)
        """=========================================="""
        # Light Options (options 2): Light, Light Source, Shadow 0
        self.frame_light = LabelFrame(self.frame_options_2, bg='#EBE5E9', text='Light')
        light = Checkbutton(self.frame_light, bg='#EBE5E9', text='Light', variable=var)
        light.place(relx=0.2, rely=0.07, relheight=0.2)
        light_source = Checkbutton(self.frame_light, bg='#EBE5E9', text='Light Source', variable=var)
        light_source.place(relx=0.2, rely=0.4, relheight=0.2)
        shadow = Checkbutton(self.frame_light, bg='#EBE5E9', text='Shadow', variable=var)
        shadow.place(relx=0.2, rely=0.73, relheight=0.2)
        """=========================================="""
        # Fog Option (options 2): Fog
        self.frame_fog = LabelFrame(self.frame_options_2, bg='#EBE5E9', text='Fog')
        fog = Checkbutton(self.frame_fog, bg='#EBE5E9', text='Fog', variable=var)
        fog.place(relx=0.2, rely=0.07, relheight=0.86)
        """=========================================="""
        # Texture Option (options 2): Texture
        self.frame_texture = LabelFrame(self.frame_options_2, bg='#EBE5E9', text='Texture')
        texture = Checkbutton(self.frame_texture, bg='#EBE5E9', text='Texture', variable=var)
        texture.place(relx=0.2, rely=0.07, relheight=0.86)
        """=========================================="""
        # Effect Option (options 2): Effect
        self.frame_effect = LabelFrame(self.frame_options_2, bg='#EBE5E9', text='Effect')
        effect = Checkbutton(self.frame_effect, bg='#EBE5E9', text='Effect', variable=var)
        effect.place(relx=0.2, rely=0.07, relheight=0.86)
        """=========================================="""
        # Draw frame
        self.frame_draw = Frame(self.root, bg='#000000')  # Draw here

        # Test_1
        self.button_test_1 = Button(self.root, bg='#DFBA67', text='Test_1', font="mincho 10",
              
                                     command=lambda:self.make_object('teapot'))


        # Exit
        self.exit_button = Button(self.root, text='X', command=self.root.quit)

        # Clear
        self.button_clear = Button(self.root, text='CLEAR', command=self.clear_screen)

    def screenMain_Load(self):
        self.button_clear.place(relx=0.22, rely=0.05, relwidth=0.05, relheight=0.04)
        # Transform buttons: scale, rotate, translate
        self.button_scale.place(relx=0.01, rely=0.05, relheight=0.04)
        self.button_rotate.place(relx=0.07, rely=0.05, relheight=0.04)
        self.button_translate.place(relx=0.137, rely=0.05, relheight=0.04)
        """=========================================="""
        # Objects buttons: teapot  
        teapot = PhotoImage(file = './teapot.png').subsample(4, 3)
        cube = PhotoImage(file = './cube.png').subsample(5, 8)
        sphere = PhotoImage(file = './sphere.png').subsample(5, 8)
        self.button_teapot['image'] = teapot
        self.button_teapot.place(relx=0.01, relwidth=0.98, rely=0.01, relheight=0.1)
        self.button_cube['image'] = cube    
        self.button_cube.place(relx=0.01, relwidth=0.98, rely=0.12, relheight=0.1)
        self.button_sphere['image'] = sphere
        self.button_sphere.place(relx=0.01, relwidth=0.98, rely=0.23, relheight=0.1)
        # self.button_teapot3['image'] = teapot
        # self.button_teapot3.place(relx=0.01, relwidth=0.98, rely=0.22)
        # self.button_teapot4['image'] = teapot
        # self.button_teapot4.place(relx=0.01, relwidth=0.98, rely=0.29)
        # self.button_teapot5['image'] = teapot
        # self.button_teapot5.place(relx=0.01, relwidth=0.98, rely=0.36)
        # self.button_teapot6['image'] = teapot
        # self.button_teapot6.place(relx=0.01, relwidth=0.98, rely=0.43)
        # self.button_teapot7['image'] = teapot
        # self.button_teapot7.place(relx=0.01, relwidth=0.98, rely=0.5)
        """=========================================="""
        self.frame_shape.place(relx=0.01, rely=0.01, relwidth=0.99, relheight=0.17)
        self.frame_projection.place(relx=0.01, rely=0.19, relwidth=0.99, relheight=0.25)
        self.frame_light.place(relx=0.01, rely=0.45, relwidth=0.99, relheight=0.17)
        self.frame_fog.place(relx=0.01, rely=0.63, relwidth=0.99, relheight=0.113)
        self.frame_texture.place(relx=0.01, rely=0.753, relwidth=0.99, relheight=0.113)
        self.frame_effect.place(relx=0.01, rely=0.876, relwidth=0.99, relheight=0.113)

        self.frame_draw.place(relx=0.25, rely=0.1, relwidth=0.74, relheight=0.89)
        self.button_test_1.place(relx=0.02, rely=0.7, relwidth=0.05, relheight=0.05)
        self.exit_button.place(relx=0.965, relwidth=0.035, relheight=0.04)
        self.root.mainloop()

    def load_scale_board(self):
        if self.object_drawing is not None:
            self.scale_mode += 1
            if self.scale_mode % 2 != 0:
                # self.object_drawing.active_scale = True
                self.object_drawing.aphinType = 0
                self.object_drawing.isScaleFirst = 1
                self.frame_scale_board = Frame(self.object_drawing)
                self.frame_scale_board.place(relx=0.01, rely=0.75, relwidth=0.2, relheight=0.24)
                label_X = Label(self.frame_scale_board, text='X')
                label_X.place(relx=0.2, rely=0.17)
                label_Y = Label(self.frame_scale_board, text='Y')
                label_Y.place(relx=0.2, rely=0.47)
                label_Z= Label(self.frame_scale_board, text='Z')
                label_Z.place(relx=0.2, rely=0.77)

                scaleX = Scale(self.frame_scale_board, variable = self.object_drawing.varScale[0], orient='horizontal', from_=1, to=10, resolution=0.01)
                scaleX.place(relx=0.4, rely=0.05)
                scaleY = Scale(self.frame_scale_board, variable = self.object_drawing.varScale[1], orient='horizontal', from_=1, to=10, resolution=0.01)
                scaleY.place(relx=0.4, rely=0.35)
                scaleZ = Scale(self.frame_scale_board, variable = self.object_drawing.varScale[2], orient='horizontal', from_=1, to=10, resolution=0.01)
                scaleZ.place(relx=0.4, rely=0.65)
                self.scale_mode = True
            if self.scale_mode % 2 == 0:
                try:
                    self.frame_scale_board.destroy()
                    self.object_drawing.aphinType = -1
                    self.object_drawing.active_scale = False
                except AttributeError:
                    pass

    def rotate(self):
        try:
            self.object_drawing.aphinType = 1
            self.object_drawing.isRotateFirst = 1
            self.object_drawing.bind('<B1-Motion>', self.object_drawing.tkAphin)
        except AttributeError:
            pass

    def translate(self):
        try:
            self.object_drawing.aphinType = 2
            self.object_drawing.isTranslateFirst = 1
            self.object_drawing.bind('<B1-Motion>', self.object_drawing.tkAphin)
        except AttributeError:
            pass


    def clear_screen(self):
        for frame in self.frames_using:
            frame.destroy()
        self.object_drawing = None
        self.scale_mode = 0


    def make_object(self, obj):
        self.object_drawing = Draw(obj, False, 'face', self.frame_draw)
        self.object_drawing.animate = 1
        self.object_drawing.place(relwidth = 1, relheight=1)
        self.object_drawing.bind('<B1-Motion>', self.object_drawing.tkSizeObject)
        self.frames_using.append(self.object_drawing)
        self.scale_mode = 0


    def run(self):
        self.screenMain_Load()

if __name__ == '__main__':
    glutInit()
    app = App3D()
    app.run()

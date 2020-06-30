from tkinter import *
import tkinter.messagebox as mbox
from shape import drawObject
from pyopengltk import OpenGLFrame
from tkinter.filedialog import Open
from tkinter.filedialog import askopenfilename
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from test3 import Draw
from PIL import Image
import os

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
        # Transform Buttons (root): Scale, Rotate, Translate
        # Scale
        self.scale_mode = 0
        self.button_scale = Button(self.root, bg='#fffc33', text='SCALE', command=self.load_scale_board)
        # Rotate
        self.button_rotate = Button(self.root, bg='#8fd6de', text='ROTATE', command=self.rotate)
        # Translate
        self.button_translate = Button(self.root, bg='#ed7686', text='TRANSLATE', command=self.translate)

        """=========================================="""
        # Objects Buttons (options 1): Teapot, Cube, Sphere
        self.button_object_before = None
        # Teapot   
        self.button_teapot = Button(self.frame_options_1, activebackground='#c9e2f8', command=lambda:self.make_object('teapot', self.button_teapot))
        # Cube
        self.button_cube = Button(self.frame_options_1, activebackground='#c9e2f8', command=lambda:self.make_object('cube', self.button_cube))
        # Sphere
        self.button_sphere = Button(self.frame_options_1, activebackground='#c9e2f8', command=lambda:self.make_object('sphere', self.button_sphere))
        # Cylinder
        self.button_cylinder = Button(self.frame_options_1, activebackground='#c9e2f8', command=lambda:self.make_object('cylinder', self.button_cylinder))
        # Torus
        self.button_torus = Button(self.frame_options_1, activebackground='#c9e2f8', command=lambda:self.make_object('torus', self.button_torus))
        # Cone
        self.button_cone = Button(self.frame_options_1, activebackground='#c9e2f8', command=lambda:self.make_object('cone', self.button_cone))
        self.button_teapot6 = Button(self.frame_options_1, command=lambda:self.make_object('teapot'))
        self.button_teapot7 = Button(self.frame_options_1, command=lambda:self.make_object('teapot'))

        """=========================================="""
        # SHAPE Options (options 2): Line, Point, Face
        def test():
            pass
        var = IntVar()
        self.shape_var = StringVar()
        self.frame_shape = LabelFrame(self.frame_options_2, bg='#EBE5E9', text='Shape')
        point = Radiobutton(self.frame_shape, bg='#EBE5E9', state='disable', text="Point", variable=self.shape_var, value='points', command=self.transfer_points)
        point.place(relx=0.2, rely=0.07, relheight=0.2)
        line = Radiobutton(self.frame_shape, bg='#EBE5E9', state='disable', text="Line", variable=self.shape_var, value='lines', command=self.transfer_lines)            
        line.place(relx=0.2, rely = 0.4, relheight=0.2)
        face = Radiobutton(self.frame_shape, bg='#EBE5E9', state='disable', text="Face", variable=self.shape_var, value='face', command=self.transfer_face)
        face.place(relx=0.2, rely = 0.73, relheight=0.2)
        self.shape_options = [point, line, face]

        """=========================================="""
        # PROJECTIONS Options (options 2): Perspective, Look At (Eye), Look At (Center), Look At(Up)
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
        # LIGHT Options (options 2): Light, Light Source, Shadow
        self.light_mode = IntVar()
        self.frame_light = LabelFrame(self.frame_options_2, bg='#EBE5E9', text='Light')
        light = Checkbutton(self.frame_light, bg='#EBE5E9', text='Light', variable=self.light_mode, onvalue=1, offvalue=-1, command=self.turn_light, state='disable')
        light.place(relx=0.2, rely=0.07, relheight=0.2)

        light_source = Checkbutton(self.frame_light, bg='#EBE5E9', text='Light Source', variable=self.light_mode, onvalue=2, offvalue=-1, command=self.turn_light, state='disable')
        light_source.place(relx=0.2, rely=0.4, relheight=0.2)
        
        shadow = Checkbutton(self.frame_light, bg='#EBE5E9', text='Shadow', variable=var)
        shadow.place(relx=0.2, rely=0.73, relheight=0.2)
        
        self.light_options = [light, light_source, shadow]
        """=========================================="""
        # Fog Option (options 2): Fog
        self.frame_fog = LabelFrame(self.frame_options_2, bg='#EBE5E9', text='Fog')
        fog = Checkbutton(self.frame_fog, bg='#EBE5E9', text='Fog', variable=var)
        fog.place(relx=0.2, rely=0.07, relheight=0.86)
        """=========================================="""
        # Texture Option (options 2): Texture
        self.texture_mode = IntVar()
        self.frame_texture = LabelFrame(self.frame_options_2, bg='#EBE5E9', text='Texture')
        texture = Checkbutton(self.frame_texture, bg='#EBE5E9', text='Texture', variable=self.texture_mode, onvalue=1, offvalue=-1, command=self.turn_texture, state='disable')
        texture.place(relx=0.2, rely=0.07, relheight=0.86)
        self.texture_options = [texture]
        """=========================================="""
        # Effect Option (options 2): Effect
        self.rotating_mode = IntVar()
        self.frame_effect = LabelFrame(self.frame_options_2, bg='#EBE5E9', text='Effect')
        effect = Checkbutton(self.frame_effect, bg='#EBE5E9', text='Rotating', variable=self.rotating_mode, onvalue=1, offvalue=-1, command=self.turn_rotating, state='disable')
        effect.place(relx=0.2, rely=0.07, relheight=0.86)
        self.rotating_options = [effect]
        """=========================================="""
        # Draw frame
        self.frame_draw = Frame(self.root, bg='#000000')  # Draw here
 
        # Exit
        self.exit_button = Button(self.root, text='X', command=self.root.quit)

        # Clear
        self.button_clear = Button(self.root, text='CLEAR', command=self.clear_screen)
        """=========================================="""
        

    """++++++++++++++++++++++++++++++++++++++++++"""
    def screenMain_Load(self):
        self.button_clear.place(relx=0.22, rely=0.05, relwidth=0.05, relheight=0.04)
        # Transform buttons: scale, rotate, translate
        self.button_scale.place(relx=0.01, rely=0.05, relheight=0.04)
        self.button_rotate.place(relx=0.07, rely=0.05, relheight=0.04)
        self.button_translate.place(relx=0.137, rely=0.05, relheight=0.04)
        """=========================================="""
        # Objects buttons: teapot  
        # Images
        teapot = PhotoImage(file = './imgs/teapot.png').subsample(5, 4)
        cube = PhotoImage(file = './imgs/cube.png').subsample(9, 10)
        sphere = PhotoImage(file = './imgs/sphere.png').subsample(8, 10)
        cylinder = PhotoImage(file = './imgs/cylinder.png').subsample(4, 6)    
        torus = PhotoImage(file = './imgs/torus.png').subsample(7, 8)    
        cone = PhotoImage(file = './imgs/cone.png').subsample(4, 7)   
        # Buttons
        # Teapot
        self.button_teapot['image'] = teapot
        self.button_teapot.place(relx=0.01, relwidth=0.98, rely=0.01, relheight=0.1)
        # Cube
        self.button_cube['image'] = cube    
        self.button_cube.place(relx=0.01, relwidth=0.98, rely=0.12, relheight=0.1)
        # Sphere
        self.button_sphere['image'] = sphere
        self.button_sphere.place(relx=0.01, relwidth=0.98, rely=0.23, relheight=0.1)
        # Cylinder
        self.button_cylinder['image'] = cylinder
        self.button_cylinder.place(relx=0.01, relwidth=0.98, rely=0.34, relheight=0.1)
        # Torus
        self.button_torus['image'] = torus
        self.button_torus.place(relx=0.01, relwidth=0.98, rely=0.45, relheight=0.1)
        # Cone
        self.button_cone['image'] = cone
        self.button_cone.place(relx=0.01, relwidth=0.98, rely=0.56, relheight=0.1)
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
        self.exit_button.place(relx=0.965, relwidth=0.035, relheight=0.04)
        self.root.mainloop()

    def transfer_lines(self):
            self.object_drawing.typeDraw = self.shape_var.get()

    def transfer_points(self):
            self.object_drawing.typeDraw = self.shape_var.get()

    def transfer_face(self):
            self.object_drawing.typeDraw = self.shape_var.get()
    """++++++++++++++++++++++++++++++++++++++++++"""
    # SCALE components
    # Load scale board when click on scale button
    def load_scale_board(self):
        try:
            self.scale_mode += 1
            if self.scale_mode % 2 != 0:
                self.object_drawing.aphinType = 0
                self.object_drawing.isScaleFirst = 1
                # Frame: scale board
                self.frame_scale_board = LabelFrame(self.object_drawing, text='Scale Ratio', cursor='arrow')
                self.frame_scale_board.place(relx=0.01, rely=0.7, relwidth=0.34, relheight=0.29)

                # Button --> Set as default
                button_set_as_default = Button(self.frame_scale_board, text='Set as default', command=self.set_as_default)
                button_set_as_default.place(relx=0.6, relwidth=0.39)

                # Line black --> magical
                frame_LineBlack = Frame(self.frame_scale_board, bg='#000000')
                frame_LineBlack.place(relx=0.52, rely=0.34, relheight=0.7)

                # Entries --> Fill X, Y, Z ratio
                entry_X = Entry(self.frame_scale_board)
                entry_X.place(relx=0.55, rely=0.37, relwidth=0.2, relheight=0.11)

                entry_Y = Entry(self.frame_scale_board)
                entry_Y.place(relx=0.55, rely=0.61, relwidth=0.2, relheight=0.11)

                entry_Z = Entry(self.frame_scale_board)
                entry_Z.place(relx=0.55, rely=0.86, relwidth=0.2, relheight=0.11)

                self.entries_list = [entry_X, entry_Y, entry_Z]    

                # Buttons --> Get X, Y, Z from entries and set 
                button_set_X = Button(self.frame_scale_board, text='Set', command=lambda:self.set_ratio(self.entries_list[0], 'X'))
                button_set_X.place(relx=0.8, rely=0.37, relwidth=0.19, relheight=0.11)

                button_set_Y = Button(self.frame_scale_board, text='Set', command=lambda:self.set_ratio(self.entries_list[1], 'Y'))
                button_set_Y.place(relx=0.8, rely=0.61, relwidth=0.19, relheight=0.11)

                button_set_Z= Button(self.frame_scale_board, text='Set', command=lambda:self.set_ratio(self.entries_list[-1], 'Z'))
                button_set_Z.place(relx=0.8, rely=0.86, relwidth=0.19, relheight=0.11)

                # Labels --> Show text: X, Y, X
                label_X = Label(self.frame_scale_board, text='X')
                label_X.place(relx=0.1, rely=0.38)

                label_Y = Label(self.frame_scale_board, text='Y')
                label_Y.place(relx=0.1, rely=0.62)

                label_Z = Label(self.frame_scale_board, text='Z')
                label_Z.place(relx=0.1, rely=0.87)

                # Scale bars --> Show scale bars: X, Y, Z
                scaleX = Scale(self.frame_scale_board, variable = self.object_drawing.varScale[0], orient='horizontal', from_=0, to=10, resolution=0.01)
                scaleX.set(1)
                scaleX.place(relx=0.2, rely=0.25, relheight=0.24)

                scaleY = Scale(self.frame_scale_board, variable = self.object_drawing.varScale[1], orient='horizontal', from_=0, to=10, resolution=0.01)
                scaleY.set(1)
                scaleY.place(relx=0.2, rely=0.5, relheight=0.24)

                scaleZ = Scale(self.frame_scale_board, variable = self.object_drawing.varScale[2], orient='horizontal', from_=0, to=10, resolution=0.01)
                scaleZ.set(1)
                scaleZ.place(relx=0.2, rely=0.75, relheight=0.24)

                self.scale_ratio = [scaleX, scaleY, scaleZ]
                self.scale_mode = True
            if self.scale_mode % 2 == 0:
                try:
                    self.frame_scale_board.destroy()
                except AttributeError:
                    pass
        except AttributeError:
            pass
    
    # Set from keyboard
    def set_ratio(self, entry, axis):
        tmp = entry.get()
        if float(tmp) < 0 or float(tmp) > 10:
            mbox.showerror("Error", "Ratio should be between 0 and 10!")
        else:
            if axis == 'X':
                self.scale_ratio[0].set(tmp)
            elif axis == 'Y':
                self.scale_ratio[1].set(tmp)
            elif axis == 'Z':
                self.scale_ratio[-1].set(tmp)
    
    # Set as default
    def set_as_default(self):
        for ratio in self.scale_ratio:
            ratio.set(1)
    """++++++++++++++++++++++++++++++++++++++++++"""
    # ROTATE components
    def rotate(self):
        try:
            self.object_drawing.aphinType = 1
            self.object_drawing.isRotateFirst = 1
            self.object_drawing.bind('<B1-Motion>', self.object_drawing.tkAphin)
            self.object_drawing['cursor'] = 'exchange'
        except AttributeError:
            pass
    """++++++++++++++++++++++++++++++++++++++++++"""
    # TRANSLATE components
    def translate(self):
        try:
            self.object_drawing.aphinType = 2
            self.object_drawing.isTranslateFirst = 1
            self.object_drawing.bind('<B1-Motion>', self.object_drawing.tkAphin)
            self.object_drawing['cursor'] = 'fleur'
        except AttributeError:
            pass
    """++++++++++++++++++++++++++++++++++++++++++"""
    # LIGHT components
    def turn_light(self):
        try:
            self.object_drawing.toggleLight = self.light_mode.get()
            self.object_drawing['cursor'] = 'arrow'
            if self.object_drawing.toggleLight == 2:
                self.object_drawing.aphinType = 3
                self.object_drawing.bind('<B1-Motion>', self.object_drawing.tkAphin)
        except AttributeError:
            pass
    """++++++++++++++++++++++++++++++++++++++++++"""
    # TEXTURE components
    def turn_texture(self):
        try:
            if self.texture_mode.get() == 1:
                path_current = os.getcwd()
                path =  askopenfilename(initialdir = f"{path_current}/textures",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
                self.object_drawing.toggleTextures = 1
                self.object_drawing['cursor'] = 'arrow'
                image = Image.open(f'{path}')
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
                self.object_drawing.imageWHTex = (image.width, image.height)
                self.object_drawing.imgDataTex = image.convert("RGBA").tobytes()
                self.object_drawing.textureDraw = glGenTextures(1)
            else:
                self.object_drawing.toggleTextures = -1
                
        except AttributeError:
            pass

    def turn_rotating(self):
        try:
            self.object_drawing.toggleRotating = self.rotating_mode.get()
        except AttributeError:
            pass

    """++++++++++++++++++++++++++++++++++++++++++"""
    def clear_screen(self):
        try:
            self.object_drawing.destroy()
            self.button_object_before['highlightbackground'] = '#d9d9d9'
            self.button_object_before['bg'] = '#d9d9d9'
            self.button_object_before = None
            self.object_drawing = None
        except AttributeError:
            pass
        self.scale_mode = 0
        # Disable choices in options
        for options in self.shape_options:
            options.deselect()
            options['state'] = 'disable'
        for options in self.light_options:
            options.deselect()
            options['state'] = 'disable'
        for options in self.texture_options:
            options.deselect()
            options['state'] = 'disable'
        for options in self.rotating_options:
            options.deselect()
            options['state'] = 'disable'
            

    """++++++++++++++++++++++++++++++++++++++++++"""
    def make_object(self, obj, button):
        try:
            self.object_drawing.destroy()
            self.button_object_before['highlightbackground'] = '#d9d9d9' # Set default color
            self.button_object_before['bg'] = '#d9d9d9'
        except AttributeError:
            pass
        for options in self.shape_options:
            options.deselect()
        for options in self.light_options:
            options.deselect()
        for options in self.texture_options:
            options.deselect()
        for options in self.rotating_options:
            options.deselect()    
            
        self.button_object_before = button
        button['highlightbackground'] = '#236aa9'
        button['bg'] = '#c9e2f8'
        self.object_drawing = Draw(obj, False, -1, 'face', self.frame_draw)
        self.object_drawing.animate = 1
        
        self.object_drawing.place(relwidth = 1, relheight=1)
        self.object_drawing.bind('<B1-Motion>', self.object_drawing.tkSizeObject)
        self.object_drawing['cursor'] = 'cross'
        self.scale_mode = 0
        for options in self.shape_options:
            options['state'] = 'active'
        for options in self.light_options:
            options['state'] = 'active'
        for options in self.texture_options:
            options['state'] = 'active'
        for options in self.rotating_options:
            options['state'] = 'active'
        self.shape_options[-1].select()


    def run(self):
        self.screenMain_Load()

if __name__ == '__main__':
    glutInit()
    app = App3D()
    app.run()

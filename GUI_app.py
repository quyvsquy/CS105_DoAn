from tkinter import *
import tkinter.messagebox as mbox
from shape import drawObject
from tkinter.filedialog import askopenfilename
from tkinter.colorchooser import askcolor
import numpy as np
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from test3 import Draw
from PIL import Image
import os
# import pkg_resources.py2_warn #for build file execute ubuntu

def exit(obj):
    obj.destroy()

class App3D:
    def __init__(self):
        self.root = Tk()
        self.root.attributes("-fullscreen", True)

        self.object_drawing = None
        self.board_using = []

        # Objects Frame --> contains objects buttons 
        self.frame_objects = Frame(self.root, bg='#EBE5E9')
        self.frame_objects.place(relx=0.01, rely=0.1, relwidth=0.08, relheight=0.89)

        # Options Frame
        self.frame_options = Frame(self.root, bg='#EBE5E9')
        self.frame_options.place(relx=0.1, rely=0.1, relwidth=0.14, relheight=0.89)
        """-----------------------------------------"""
        """Upper Toolbar"""
        # Buttons: Scale, Rotate, Translate
        self.scale_mode = 0
        self.button_scale = Button(self.root, bg='#e1f281', text='SCALE', activebackground='#b0cf04', command=self.load_scale_board)

        self.button_rotate = Button(self.root, bg='#aef9f8', text='ROTATE', activebackground='#07cdcb', command=self.rotate)

        self.button_translate = Button(self.root, bg='#fec282', text='TRANSLATE', activebackground='#ff8e14', command=self.translate)

        # Button: Color
        self.button_choose_color = Button(self.root, bg='#b0f098', text='COLOR', activebackground='#298107', command=self.load_color_board)
        
        # Button: Clear
        self.button_clear = Button(self.root, text='CLEAR', bg='#88809b', command=self.clear_screen)
        """-----------------------------------------"""
        # Buttons (Objects): Teapot, Cube, Sphere, Cylinder, Torus, Cone, Pyramid, Truncated Cone
        self.button_object_before = None
        
        self.button_Teapot = Button(self.frame_objects, activebackground='#c9e2f8', command=lambda:self.make_object('teapot', self.button_Teapot))
        
        self.button_Cube = Button(self.frame_objects, activebackground='#c9e2f8', command=lambda:self.make_object('cube', self.button_Cube))

        self.button_Sphere = Button(self.frame_objects, activebackground='#c9e2f8', command=lambda:self.make_object('sphere', self.button_Sphere))

        self.button_Cylinder = Button(self.frame_objects, activebackground='#c9e2f8', command=lambda:self.make_object('cylinder', self.button_Cylinder))

        self.button_Torus = Button(self.frame_objects, activebackground='#c9e2f8', command=lambda:self.make_object('torus', self.button_Torus))

        self.button_Cone = Button(self.frame_objects, activebackground='#c9e2f8', command=lambda:self.make_object('cone', self.button_Cone))

        self.button_Pyramid = Button(self.frame_objects, activebackground='#c9e2f8', command=lambda:self.make_object('pyramid', self.button_Pyramid))

        self.button_TruncatedCone = Button(self.frame_objects, activebackground='#c9e2f8', command=lambda:self.make_object('truncated cone', self.button_TruncatedCone))

        """-----------------------------------------"""
        # SHAPE Options: Line, Point, Face
        self.shape_var = StringVar()
        self.frame_shape = LabelFrame(self.frame_options, bg='#EBE5E9', text='Shape')
        
        point = Radiobutton(self.frame_shape, bg='#EBE5E9', state='disable', text="Point", variable=self.shape_var, value='points', command=self.transfer_points)
        point.place(relx=0.2, rely=0.07, relheight=0.2)
        
        line = Radiobutton(self.frame_shape, bg='#EBE5E9', state='disable', text="Line", variable=self.shape_var, value='lines', command=self.transfer_lines)            
        line.place(relx=0.2, rely = 0.4, relheight=0.2)
        
        face = Radiobutton(self.frame_shape, bg='#EBE5E9', state='disable', text="Face", variable=self.shape_var, value='face', command=self.transfer_face)
        face.place(relx=0.2, rely = 0.73, relheight=0.2)
        
        self.shape_options = [point, line, face]
        """-----------------------------------------"""
        # PROJECTIONS Options (options 2): Perspective, Look At (Eye), Look At (Center), Look At(Up)
        self.projection_var = IntVar()
        self.frame_projection = LabelFrame(self.frame_options, bg='#EBE5E9', text='Projection')
        
        perspective = Radiobutton(self.frame_projection, bg='#EBE5E9', variable=self.projection_var, value=1, text="Perspective", command=self.load_projection_board, state='disable')
        perspective.place(relx=0.2, rely=0.07, relheight=0.2)
        
        lookat_eye = Radiobutton(self.frame_projection, bg='#EBE5E9', text="Look At (Eye)", variable=self.projection_var, value=2, command=self.load_projection_board, state='disable')
        lookat_eye.place(relx=0.2, rely=0.29, relheight=0.2)
        
        lookat_center = Radiobutton(self.frame_projection, bg='#EBE5E9', text="Look At (Center)", variable=self.projection_var, value=3, command=self.load_projection_board, state='disable')
        lookat_center.place(relx=0.2, rely=0.51, relheight=0.2)
        
        lookat_up = Radiobutton(self.frame_projection, bg='#EBE5E9', text="Look At (Up)", variable=self.projection_var, value=4, command=self.load_projection_board, state='disable')
        lookat_up.place(relx=0.2, rely=0.73, relheight=0.2)
        
        self.projection_options = [perspective, lookat_eye, lookat_center, lookat_up]
        """-----------------------------------------"""
        # LIGHT Options (options 2): Light, Light Source, Shadow
        self.light_mode = IntVar()
        self.frame_light = LabelFrame(self.frame_options, bg='#EBE5E9', text='Light')
        light = Checkbutton(self.frame_light, bg='#EBE5E9', text='Light', variable=self.light_mode, onvalue=1, offvalue=-1, command=self.turn_light, state='disable')
        light.place(relx=0.2, rely=0.07, relheight=0.2)

        light_source = Checkbutton(self.frame_light, bg='#EBE5E9', text='Light Source', variable=self.light_mode, onvalue=2, offvalue=-1, command=self.turn_light, state='disable')
        light_source.place(relx=0.2, rely=0.4, relheight=0.2)
        
        shadow = Checkbutton(self.frame_light, bg='#EBE5E9', text='Shadow', variable=self.projection_var)
        # shadow.place(relx=0.2, rely=0.73, relheight=0.2)
        
        self.light_options = [light, light_source, shadow]
        """-----------------------------------------"""
        # Fog Option (options 2): Fog
        self.frame_fog = LabelFrame(self.frame_options, bg='#EBE5E9', text='Fog')
        fog = Checkbutton(self.frame_fog, bg='#EBE5E9', text='Fog', variable=self.projection_var)
        fog.place(relx=0.2, rely=0.07, relheight=0.86)
        """-----------------------------------------"""
        # TEXTURE Option (options 2): Texture
        self.texture_mode = IntVar()
        self.frame_texture = LabelFrame(self.frame_options, bg='#EBE5E9', text='Texture')
        texture = Checkbutton(self.frame_texture, bg='#EBE5E9', text='Texture', variable=self.texture_mode, onvalue=1, offvalue=-1, command=self.turn_texture, state='disable')
        texture.place(relx=0.2, rely=0.07, relheight=0.86)
        self.texture_options = [texture]
        """-----------------------------------------"""
        # EFFECT Option (options 2): Effect
        self.rotating_mode = IntVar()
        self.frame_effect = LabelFrame(self.frame_options, bg='#EBE5E9', text='Effect')
        effect = Checkbutton(self.frame_effect, bg='#EBE5E9', text='Rotating', variable=self.rotating_mode, onvalue=1, offvalue=-1, command=self.turn_rotating, state='disable')
        effect.place(relx=0.2, rely=0.07, relheight=0.86)
        self.rotating_options = [effect]
        """-----------------------------------------"""
        # Draw frame
        self.frame_draw = Frame(self.root, bg='#000000')  # Draw here
 
        # Exit
        self.exit_button = Button(self.root, text='X', bg='#e2280a', fg='#ffffff', font='12', command=self.root.quit)
        """-----------------------------------------"""
    """++++++++++++++++++++++++++++++++++++++++++"""
    def screenMain_Load(self):
        """Upper Toolbar"""
        # Buttons: Scale, Rotate, Translate
        self.button_scale.place(relx=0.01, rely=0.05, relwidth=0.05, relheight=0.04)
        self.button_rotate.place(relx=0.07, rely=0.05, relwidth=0.06, relheight=0.04)
        self.button_translate.place(relx=0.14, rely=0.05, relwidth=0.09, relheight=0.04)
        
        # Button: Color
        self.button_choose_color.place(relx=0.24, rely=0.05, relwidth=0.05, relheight=0.04)
        
        # Button: Clear
        self.button_clear.place(relx=0.3, rely=0.05, relwidth=0.05, relheight=0.04)
        """-----------------------------------------"""
        # Objects buttons: teapot  
        # Images
        teapot = PhotoImage(file = './imgs/teapot.png').subsample(8,8)
        cube = PhotoImage(file = './imgs/cube.png').subsample(8,8)
        sphere = PhotoImage(file = './imgs/sphere.png').subsample(8, 8)
        cylinder = PhotoImage(file = './imgs/cylinder.png').subsample(8, 8)    
        torus = PhotoImage(file = './imgs/torus.png').subsample(8, 8)    
        cone = PhotoImage(file = './imgs/cone.png').subsample(8, 8) 
        pyramid = PhotoImage(file = './imgs/pyramid.png').subsample(8, 8) 
        truncated_cone = PhotoImage(file = './imgs/truncatedcone.png').subsample(8, 8) 
        # Buttons
        # Teapot
        objects_y = 0.03
        self.button_Teapot['image'] = teapot
        self.button_Teapot.place(relx=0.01, relwidth=0.98, rely=objects_y, relheight=0.1)
        # Cube
        self.button_Cube['image'] = cube    
        self.button_Cube.place(relx=0.01, relwidth=0.98, rely=objects_y + 0.1 + 0.02, relheight=0.1)
        # Sphere
        self.button_Sphere['image'] = sphere
        self.button_Sphere.place(relx=0.01, relwidth=0.98, rely=objects_y + 0.1*2 + 0.02*2, relheight=0.1)
        # Cylinder
        self.button_Cylinder['image'] = cylinder
        self.button_Cylinder.place(relx=0.01, relwidth=0.98, rely=objects_y + 0.1*3 + 0.02*3, relheight=0.1)
        # Torus
        self.button_Torus['image'] = torus
        self.button_Torus.place(relx=0.01, relwidth=0.98, rely=objects_y + 0.1*4 + 0.02*4, relheight=0.1)
        # Cone
        self.button_Cone['image'] = cone
        self.button_Cone.place(relx=0.01, relwidth=0.98, rely=objects_y + 0.1*5 + 0.02*5, relheight=0.1)
        # Pyramid
        self.button_Pyramid['image'] = pyramid
        self.button_Pyramid.place(relx=0.01, relwidth=0.98, rely=objects_y + 0.1*6 + 0.02*6, relheight=0.1)
        # Truncated Cone
        self.button_TruncatedCone['image'] = truncated_cone
        self.button_TruncatedCone.place(relx=0.01, relwidth=0.98, rely=objects_y + 0.1*7 + 0.02*7, relheight=0.1)
        """-----------------------------------------"""
        self.frame_shape.place(relx=0.01, rely=0.01, relwidth=0.99, relheight=0.17)

        self.frame_projection.place(relx=0.01, rely=0.19, relwidth=0.99, relheight=0.25)
        
        self.frame_light.place(relx=0.01, rely=0.45, relwidth=0.99, relheight=0.17)
        
        # self.frame_fog.place(relx=0.01, rely=0.63, relwidth=0.99, relheight=0.113)
        
        self.frame_texture.place(relx=0.01, rely=0.753, relwidth=0.99, relheight=0.113)
        
        self.frame_effect.place(relx=0.01, rely=0.876, relwidth=0.99, relheight=0.113)

        self.frame_draw.place(relx=0.25, rely=0.1, relwidth=0.74, relheight=0.89)
        
        self.exit_button.place(relx=0.97, relwidth=0.03, relheight=0.04)
        
        self.root.mainloop()
    """++++++++++++++++++++++++++++++++++++++++++"""
    def transfer_lines(self):
            self.object_drawing.typeDraw = self.shape_var.get()

    def transfer_points(self):
            self.object_drawing.typeDraw = self.shape_var.get()

    def transfer_face(self):
            self.object_drawing.typeDraw = self.shape_var.get()
    """++++++++++++++++++++++++++++++++++++++++++"""
    """SCALE"""
    # Load scale board when click on scale button
    def load_scale_board(self):
        try:
            for board in self.board_using:
                board.destroy()
            self.aphinType_pre = self.object_drawing.aphinType
            self.color_before = '#e1f281'
            self.button_scale['bg'] = '#b0cf04'
            self.object_drawing.aphinType = 0
            self.object_drawing.isScaleFirst = 1
            # Frame: scale board
            self.frame_scale_board = Frame(self.object_drawing, cursor='arrow')
            self.frame_scale_board.place(relx=0.01, rely=0.67, relwidth=0.34, relheight=0.32)
            
            self.board_using.append(self.frame_scale_board)
            
            # Label: Name of the Board
            label_name = Label(self.frame_scale_board, bg='#81dbd0', justify='left', text='Scale Board')
            label_name.place(relwidth=1, relheight=0.1)

            # Button --> Exit
            button_exit = Button(self.frame_scale_board, text='X', command=self.exit_scale_mode)
            button_exit.place(relx=0.91, relwidth=0.09, relheight=0.1)

            pos_buttons_y = 0.18
            # Button --> Set as default
            button_Set_as_default = Button(self.frame_scale_board, text='Set as default', command=self.set_as_default)
            button_Set_as_default.place(relx=0.05, rely=pos_buttons_y, relwidth=0.39)

            # Buton: Save
            button_Save = Button(self.frame_scale_board, text='Save', command=self.save)
            button_Save.place(relx=0.45, rely=pos_buttons_y, relwidth=0.245)

            # Button: Cancel
            button_Cancel = Button(self.frame_scale_board, text='Cancel', command=self.cancel)
            button_Cancel.place(relx=0.705, rely=pos_buttons_y, relwidth=0.245)

            # Labels --> Show text: X, Y, X
            pos_labels_x = 0.1
            pos_labels_y = 0.43
            label_X = Label(self.frame_scale_board, text='X')
            label_X.place(relx=pos_labels_x, rely=pos_labels_y)

            label_Y = Label(self.frame_scale_board, text='Y')
            label_Y.place(relx=pos_labels_x, rely=pos_labels_y + 0.24)

            label_Z = Label(self.frame_scale_board, text='Z')
            label_Z.place(relx=pos_labels_x, rely=pos_labels_y + 0.47)

            # Scale bars --> Show scale bars: X, Y, Z
            scale_bars_x = 0.2
            scale_bars_y = 0.34
            scaleX = Scale(self.frame_scale_board, variable=self.object_drawing.varScale[0], orient='horizontal', from_=-30, to=30, resolution=0.01)
            scaleX.set(self.object_drawing.varScale[0].get())
            scaleX.place(relx=scale_bars_x, rely=scale_bars_y, relheight=0.2)

            scaleY = Scale(self.frame_scale_board, variable=self.object_drawing.varScale[1], orient='horizontal', from_=-30, to=30, resolution=0.01)
            scaleY.set(self.object_drawing.varScale[1].get())
            scaleY.place(relx=scale_bars_x, rely=scale_bars_y + 0.2 + 0.03, relheight=0.2)

            scaleZ = Scale(self.frame_scale_board, variable=self.object_drawing.varScale[2], orient='horizontal', from_=-30, to=30, resolution=0.01)
            scaleZ.set(self.object_drawing.varScale[2].get())
            scaleZ.place(relx=scale_bars_x, rely=scale_bars_y + 0.2 * 2 + 0.03 * 2, relheight=0.2)

            self.scale_ratio = [scaleX, scaleY, scaleZ]

            # Line black
            frame_LineBlack = Frame(self.frame_scale_board, bg='#000000')
            frame_LineBlack.place(relx=0.52, rely=0.4, relheight=0.6)

            # Entries --> Fill X, Y, Z ratio
            entry_X = Entry(self.frame_scale_board)
            entry_X.place(relx=0.55, rely=0.43, relwidth=0.2, relheight=0.1)

            entry_Y = Entry(self.frame_scale_board)
            entry_Y.place(relx=0.55, rely=0.66, relwidth=0.2, relheight=0.1)

            entry_Z = Entry(self.frame_scale_board)
            entry_Z.place(relx=0.55, rely=0.88, relwidth=0.2, relheight=0.1)

            self.entries_list = [entry_X, entry_Y, entry_Z]    

            # Buttons --> Get X, Y, Z from entries and set 
            button_Set_X = Button(self.frame_scale_board, text='Set', command=lambda:self.set_scale_ratio(self.entries_list[0], 'X'))
            button_Set_X.place(relx=0.8, rely=0.43, relwidth=0.19, relheight=0.1)

            button_Set_Y = Button(self.frame_scale_board, text='Set', command=lambda:self.set_scale_ratio(self.entries_list[1], 'Y'))
            button_Set_Y.place(relx=0.8, rely=0.66, relwidth=0.19, relheight=0.1)

            button_Set_Z = Button(self.frame_scale_board, text='Set', command=lambda:self.set_scale_ratio(self.entries_list[-1], 'Z'))
            button_Set_Z.place(relx=0.8, rely=0.88, relwidth=0.19, relheight=0.1)
        except AttributeError:
            pass

    def exit_scale_mode(self):
        self.object_drawing.varScale[0].set(self.object_drawing.varScale_tmp[0].get())
        self.object_drawing.varScale[1].set(self.object_drawing.varScale_tmp[1].get())
        self.object_drawing.varScale[2].set(self.object_drawing.varScale_tmp[2].get())
        self.button_scale['bg'] = self.color_before
        self.frame_scale_board.destroy()
        if self.aphinType_pre != -1:
            self.object_drawing.aphinType = self.aphinType_pre

    # Set from keyboard
    def set_scale_ratio(self, entry, axis):
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
        mbox.showinfo("Info", f"Successfully!\nScale X: 1\nScale Y: 1\nScale Z: 1")

    def save(self):
        mbox.showinfo("Info", f"Save successfully!\nScale X: {self.object_drawing.varScale[0].get()}\nScale Y: {self.object_drawing.varScale[1].get()}\nScale Z: {self.object_drawing.varScale[2].get()}")
        self.object_drawing.varScale_tmp[0].set(self.object_drawing.varScale[0].get())
        self.object_drawing.varScale_tmp[1].set(self.object_drawing.varScale[1].get())
        self.object_drawing.varScale_tmp[2].set(self.object_drawing.varScale[2].get())

    def cancel(self):
        self.object_drawing.varScale[0].set(self.object_drawing.varScale_tmp[0].get())
        self.object_drawing.varScale[1].set(self.object_drawing.varScale_tmp[1].get())
        self.object_drawing.varScale[2].set(self.object_drawing.varScale_tmp[2].get())
    """++++++++++++++++++++++++++++++++++++++++++"""
    """ ROTATE """
    def rotate(self):
        try:
            self.object_drawing.aphinType = 1
            self.object_drawing.isRotateFirst = 1
            self.object_drawing.bind('<B1-Motion>', self.object_drawing.tkAphin)
            self.object_drawing['cursor'] = 'exchange'
        except AttributeError:
            pass
    """++++++++++++++++++++++++++++++++++++++++++"""
    """ TRANSLATE """
    def translate(self):
        try:
            self.object_drawing.aphinType = 2
            self.object_drawing.isTranslateFirst = 1
            self.object_drawing.bind('<B1-Motion>', self.object_drawing.tkAphin)
            self.object_drawing['cursor'] = 'fleur'
        except AttributeError:
            pass
    """++++++++++++++++++++++++++++++++++++++++++"""
    """COLOR"""
    def load_color_board(self):
        if self.object_drawing is None:
            pass
        else:
            self.button_choose_color['bg'] = '#298107'
            self.object_drawing.color = np.array(askcolor(title ="Choose color")[0])
            self.button_choose_color['bg'] = '#b0f098'
    """++++++++++++++++++++++++++++++++++++++++++"""
    """ PROJECTION """
    def load_projection_board(self):
        if self.object_drawing is not None:
            for board in self.board_using:
                board.destroy()
            if self.projection_var.get() == 1:
                # Frame: perspective board
                self.frame_perspective_board = Frame(self.object_drawing, cursor='arrow')
                self.frame_perspective_board.place(relx=0.01, rely=0.6, relwidth=0.34, relheight=0.39)
               
                self.board_using.append(self.frame_perspective_board)

                # Label: Name of the Board      
                label_name = Label(self.frame_perspective_board, bg='#81dbd0', text='Perspecive', justify='left')
                label_name.place(relwidth=1, relheight=0.1)

                # Button --> Exit
                button_exit = Button(self.frame_perspective_board, text='X', command=self.exit_projective_mode)
                button_exit.place(relx=0.91, relwidth=0.09, relheight=0.1)

                buttons_y = 0.15
                # Button: Set as default --> Set as default
                button_Set_as_default = Button(self.frame_perspective_board, text='Set as default', command=self.set_as_default_)
                button_Set_as_default.place(relx=0.05, rely=buttons_y, relwidth=0.39)

                # Buton: Save
                button_Save = Button(self.frame_perspective_board, text='Save', command=self.projection_save)
                button_Save.place(relx=0.45, rely=buttons_y, relwidth=0.245)

                # Button: Cancel
                button_Cancel = Button(self.frame_perspective_board, text='Cancel', command=self.projection_cancel)
                button_Cancel.place(relx=0.705, rely=buttons_y, relwidth=0.245)

                # Labels --> Show text: Fovy, Aspect, Near, Far
                pos_labels_x = 0.04
                label_Fovy = Label(self.frame_perspective_board, text='Fovy')
                label_Fovy.place(relx=pos_labels_x, rely=0.34, relheight=0.1)

                label_Aspect = Label(self.frame_perspective_board, text='Aspect')
                label_Aspect.place(relx=pos_labels_x, rely=0.52, relheight=0.1)

                label_Near = Label(self.frame_perspective_board, text='Near')
                label_Near.place(relx=pos_labels_x, rely=0.7, relheight=0.1)

                label_Far = Label(self.frame_perspective_board, text='Far')
                label_Far.place(relx=pos_labels_x, rely=0.88, relheight=0.1)

                # Scale bars --> Show scale bars: Fovy, Aspect, Near, Far
                pos_scale_bars_x = 0.2
                scale_Fovy = Scale(self.frame_perspective_board, variable=self.object_drawing.fov, orient='horizontal', from_=-360, to=360, resolution=5)
                scale_Fovy.set(self.object_drawing.fov.get())
                scale_Fovy.place(relx=pos_scale_bars_x, rely=0.28, relheight=0.2)

                scale_Aspect = Scale(self.frame_perspective_board, variable=self.object_drawing.asp, orient='horizontal', from_=-30, to=30, resolution=0.01)
                scale_Aspect.set(self.object_drawing.asp.get())
                scale_Aspect.place(relx=pos_scale_bars_x, rely=0.46, relheight=0.2)

                scale_Near = Scale(self.frame_perspective_board, variable=self.object_drawing.zNear, orient='horizontal', from_=-30, to=30, resolution=0.01)
                scale_Near.set(self.object_drawing.zNear.get())
                scale_Near.place(relx=pos_scale_bars_x, rely=0.64, relheight=0.2)

                scale_Far = Scale(self.frame_perspective_board, variable=self.object_drawing.zFar, orient='horizontal', from_=-30, to=30, resolution=0.01)
                scale_Far.set(self.object_drawing.zFar.get())
                scale_Far.place(relx=pos_scale_bars_x, rely=0.82, relheight=0.2)

                self.scale_ratio = [scale_Fovy, scale_Aspect, scale_Near, scale_Far]

                # Line black
                frame_LineBlack = Frame(self.frame_perspective_board, bg='#000000')
                frame_LineBlack.place(relx=0.52, rely=0.3, relheight=0.7)

                # Entries --> Fill Fovy, Aspect, Near, Far ratio
                entry_Fovy = Entry(self.frame_perspective_board)
                entry_Fovy.place(relx=0.55, rely=0.34, relwidth=0.2, relheight=0.1)

                entry_Aspect = Entry(self.frame_perspective_board)
                entry_Aspect.place(relx=0.55, rely=0.52, relwidth=0.2, relheight=0.1)

                entry_Near = Entry(self.frame_perspective_board)
                entry_Near.place(relx=0.55, rely=0.7, relwidth=0.2, relheight=0.1)

                entry_Far = Entry(self.frame_perspective_board)
                entry_Far.place(relx=0.55, rely=0.88, relwidth=0.2, relheight=0.1)

                self.entries_list = [entry_Fovy, entry_Aspect, entry_Near, entry_Far]    

                # Buttons --> Get and Set: Fovy, Aspect, Near, Far from entries  
                button_Set_Fovy = Button(self.frame_perspective_board, text='Set', command=lambda:self.set_projection_ratio(self.entries_list[0], 'fovy'))
                button_Set_Fovy.place(relx=0.8, rely=0.34, relwidth=0.19, relheight=0.1)

                button_Set_Aspect = Button(self.frame_perspective_board, text='Set', command=lambda:self.set_projection_ratio(self.entries_list[1], 'aspect'))
                button_Set_Aspect.place(relx=0.8, rely=0.52, relwidth=0.19, relheight=0.1)

                button_Set_Near = Button(self.frame_perspective_board, text='Set', command=lambda:self.set_projection_ratio(self.entries_list[2], 'near'))
                button_Set_Near.place(relx=0.8, rely=0.7, relwidth=0.19, relheight=0.1)

                button_Set_Far = Button(self.frame_perspective_board, text='Set', command=lambda:self.set_projection_ratio(self.entries_list[-1], 'far'))
                button_Set_Far.place(relx=0.8, rely=0.88, relwidth=0.19, relheight=0.1)      
            else:
                # Frame: scale board
                self.frame_scale_board = Frame(self.object_drawing, cursor='arrow')
                self.frame_scale_board.place(relx=0.01, rely=0.67, relwidth=0.34, relheight=0.32)
                
                self.board_using.append(self.frame_scale_board)
                
                # Label: Name of the Board
                label_name = Label(self.frame_scale_board, bg='#81dbd0', justify='left')
                label_name.place(relwidth=1, relheight=0.1)

                # Button --> Exit
                button_exit = Button(self.frame_scale_board, text='X', command=self.exit_projective_mode)
                button_exit.place(relx=0.91, relwidth=0.09, relheight=0.1)

                pos_buttons_y = 0.18
                # Button --> Set as default
                button_Set_as_default = Button(self.frame_scale_board, text='Set as default', command=self.set_as_default_)
                button_Set_as_default.place(relx=0.05, rely=pos_buttons_y, relwidth=0.39)

                # Buton: Save
                button_Save = Button(self.frame_scale_board, text='Save', command=self.projection_save)
                button_Save.place(relx=0.45, rely=pos_buttons_y, relwidth=0.245)

                # Button: Cancel
                button_Cancel = Button(self.frame_scale_board, text='Cancel', command=self.projection_cancel)
                button_Cancel.place(relx=0.705, rely=pos_buttons_y, relwidth=0.245)

                # Labels --> Show text: X, Y, X
                labels_x = 0.1
                labels_y = 0.43
                label_X = Label(self.frame_scale_board, text='X')
                label_X.place(relx=labels_x, rely=labels_y)

                label_Y = Label(self.frame_scale_board, text='Y')
                label_Y.place(relx=labels_x, rely=labels_y + 0.24)

                label_Z = Label(self.frame_scale_board, text='Z')
                label_Z.place(relx=labels_x, rely=labels_y + 0.47)

                # Scale bars --> Show scale bars: X, Y, Z
                scale_bars_x = 0.2
                scale_bars_y = 0.34
                if self.projection_var.get() == 2:
                    label_name['text'] = 'Look at (Eye)'
                    var = [self.object_drawing.eyeX, self.object_drawing.eyeY, self.object_drawing.eyeZ]
                    boundary = [[-30, 30], [-30, 30], [-30, 30]]
                elif self.projection_var.get() == 3:
                    label_name['text'] = 'Look at (Center)'
                    var = [self.object_drawing.centerX, self.object_drawing.centerY, self.object_drawing.centerZ]
                    boundary = [[-30, 30], [-30, 30], [-30, 30]]
                else:
                    label_name['text'] = 'Look at (Up)'
                    var = [self.object_drawing.upX, self.object_drawing.upY, self.object_drawing.upZ]
                    boundary = [[-30, 30], [-30, 30], [-30, 30]]

                scaleX = Scale(self.frame_scale_board, variable=var[0], orient='horizontal', from_=boundary[0][0], to=boundary[0][1], resolution=0.01)
                scaleX.set(var[0].get())
                scaleX.place(relx=scale_bars_x, rely=scale_bars_y, relheight=0.2)

                scaleY = Scale(self.frame_scale_board, variable=var[1], orient='horizontal', from_=boundary[1][0], to=boundary[1][1], resolution=0.01)
                scaleY.set(var[1].get())
                scaleY.place(relx=scale_bars_x, rely=scale_bars_y + 0.2 + 0.03, relheight=0.2)

                scaleZ = Scale(self.frame_scale_board, variable=var[2], orient='horizontal', from_=boundary[2][0], to=boundary[2][1], resolution=0.01)
                scaleZ.set(var[2].get())
                scaleZ.place(relx=scale_bars_x, rely=scale_bars_y + 0.2 * 2 + 0.03 * 2, relheight=0.2)

                self.scale_ratio = [scaleX, scaleY, scaleZ]

                # Line black
                frame_LineBlack = Frame(self.frame_scale_board, bg='#000000')
                frame_LineBlack.place(relx=0.52, rely=0.4, relheight=0.6)

                # Entries --> Fill X, Y, Z ratio
                entry_X = Entry(self.frame_scale_board)
                entry_X.place(relx=0.55, rely=0.43, relwidth=0.2, relheight=0.1)

                entry_Y = Entry(self.frame_scale_board)
                entry_Y.place(relx=0.55, rely=0.66, relwidth=0.2, relheight=0.1)

                entry_Z = Entry(self.frame_scale_board)
                entry_Z.place(relx=0.55, rely=0.88, relwidth=0.2, relheight=0.1)

                self.entries_list = [entry_X, entry_Y, entry_Z]    

                # Buttons --> Get X, Y, Z from entries and set 
                button_Set_X = Button(self.frame_scale_board, text='Set', command=lambda:self.set_projection_ratio(self.entries_list[0], 'X'))
                button_Set_X.place(relx=0.8, rely=0.43, relwidth=0.19, relheight=0.1)

                button_Set_Y = Button(self.frame_scale_board, text='Set', command=lambda:self.set_projection_ratio(self.entries_list[1], 'Y'))
                button_Set_Y.place(relx=0.8, rely=0.66, relwidth=0.19, relheight=0.1)

                button_Set_Z = Button(self.frame_scale_board, text='Set', command=lambda:self.set_projection_ratio(self.entries_list[-1], 'Z'))
                button_Set_Z.place(relx=0.8, rely=0.88, relwidth=0.19, relheight=0.1)
                
    def exit_projective_mode(self):
        for board in self.board_using:
            board.destroy()

    def set_projection_ratio(self, entry, axis):
        tmp = entry.get()
        if axis == 'fovy':
            if float(tmp) < -360 or float(tmp) > 360:
                mbox.showerror("Error", "Ratio should be between -360 and 360!")
            elif float(tmp) - int(float(tmp)) != 0:
                mbox.showerror("Error", "Ratio should be integer number!")
            elif float(tmp) % 5 != 0:
                mbox.showerror("Error", "Ratio should be divide by 5!")
            else: 
                self.scale_ratio[0].set(float(tmp))
        elif axis == 'aspect':
            if float(tmp) < -30 or float(tmp) > 30:
                mbox.showerror("Error", "Ratio should be between -30 and 30!")
            else:
                self.scale_ratio[1].set(tmp)
        elif axis == 'near':
            if float(tmp) < -30 or float(tmp) > 30:
                mbox.showerror("Error", "Ratio should be between -30 and 30!")
            else:
                self.scale_ratio[2].set(tmp)
        elif axis == 'far':
            if float(tmp) < -30 or float(tmp) > 30:
                mbox.showerror("Error", "Ratio should be between -30 and 30!")
            else:
                self.scale_ratio[-1].set(tmp)
        elif axis == 'X':
            if float(tmp) < -30 or float(tmp) > 30:
                mbox.showerror("Error", "Ratio should be between -30 and 30!")
            else:
                self.scale_ratio[0].set(tmp)
        elif axis == 'Y':
            if float(tmp) < -30 or float(tmp) > 30:
                mbox.showerror("Error", "Ratio should be between -30 and 30!")
            else:
                self.scale_ratio[1].set(tmp)
        else:
            if float(tmp) < -30 or float(tmp) > 30:
                mbox.showerror("Error", "Ratio should be between -30 and 30!")
            else:
                self.scale_ratio[-1].set(tmp)
    

    def set_as_default_(self):
        if self.projection_var.get() == 1:
            self.scale_ratio[0].set(45)
            if self.object_drawing.height > 0:
                self.scale_ratio[1].set(self.object_drawing.width/self.object_drawing.height)
            else: 
                self.scale_ratio[1].set(1)
            # self.scale_ratio[1].set(1)
            self.scale_ratio[2].set(1)
            self.scale_ratio[-1].set(100)
            mbox.showinfo("Info", f"Successfully!\nFovy: {self.object_drawing.fov.get()}\nAspect: {self.object_drawing.asp.get()}\nNear: {self.object_drawing.zNear.get()}\nFar: {self.object_drawing.zFar.get()}")
        elif self.projection_var.get() == 2:
            self.scale_ratio[0].set(0)
            self.scale_ratio[1].set(0)
            self.scale_ratio[2].set(10)
            mbox.showinfo("Info", f"Successfully!\nEye X: {self.object_drawing.eyeX.get()}\nEye Y: {self.object_drawing.eyeY.get()}\nEye Z: {self.object_drawing.eyeZ.get()}")
        elif self.projection_var.get() == 3:
            self.scale_ratio[0].set(0)
            self.scale_ratio[1].set(0)
            self.scale_ratio[2].set(0)
            mbox.showinfo("Info", f"Successfully!\nCenter X: {self.object_drawing.centerX.get()}\nCenter Y: {self.object_drawing.centerY.get()}\nCenter Z: {self.object_drawing.centerZ.get()}")
        else:
            self.scale_ratio[0].set(0)
            self.scale_ratio[1].set(1)
            self.scale_ratio[2].set(0)
            mbox.showinfo("Info", f"Save successfully!\nUp X: {self.object_drawing.upX.get()}\nUp Y: {self.object_drawing.upY.get()}\nUp Z: {self.object_drawing.upZ.get()}")

    def projection_save(self):
        if self.projection_var.get() == 1:
            mbox.showinfo("Info", f"Save successfully!\nFovy: {self.object_drawing.fov.get()}\nAspect: {self.object_drawing.asp.get()}\nNear: {self.object_drawing.zNear.get()}\nFar: {self.object_drawing.zFar.get()}")
            self.object_drawing.fov_tmp.set(self.object_drawing.fov.get())
            self.object_drawing.asp_tmp.set(self.object_drawing.asp.get())
            self.object_drawing.zNear_tmp.set(self.object_drawing.zNear.get())
            self.object_drawing.zFar_tmp.set(self.object_drawing.zFar.get())
        elif self.projection_var.get() == 2:
            mbox.showinfo("Info", f"Save successfully!\nEye X: {self.object_drawing.eyeX.get()}\nEye Y: {self.object_drawing.eyeY.get()}\nEye Z: {self.object_drawing.eyeZ.get()}")
            self.object_drawing.eyeX_tmp.set(self.object_drawing.eyeX.get())
            self.object_drawing.eyeY_tmp.set(self.object_drawing.eyeY.get())
            self.object_drawing.eyeZ_tmp.set(self.object_drawing.eyeZ.get())
        elif self.projection_var.get() == 3:
            mbox.showinfo("Info", f"Save successfully!\nCenter X: {self.object_drawing.centerX.get()}\nCenter Y: {self.object_drawing.centerY.get()}\nCenter Z: {self.object_drawing.centerZ.get()}")
            self.object_drawing.centerX_tmp.set(self.object_drawing.centerX.get())
            self.object_drawing.centerY_tmp.set(self.object_drawing.centerY.get())
            self.object_drawing.centerZ_tmp.set(self.object_drawing.centerZ.get())
        else:
            mbox.showinfo("Info", f"Save successfully!\nUp X: {self.object_drawing.upX.get()}\nUp Y: {self.object_drawing.upY.get()}\nUp Z: {self.object_drawing.upZ.get()}")
            self.object_drawing.upX_tmp.set(self.object_drawing.upX.get())
            self.object_drawing.upY_tmp.set(self.object_drawing.upY.get())
            self.object_drawing.upZ_tmp.set(self.object_drawing.upZ.get())

    def projection_cancel(self):
        if self.projection_var.get() == 1:
            self.object_drawing.fov.set(self.object_drawing.fov_tmp.get())
            self.object_drawing.asp.set(self.object_drawing.asp_tmp.get())
            self.object_drawing.zNear.set(self.object_drawing.zNear_tmp.get())
            self.object_drawing.zFar.set(self.object_drawing.zFar_tmp.get())
        elif self.projection_var.get() == 2:
            self.object_drawing.eyeX.set(self.object_drawing.eyeX_tmp.get())
            self.object_drawing.eyeY.set(self.object_drawing.eyeY_tmp.get())
            self.object_drawing.eyeZ.set(self.object_drawing.eyeZ_tmp.get())
        elif self.projection_var.get() == 3:
            self.object_drawing.centerX.set(self.object_drawing.centerX_tmp.get())
            self.object_drawing.centerY.set(self.object_drawing.centerY_tmp.get())
            self.object_drawing.centerZ.set(self.object_drawing.centerZ_tmp.get())
        else:
            self.object_drawing.upX.set(self.object_drawing.upX_tmp.get())
            self.object_drawing.upY.set(self.object_drawing.upY_tmp.get())
            self.object_drawing.upZ.set(self.object_drawing.upZ_tmp.get())


    """++++++++++++++++++++++++++++++++++++++++++"""
    # LIGHT functions
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
    # TEXTURE functions
    def turn_texture(self):
        try:
            if self.texture_mode.get() == 1:
                path_current = os.getcwd()
                path_img = askopenfilename(initialdir = f"{path_current}/textures",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
                if path_img == () or path_img == "":
                    self.object_drawing.toggleTextures = -1
                    self.texture_mode.set(-1)
                else:
                    self.object_drawing.toggleTextures = 1
                    # self.object_drawing['cursor'] = 'arrow'
                    image = Image.open(f'{path_img}')
                    image = image.transpose(Image.FLIP_TOP_BOTTOM)
                    self.object_drawing.imageWHTex = (image.width, image.height)
                    self.object_drawing.imgDataTex = image.convert("RGBA").tobytes()
                    self.object_drawing.textureDraw = glGenTextures(1)
            else:
                self.object_drawing.toggleTextures = -1
        except AttributeError:
            pass
    """++++++++++++++++++++++++++++++++++++++++++"""
    # EFFECTS functions
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
            self.button_scale['bg'] = '#e1f281'
        except AttributeError:
            pass
        self.scale_mode = 0
        # Disable choices in options
        for options in self.shape_options:
            options.deselect()
            options['state'] = 'disable'
        for options in self.projection_options:
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
        for options in self.projection_options:
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
        for options in self.projection_options:
            options['state'] = 'active'
        for options in self.light_options:
            options['state'] = 'active'
        for options in self.texture_options:
            options['state'] = 'active'
        for options in self.rotating_options:
            options['state'] = 'active'
        self.shape_options[-1].select()

    """++++++++++++++++++++++++++++++++++++++++++"""
    def run(self):
        self.screenMain_Load()

if __name__ == '__main__':
    glutInit()
    app = App3D()
    app.run()
#!/usr/bin/env python3

from random import random
import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D
from time import time


class ViewerGL:
    def __init__(self):

        PLEIN_ECRAN = False
        self.TEMPS = 60

        self.HEIGHT = 480
        self.WIDTH = 640
        self.SENSI = 0.005
        #self.lastX, self.lastY = self.WIDTH / 2, self.HEIGHT / 2
        self.lastX, self.lastY = 0, 0

        self.fps_last_time = 0
        self.fps_10_last = [0 for i in range(10)]
        self.fps_text_object = None

        self.temps_origine = None
        self.timer_text_object = None




        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        if PLEIN_ECRAN:
            PLEIN_ECRAN_ = glfw.get_primary_monitor()
        else:
            PLEIN_ECRAN_ = None
        self.window = glfw.create_window(self.WIDTH, self.HEIGHT, 'OpenGL', PLEIN_ECRAN_, None)
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)

    	#leo gestion souris
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback )
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.objs = []
        self.touch = {}

        self.perso = None

        #SOURIS AU NATUREL
        if (glfw.raw_mouse_motion_supported()):
            #print("SOURIS AU NATUREL")
            glfw.set_input_mode(self.window, glfw.RAW_MOUSE_MOTION, glfw.TRUE);
        
        

    def run(self):
        # boucle d'affichage

        tps1 = time()

        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.update_key()
            self.timer_update()

            for obj in self.objs:
                GL.glUseProgram(obj.program)
                if isinstance(obj, Object3D):
                    self.update_camera(obj.program)
                obj.draw()

            # changement de buffer d'affichage pour éviter un effet de scintillement 
            #The glfwSwapBuffers 4.4 One last thing 23 will swap the color buffer (a large 2D buffer that contains color values for each pixel in GLFW’s window) that is used to render to during this render iteration and show it as output to the screen.
            glfw.swap_buffers(self.window)
            # gestion des évènements
            # The glfwPollEvents function checks if any events are triggered (like keyboard input or mouse movement events), updates the window state, and calls the corresponding functions (which we can register via callback methods).
            glfw.poll_events() 



            self.update_fps()

        
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        self.touch[key] = action
    
    def add_object(self, obj):
        self.objs.append(obj)

    def set_camera(self, cam):
        self.cam = cam

    def update_camera(self, prog):
        GL.glUseProgram(prog)
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_view")
        # Modifie la variable pour le programme courant
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)
    
        loc = GL.glGetUniformLocation(prog, "projection")
        if (loc == -1) :
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)

    def update_key(self):
        if glfw.KEY_W in self.touch and self.touch[glfw.KEY_W] > 0: #KEY Z
            self.perso.transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.perso.transformation.rotation_euler), pyrr.Vector3([0, 0, 0.5]))
        if glfw.KEY_S in self.touch and self.touch[glfw.KEY_S] > 0: #KEY S
            self.perso.transformation.translation -= \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.perso.transformation.rotation_euler), pyrr.Vector3([0, 0, 0.5]))
        if glfw.KEY_A in self.touch and self.touch[glfw.KEY_A] > 0: #KEY Q
            self.perso.transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.perso.transformation.rotation_euler), pyrr.Vector3([0.5, 0, 0]))
        if glfw.KEY_D in self.touch and self.touch[glfw.KEY_D] > 0: #KEY D
            self.perso.transformation.translation -= \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.perso.transformation.rotation_euler), pyrr.Vector3([0.5, 0, 0]))

        if not(glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0):
            #self.cam.transformation.rotation_euler = self.perso.transformation.rotation_euler.copy() 
            #self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
            self.cam.transformation.rotation_center = self.perso.transformation.translation + self.perso.transformation.rotation_center
            self.cam.transformation.translation = self.perso.transformation.translation + pyrr.Vector3([0, 1, 4])

    def mouse_callback(self, window, xpos, ypos): #fonction dediee a la gestion de la cam par la souris

        # if first_mouse:
        #     lastX = xpos
        #     lastY = ypos
        #     first_mouse = False


        xoffset = (xpos - self.lastX)*self.SENSI
        yoffset = (ypos - self.lastY)*self.SENSI

        self.lastX = xpos
        self.lastY = ypos

        roll = self.cam.transformation.rotation_euler[pyrr.euler.index().roll]
    
        if roll+yoffset >= -0.2 and roll+yoffset <= 1:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += yoffset

        self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += xoffset

        #forcer le perso a suivre la cam
        self.perso.transformation.rotation_euler[pyrr.euler.index().yaw] = self.cam.transformation.rotation_euler[pyrr.euler.index().yaw]+np.pi


    def set_timer(self, timer, temps_origine):
        self.timer_text_object = timer
        self.temps_origine = temps_origine


    def timer_update(self):
        self.timer_text_object.value = str(self.TEMPS + self.temps_origine - time())[:4]


    def update_fps(self):
        self.fps_10_last.append(1/(time() - self.fps_last_time))
        self.fps_text_object.value = str(np.average(self.fps_10_last))[:2]
        self.fps_last_time = time()

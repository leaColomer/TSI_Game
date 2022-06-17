#!/usr/bin/env python3

from random import random
import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D
from time import time, sleep
import collision


class ViewerGL:
    def __init__(self):

        PLEIN_ECRAN = False
        self.TEMPS = 60

        self.TAILLE_LABY = None

        self.HEIGHT = 600
        self.WIDTH = 600

        self.SENSI = 0.005
        self.PAS_DE_DEPLACEMENT = 1.5 # case par seconde
        #self.lastX, self.lastY = self.WIDTH / 2, self.HEIGHT / 2
        self.lastX, self.lastY = 0, 0

        self.i = 0
        self.j = 0

        self.dernier_temps = 0
        self.fps_10_last = [0 for i in range(10)]
        self.fps_text_object = None
        self.compteur_80f = 0
        self.overload_text_object = None

        self.coos_text_object = None

        self.temps_zero = None
        self.temps_depart = None
        self.timer_text_object = None

        self.unite = None
        self.rayon_perso = None
        self.epaisseur_mur = None


        self.murs = None




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
        self.murs = None

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
            self.coos_update()

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


    def collision_global(self, x, y, r):
        contact = False
        maxim = len(self.murs.grille[0])
        j = int(x/self.unite)
        i = int(y/self.unite)

        if 0<=i<maxim and 0<=j<maxim:
            murs_a_tester = self.murs.grille[i][j]
            nb_murs = len(murs_a_tester)
            k=0
            while not contact and k<nb_murs:
                mur = murs_a_tester[k]
                cercle = collision.Cercle(x,y,r)
                contact = collision.collision_cercle_rectangle(cercle,mur)
                k+=1

        return contact


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
        deplacement = np.array([0.0,0.0,0.0])
        if glfw.KEY_W in self.touch and self.touch[glfw.KEY_W] > 0: #KEY Z
            deplacement += [0.0, 0.0, 1.0]
        if glfw.KEY_S in self.touch and self.touch[glfw.KEY_S] > 0: #KEY S
            deplacement += [0.0, 0.0, -1.0]
        if glfw.KEY_A in self.touch and self.touch[glfw.KEY_A] > 0: #KEY Q
            deplacement += [1.0, 0.0, 0.0]
        if glfw.KEY_D in self.touch and self.touch[glfw.KEY_D] > 0: #KEY D
            deplacement += [-1.0, 0.0, 0.0]
        
        norm = np.linalg.norm(deplacement)
        if norm>0:
            deplacement = deplacement/norm

        deplacement_oriente = pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.perso.transformation.rotation_euler), pyrr.Vector3(deplacement))

        coo = self.perso.transformation.translation

        fps = self.fps_10_last[9]
        if fps>20:
            vitesse = self.PAS_DE_DEPLACEMENT/fps
        else:
            vitesse = self.PAS_DE_DEPLACEMENT/20
        nouv_coo = coo + deplacement_oriente*vitesse
        
        if not self.collision_global(coo.x, nouv_coo.z, self.rayon_perso):
            coo.z += (deplacement_oriente*vitesse)[2]
            self.perso.transformation.translation = coo
        
        if not self.collision_global(nouv_coo.x, coo.z, self.rayon_perso):
            coo.x += (deplacement_oriente*vitesse)[0]
            self.perso.transformation.translation = coo
            

        if not(glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0):
            #self.cam.transformation.rotation_euler = self.perso.transformation.rotation_euler.copy() 
            #self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
            self.cam.transformation.rotation_center = self.perso.transformation.translation + self.perso.transformation.rotation_center
            self.cam.transformation.translation = self.perso.transformation.translation  + pyrr.Vector3([0, 0.2, 0.2])

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


    def set_timer(self, timer, t):
        self.timer_text_object = timer
        self.temps_depart = t


    def timer_update(self):
        temps = self.TEMPS + self.temps_depart - time()
        self.timer_text_object.value = str(temps)[:4]
        if temps<0.1*self.TEMPS:
            self.timer_text_object.bottomLeft = np.array([-0.25, 0.70], np.float32)
            self.timer_text_object.topRight = np.array([0.35, 0.95], np.float32)
        
        #teleportation du joueur au centre a la fin du compteur
        if temps<0:
            self.temps_depart = time()
            self.perso.transformation.translation = pyrr.Vector3([self.unite/2 + self.TAILLE_LABY//2, 0.0, self.unite/2 + self.TAILLE_LABY//2])


    def coos_update(self):
        coos = self.perso.transformation.translation
        self.i = int(coos[0]/self.unite)
        self.j = int(coos[2]/self.unite)
        self.coos_text_object.value = '(' + str(self.i) + ',' + str(self.j) + ')'

    def update_fps(self):
        temps = time()
        delta = (temps - self.dernier_temps)

        fps = 1/delta
        self.fps_10_last.append(fps)
        self.fps_10_last.pop(0)
        

        self.dernier_temps = temps
        self.fps_text_object.value = str(np.average(self.fps_10_last))[:2] + 'FPS'

        
        if fps<20:
            if self.compteur_80f<10:
                self.overload_text_object.value = "Performances reduites"
            else:
                self.overload_text_object.value = " "
            if self.compteur_80f==0:
                self.compteur_80f = 20
            self.compteur_80f-=1
        elif self.compteur_80f!=0 :
            self.compteur_80f = 0
            self.overload_text_object.value = " "

        

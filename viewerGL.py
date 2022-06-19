#!/usr/bin/env python3

import glutils
import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D, Camera, Transformation3D
from time import time, sleep
import collision

import mesh


import objets_ini
import gen_laby_mat
import gen_laby_2d
import gen_laby_3d


class ViewerGL:
    def __init__(self):

        self.PLEIN_ECRAN = False
        self.HEIGHT = 600
        self.WIDTH = 600



        self.scene = 0
        self.premiere_partie = True

        self.TEMPS = None
        self.TRICHE = None
        self.TAILLE_LABY = None
        self.SENSI = None
        self.VITESSE = None
        
        self.lastX, self.lastY = 0, 0
        self.i = 0
        self.j = 0
        
        self.coos_text_object = None

        self.dernier_temps = 0
        self.fps_10_last = [0 for _ in range(10)]
        self.fps_text_object = None
        self.compteur_80f = 0
        self.overload_text_object = None

        self.compteur_teleportation = 0

        self.temps_origine = None
        self.temps_depart = None
        self.temps_pause = 0
        self.temps_pause_ini = None
        self.timer_text_object = None
        self.timer2_text_object = None

        self.unite = None
        self.rayon_perso = None
        self.epaisseur_mur = None


        self.murs = None

        self.x_fin = None
        self.y_fin = None

        self.LONGUEUR_CHEMIN_PARFAIT = None

        self.load_screen = None



        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        if self.PLEIN_ECRAN:
            PLEIN_ECRAN_ = glfw.get_primary_monitor()
        else:
            PLEIN_ECRAN_ = None
        self.window = glfw.create_window(self.WIDTH, self.HEIGHT, 'OpenGL', PLEIN_ECRAN_, None)
        
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)

        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        glfw.set_mouse_button_callback(self.window, self.clic_callback)

        self.objs = []
        self.objs_attaches_perso = []
        self.objs_r = []
        self.objs_menu = []
        self.objs_fin = []
        self.touch = {}


        self.perso = None

        self.murs = None

        self.set_camera(Camera())

        #SOURIS AU NATUREL
        if (glfw.raw_mouse_motion_supported()):
            #print("SOURIS AU NATUREL")
            glfw.set_input_mode(self.window, glfw.RAW_MOUSE_MOTION, glfw.TRUE);
        
    def clic_callback(self,window,b,up,d):
        if self.scene == 0 and up:
            x , y = glfw.get_cursor_pos(self.window)
            x = (x-self.WIDTH/2)/self.WIDTH*2
            y = (-y+self.HEIGHT/2)/self.HEIGHT*2
            b_play = self.objs_menu[0]
            b_re = self.objs_menu[1]
            b_quit = self.objs_menu[2]
            if b_play.bottomLeft[0]<x<b_play.topRight[0] and b_play.bottomLeft[1]<y<b_play.topRight[1]:
                self.scene = 1
                self.chargement()
                self.nvlle_partie()
            if b_re.bottomLeft[0]<x<b_re.topRight[0] and b_re.bottomLeft[1]<y<b_re.topRight[1]:
                if not self.premiere_partie:
                    self.scene = 1
                    self.reprendre_partie()
            if b_quit.bottomLeft[0]<x<b_quit.topRight[0] and b_quit.bottomLeft[1]<y<b_quit.topRight[1]:
                glfw.set_window_should_close(self.window, glfw.TRUE)
        if self.scene == 2 and up:
            x , y = glfw.get_cursor_pos(self.window)
            x = (x-self.WIDTH/2)/self.WIDTH*2
            y = (-y+self.HEIGHT/2)/self.HEIGHT*2
            btn = self.objs_fin[0]
            if btn.bottomLeft[0]<x<btn.topRight[0] and btn.bottomLeft[1]<y<btn.topRight[1]:
                self.scene = 0

    def nvlle_partie(self):

        self.perso.transformation.translation.x = self.unite/2 + self.TAILLE_LABY//2
        self.perso.transformation.translation.y = self.unite/5 + self.TRICHE*3
        self.perso.transformation.translation.z = self.unite/2 + self.TAILLE_LABY//2

        matrice_laby, _, [self.x_fin,self.y_fin] = gen_laby_mat.genere_spe(self.TAILLE_LABY,self.LONGUEUR_CHEMIN_PARFAIT,0) # 0 erreur. le chemin parf fait exactement 97(x) cases de long
        gen_laby_3d.nouveau_obj_laby(matrice_laby, 'laby.obj', self.epaisseur_mur) #regenerer laby.obj
        self.murs = gen_laby_2d.Murs(matrice_laby, self.epaisseur_mur, self.unite)

        if not self.premiere_partie:
            self.objs_r = [] #on suppr l ancien laby et ses objets
        else:
            self.premiere_partie = False

        objets_ini.creer_big_maze(self)

        self.temps_depart = time()
        self.temps_origine = time()
        self.temps_pause = 0

    def reprendre_partie(self):
        self.temps_pause += time() - self.temps_pause_ini


    def key_callback(self, win, key, scancode, action, mods):
        # retour au menu si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            self.temps_pause_ini = time()
            self.scene = 0
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
            pas_de_deplacmeent = self.VITESSE/fps
        else:
            pas_de_deplacmeent = self.VITESSE/20
        nouv_coo = coo + deplacement_oriente*pas_de_deplacmeent
        
        if not self.collision_global(coo.x, nouv_coo.z, self.rayon_perso):
            coo.z += (deplacement_oriente*pas_de_deplacmeent)[2]
            self.perso.transformation.translation = coo
        
        if not self.collision_global(nouv_coo.x, coo.z, self.rayon_perso):
            coo.x += (deplacement_oriente*pas_de_deplacmeent)[0]
            self.perso.transformation.translation = coo
        
    def objs_suivent_perso(self):
        #la cam a le droit a un traitement particulier
        self.cam.transformation.rotation_center = self.perso.transformation.translation + self.perso.transformation.rotation_center
        self.cam.transformation.translation = self.perso.transformation.translation  + pyrr.Vector3([0, 0.2, 0])

        #tout les autre objets concernes sont translates au meme endroit que le joueur
        for obj in self.objs_attaches_perso:
            obj.transformation.translation = self.perso.transformation.translation  + pyrr.Vector3([0, 0.2, 0])

    def mouse_partie_callback(self, window, xpos, ypos): #fonction dediee a la gestion de la cam par la souris

        xoffset = (xpos - self.lastX)*self.SENSI
        yoffset = (ypos - self.lastY)*self.SENSI

        self.lastX = xpos
        self.lastY = ypos

        roll = self.cam.transformation.rotation_euler[pyrr.euler.index().roll]
    
        if roll+yoffset >= -0.5 and roll+yoffset <= 1:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += yoffset

        self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += xoffset

        #forcer le perso a suivre la cam
        self.perso.transformation.rotation_euler[pyrr.euler.index().yaw] = self.cam.transformation.rotation_euler[pyrr.euler.index().yaw]+np.pi


    def timers_update(self):
        temps = self.TEMPS + self.temps_depart - time() + self.temps_pause #temps imaprti 60s + time.depart - time.actuel
        self.timer_text_object.value = str(temps)[:4]
        temps2 = time()-self.temps_origine-self.temps_pause
        self.timer2_text_object.value = str(temps2)[:4]
        if temps<0.1*self.TEMPS: #pour grossir le chrono et le mettre en rouge c est rigolo
            self.timer_text_object.bottomLeft = np.array([-0.30, 0.70], np.float32)
            self.timer_text_object.topRight = np.array([0.30, 0.95], np.float32)
            self.timer_text_object.texture = glutils.load_texture('tex/fontBred.jpg')
        else:
            self.timer_text_object.bottomLeft = np.array([-0.17, 0.80], np.float32)
            self.timer_text_object.topRight = np.array([0.17, 0.95], np.float32)
            self.timer_text_object.texture = glutils.load_texture('tex/fontB.jpg')
        
        #teleportation du joueur au centre a la fin du compteur
        if temps<0:
            self.retour_a_la_case_depart() #monopoly
    
    def retour_a_la_case_depart(self):
        self.temps_depart = time()
        self.temps_pause+=2
    
        program3d_sky_id = glutils.create_program_from_file('shader.vert', 'sky.frag') #frag sans illumination

        #on créé un objet noir autour de la cam ca evite de faire une scene de transition
        m = mesh.Mesh.load_obj('cube.obj')
        m.normalize()
        m.apply_matrix(pyrr.matrix44.create_from_scale([0.1, 0.1, 0.1]))
        texture = glutils.load_texture('tex/pizzas.jpg')
        o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_sky_id, texture, Transformation3D())
        self.add_object(o)
        self.objs_attaches_perso.append(o)

        self.compteur_teleportation = time()

        self.perso.transformation.translation = pyrr.Vector3([self.unite/2 + self.TAILLE_LABY//2, self.unite/5 + self.TRICHE*3, self.unite/2 + self.TAILLE_LABY//2])


    def coos_update(self):
        coos = self.perso.transformation.translation
        self.i = int(coos[0]/self.unite) - self.TAILLE_LABY//2
        self.j = int(coos[2]/self.unite) - self.TAILLE_LABY//2
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

    def victoire(self):
        x, y = self.perso.transformation.translation.xz
        if 0.5>=abs(x-(self.x_fin+0.5)) and 0.5>=abs(y-(self.y_fin+0.5)):
            self.scene = 2
            temps_final = time() - self.temps_origine - self.temps_pause
            self.objs_fin[1].value = 'Score : ' + str(temps_final)[:4] + ' s'
    
    def chargement(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        
        obj = self.load_screen
        GL.glUseProgram(obj.program)
        obj.draw()
        
        glfw.swap_buffers(self.window)
        glfw.poll_events() 
        

    def run_menu(self):
        #self.scene = 1
        # nettoyage de la fenêtre : fond et profondeur
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        for obj in self.objs_menu:
            GL.glUseProgram(obj.program)
            obj.draw()
        
        glfw.swap_buffers(self.window)
        glfw.poll_events() 


    def run_partie(self):
        # nettoyage de la fenêtre : fond et profondeur
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        if self.compteur_teleportation != 0 :
            if time() - self.compteur_teleportation > 2 : #deux secondes d'atente
                #on retire l'ecran transition
                self.objs.pop()
                self.objs_attaches_perso.pop()
                self.compteur_teleportation = 0

        self.update_key()
        self.objs_suivent_perso()
        self.timers_update()
        #self.coos_update()
        self.victoire()

        for obj in (self.objs_r + self.objs):
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


    def run_fin(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        for obj in self.objs_fin:
            GL.glUseProgram(obj.program)
            obj.draw()
            
        glfw.swap_buffers(self.window)
        glfw.poll_events() 
        
    def run(self):

        while not glfw.window_should_close(self.window):
            
            

            while not glfw.window_should_close(self.window) and self.scene == 0:
                self.run_menu()
            
            #on remet la fonc de callback mouse + desactive le curseur
            glfw.set_cursor_pos_callback(self.window, self.mouse_partie_callback )
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

            while not glfw.window_should_close(self.window) and self.scene == 1:
                self.run_partie()

            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)

            while not glfw.window_should_close(self.window) and self.scene == 2:
                self.run_fin()

        
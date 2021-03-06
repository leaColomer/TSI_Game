import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr
from time import time

#fonc a part pour l appeler quand nvlle partie
def creer_big_maze(viewer): #BIG MAZE COMME TEN AS JAMAIS VU V2
    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    m = Mesh.load_obj('laby.obj')
    #m.normalize()
    #alpha = viewer.TAILLE_LABY+2
    #m.apply_matrix(pyrr.matrix44.create_from_scale([alpha, alpha, alpha, 1]))
    texture = glutils.load_texture('tex/brique.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.objs_r.append(o)
    
    #cube fin
    m = Mesh.load_obj('cylindre.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([0.3, 0.3, 0.3, 1]))
    tr = Transformation3D()
    tr.translation.x = 1/2 + viewer.x_fin
    tr.translation.y = 1/2
    tr.translation.z = 1/2 + viewer.y_fin
    texture = glutils.load_texture('tex/red.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.objs_r.append(o)

def initialisation(viewer):
    
    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')
    program3d_sky_id = glutils.create_program_from_file('shader.vert', 'sky.frag') #frag sans illumination

    #skybox
    m = Mesh.load_obj('cube_skybox.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([20, 20, 20]))
    tr = Transformation3D()
    tr.translation.x = viewer.TAILLE_LABY//2
    tr.translation.y = 10.5
    tr.translation.z = viewer.TAILLE_LABY//2
    texture = glutils.load_texture('tex/skybox.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_sky_id, texture, tr)
    viewer.add_object(o)
    viewer.objs_attaches_perso.append(o)

    #personnage
    m = Mesh.load_obj('cylindre.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([viewer.rayon_perso*1.3, 0.03, viewer.rayon_perso*1.3, 1]))
    tr = Transformation3D()
    tr.translation.x = 1/2 + viewer.TAILLE_LABY//2
    tr.translation.y = 1/5 + viewer.TRICHE*3
    tr.translation.z = 1/2 + viewer.TAILLE_LABY//2
    #tr.rotation_center.z = 0.2
    texture = glutils.load_texture('tex/red.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)
    viewer.perso = o

    #sol
    m = Mesh()
    lar = viewer.TAILLE_LABY
    p0, p1, p2, p3 = [0, 0, 0], [lar, 0, 0], [lar, 0, lar], [0, 0, lar] # coos des points : ATTENTION, un point UNE SEULE NORMALE donc CUBE : trois normales, trois points par angle
    n, c = [0, 1, 0], [1, 1, 1] # la normale n : oriente chacun des points pour la lumi??re ! # la couleur : ?? peu pr??s pareil
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1] # coordonn??es de textures
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('tex/grass.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    #test collisions
    # m = Mesh()
    # murs1 = viewer.murs.grille[0][0]
    # for mu in murs1:
    #     p0 = [mu.x,         1.5,    mu.y]
    #     p1 = [mu.x + mu.l,  1.5,    mu.y]
    #     p2 = [mu.x + mu.l,  1.5,    mu.y + mu.h]
    #     p3 = [mu.x,         1.5,    mu.y + mu.h]
    #     n, c = [0, 1, 0], [1, 1, 1] # la normale n : oriente chacun des points pour la lumi??re ! # la couleur : ?? peu pr??s pareil
    #     t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1] # coordonn??es de textures
    #     m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    #     m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    #     texture = glutils.load_texture('tex/blue.jpg')
    #     o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    #     viewer.add_object(o)





    vao = Text.initalize_geometry()
    texture = glutils.load_texture('tex/fontB.jpg')
    #ARGS self, value, bottomLeft, topRight, vao, nb_triangle, program, texture

    #timer
    o = Text('HUGO JTM', np.array([-0.15, 0.85], np.float32), np.array([0.15, 0.95], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    viewer.timer_text_object = o

    #timer2 g??n??ral
    o = Text('HUGO JTM', np.array([-0.98, -1.0], np.float32), np.array([-0.80, -0.85], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    viewer.timer2_text_object = o

    #compteur de FPS
    o = Text('HUGO JTM', np.array([0.75, 0.85], np.float32), np.array([0.98, 0.98], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    viewer.fps_text_object = o

    # # affichage coordonnes
    # o = Text('HUGO JTM', np.array([-0.17, -1.0], np.float32), np.array([0.17, -0.85], np.float32), vao, 2, programGUI_id, texture)
    # viewer.add_object(o)
    # viewer.coos_text_object = o

    # affichage info commande ESC
    o = Text('PAUSE [ESC]', np.array([-0.98, 0.85], np.float32), np.array([-0.50, 0.98], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)

    # affichage erreur performance
    o = Text(' ', np.array([-0.5, 0.0], np.float32), np.array([0.5, 0.10], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    viewer.overload_text_object = o

    # Bouton jouer
    o = Text('Nouvelle partie', np.array([-0.7, 0.25], np.float32), np.array([0.7, 0.55], np.float32), vao, 2, programGUI_id, texture)
    viewer.objs_menu.append(o)

    # Bouton reprendre
    o = Text('Reprendre', np.array([-0.7, -0.20], np.float32), np.array([0.7, 0.10], np.float32), vao, 2, programGUI_id, texture)
    viewer.objs_menu.append(o)

    # Bouton quitter
    o = Text('Quitter', np.array([-0.7, -0.70], np.float32), np.array([0.7, -0.45], np.float32), vao, 2, programGUI_id, texture)
    viewer.objs_menu.append(o)

    # FIN bouton retour au menu
    o = Text('Retour au menu', np.array([-0.7, -0.70], np.float32), np.array([0.7, -0.45], np.float32), vao, 2, programGUI_id, texture)
    viewer.objs_fin.append(o)

    # FIN temps final
    o = Text('Score : 10.0 s', np.array([-0.6, -0.13], np.float32), np.array([0.6, 0.13], np.float32), vao, 2, programGUI_id, texture)
    viewer.objs_fin.append(o)

    # FIN BRAVISSIMO
    o = Text('bravissimo', np.array([-0.7, 0.30], np.float32), np.array([0.7, 0.67], np.float32), vao, 2, programGUI_id, texture)
    viewer.objs_fin.append(o)

    # LOAD SCREEN
    o = Text('Generation  du  Labyrinthe...', np.array([-0.8, -0.08], np.float32), np.array([0.8, 0.08], np.float32), vao, 2, programGUI_id, texture)
    viewer.load_screen = o


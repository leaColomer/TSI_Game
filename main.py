from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr
from time import time
import gen_laby_mat
import gen_laby_2d
import gen_laby_3d

def main():
    TAILLE_LABY = 10 #taille du cote du labyrinthe
    

    viewer = ViewerGL()
    viewer.TAILLE_LABY = TAILLE_LABY
    
    viewer.epaisseur_mur = 0.09
    viewer.unite = 1 #longeur d'un mur OU PLUTOT D'UNE CASE DU LABY
    
    viewer.rayon_perso = 0.3 # 0.3*viewer.unite

    matrice_laby = gen_laby_mat.genere(TAILLE_LABY)
    gen_laby_3d.nouveau_obj_laby(matrice_laby, 'laby.obj', viewer.epaisseur_mur) #regenerer laby.obj
    viewer.murs = gen_laby_2d.Murs(matrice_laby, viewer.epaisseur_mur, viewer.unite)




    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 1
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')

    #personnage
    m = Mesh.load_obj('cube.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([viewer.rayon_perso, 0.5, viewer.rayon_perso, 1]))
    tr = Transformation3D()
    tr.translation.x = viewer.unite/2
    tr.translation.y = viewer.unite/2
    tr.translation.z = viewer.unite/2
    #tr.rotation_center.z = 0.2
    texture = glutils.load_texture('stegosaurus.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)
    viewer.perso = o

    #cube reperage
    m = Mesh.load_obj('cube.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([0.3, 0.3, 0.3, 1]))
    vao = m.load_to_gpu()

    tr = Transformation3D()
    tr.translation.x = 0
    tr.translation.y = 2
    tr.translation.z = 0
    texture = glutils.load_texture('red.jpg')
    o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)
    
    tr = Transformation3D()
    tr.translation.x = 1
    tr.translation.y = 2
    tr.translation.z = 0
    texture = glutils.load_texture('blue.jpg')
    o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)

    tr = Transformation3D()
    tr.translation.x = 0
    tr.translation.y = 2
    tr.translation.z = 1
    texture = glutils.load_texture('chill.jpg')
    o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)

    #sol
    m = Mesh()
    p0, p1, p2, p3 = [-25, 0, -25], [25, 0, -25], [25, 0, 25], [-25, 0, 25] # coos des points : ATTENTION, un point UNE SEULE NORMALE donc CUBE : trois normales, trois points par angle
    n, c = [0, 1, 0], [1, 1, 1] # la normale n : oriente chacun des points pour la lumière ! # la couleur : à peu près pareil
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1] # coordonnées de textures
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('grass.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    #BIG MAZE COMME TEN AS JAMAIS VU V2
    m = Mesh.load_obj('laby.obj')
    m.normalize()
    alpha = TAILLE_LABY+1
    m.apply_matrix(pyrr.matrix44.create_from_scale([alpha, alpha, alpha, 1]))
    vao = m.load_to_gpu()
    texture = glutils.load_texture('brique.jpg')
    tr = Transformation3D()
    tr.translation.x = alpha//2
    tr.translation.y = 0
    tr.translation.z = alpha//2
    o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)


    vao = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    #ARGS self, value, bottomLeft, topRight, vao, nb_triangle, program, texture
    o = Text('HUGO JTM', np.array([-0.15, 0.85], np.float32), np.array([0.15, 0.95], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    viewer.set_timer(o,time())

    #compteur de FPS
    o = Text('HUGO JTM', np.array([0.85, 0.85], np.float32), np.array([0.95, 0.95], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    viewer.fps_text_object = o


    viewer.run()


if __name__ == '__main__':
    main()
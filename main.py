from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr
from time import time
import creation_laby


def main():
    TAILLE_LABY = 5 #taille du labyrinthe

    viewer = ViewerGL()

    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 1
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')

    #personnage
    m = Mesh.load_obj('cube.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([0.5, 1, 0.5, 1]))
    tr = Transformation3D()
    tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z = -5
    tr.rotation_center.z = 0.2
    texture = glutils.load_texture('stegosaurus.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)
    viewer.perso = o

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

    #BIG MAZE COMME TEN AS JAMAIS VU
    m = Mesh.load_obj('wall.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
    vao = m.load_to_gpu()
    texture = glutils.load_texture('brique.jpg')

    matrice_laby = creation_laby.matrice_laby_alea(TAILLE_LABY)
    print(matrice_laby)
    for i in range(TAILLE_LABY+1):
        for j in range(TAILLE_LABY+1):
            tr = Transformation3D()
            tr.rotation_center.x = 0
            tr.rotation_center.y = 0
            tr.rotation_center.z = 1
            tr.translation.x = j*2
            tr.translation.y = 1
            tr.translation.z = i*2

            e = matrice_laby[i][j]
            if e == 0:
                tr.rotation_euler[pyrr.euler.index().yaw] = -np.pi/2
                
                o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
                viewer.murs.append(o)
                viewer.add_object(o)
            elif e == 3:
                o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
                viewer.murs.append(o)
                viewer.add_object(o)
            elif e == 1:
                o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
                viewer.murs.append(o)
                viewer.add_object(o)
                
                tr = Transformation3D()
                tr.rotation_center.x = 0
                tr.rotation_center.y = 0
                tr.rotation_center.z = 1
                tr.translation.x = j*2
                tr.translation.y = 1
                tr.translation.z = i*2
                tr.rotation_euler[pyrr.euler.index().yaw] = -np.pi/2
                
                o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
                viewer.murs.append(o)
                viewer.add_object(o)


    vao = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    # o = Text('Bonjour les', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
    # viewer.add_object(o)
    #ARGS self, value, bottomLeft, topRight, vao, nb_triangle, program, texture
    o = Text('HUGO JTM', np.array([-0.15, 0.85], np.float32), np.array([0.15, 0.95], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    viewer.set_timer(o,time())

    o = Text('HUGO JTM', np.array([0.85, 0.85], np.float32), np.array([0.95, 0.95], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    viewer.fps_text_object = o


    viewer.run()


if __name__ == '__main__':
    main()
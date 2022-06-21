
    # #BIG MAZE COMME TEN AS JAMAIS VU V1
    # m = Mesh.load_obj('wall_creux.obj')
    # m.normalize()
    # m.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
    # vao = m.load_to_gpu()
    # texture = glutils.load_texture('brique.jpg')

    # matrice_laby = creation_laby.matrice_laby_alea(TAILLE_LABY)
    # print(matrice_laby)
    # for i in range(TAILLE_LABY+1):
    #     for j in range(TAILLE_LABY+1):
    #         tr = Transformation3D()
    #         tr.rotation_center.x = 0
    #         tr.rotation_center.y = 0
    #         tr.rotation_center.z = 1
    #         tr.translation.x = j*2
    #         tr.translation.y = 1
    #         tr.translation.z = i*2

    #         e = matrice_laby[i][j]
    #         if e == 0:
    #             tr.rotation_euler[pyrr.euler.index().yaw] = -np.pi/2
                
    #             o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
    #             viewer.murs.append(o)
    #             viewer.add_object(o)
    #         elif e == 3:
    #             o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
    #             viewer.murs.append(o)
    #             viewer.add_object(o)
    #         elif e == 1:
    #             o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
    #             viewer.murs.append(o)
    #             viewer.add_object(o)
                
    #             tr = Transformation3D()
    #             tr.rotation_center.x = 0
    #             tr.rotation_center.y = 0
    #             tr.rotation_center.z = 1
    #             tr.translation.x = j*2
    #             tr.translation.y = 1
    #             tr.translation.z = i*2
    #             tr.rotation_euler[pyrr.euler.index().yaw] = -np.pi/2
                
    #             o = Object3D(vao, m.get_nb_triangles(), program3d_id, texture, tr)
    #             viewer.murs.append(o)
    #             viewer.add_object(o)
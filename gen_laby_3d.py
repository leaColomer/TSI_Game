#
import numpy as np



class Maillage():
    def __init__(self):
        self.sommets = []
        self.faces = []
        self.normales = [ [0.0, 0.0, 1.0], [0.0, 0.0, -1.0], [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0] ]
        self.textures = [ [0, 0.25], [0.25, 0.25], [0.5, 0.25], [0.75, 0.25], [0.0, 0.5], [0.25, 0.5], [0.5, 0.5], [0.75, 0.5], [0.25, 0.75], [0.5, 0.75], [0.25, 1.0], [0.5,  1.0] ]
        self.nombre_murs = 0
        self.nombre_piliers = 0
        self.nombre_face_mur = None
        self.nombre_face_pillier = None

    def creer_mur(self, j, i, o, epaisseur):
        #coos d'un mur horizontal à l'origine
        e = epaisseur #epaisseur du mur
        sommets_mur_h = [ [e, 0.0,  0.0], [e,  0.0,  e], [e,  1.0,  0.0], [e,  1.0,  e], [1.0,  0.0,  0.0], [1.0,  0.0,  e], [1.0,  1.0,  0.0], [1.0,  1.0,  e] ]
        sommets_mur_g = [ [0.0, 0.0,  e], [e,  0.0,  e], [0.0,  1.0,  e], [e,  1.0,  e], [0.0,  0.0,  1.0], [e,  0.0,  1.0], [0.0,  1.0,  1.0], [e,  1.0,  1.0] ]
        faces_mur = [   [[1,9,2], [7,12,2], [5,10,2] ], [[1,9,2], [3,11,2], [7,12,2] ], [[1,5,4], [4,2,4], [3,1,4]] , [[1,5,4], [2,6,4], [4,2,4]], [[5,8,3], [7,4,3], [8,3,3]], [[5,8,3], [8,3,3], [6,7,3]], [[2,6,1], [6,7,1], [8,3,1]], [[2,6,1], [8,3,1], [4,2,1]]   ]
        self.nombre_face_mur = len(faces_mur)
        if o: #si c'est un mur horizontal
            sommets_mur = sommets_mur_h
        else:
            sommets_mur = sommets_mur_g
        
        for sommet in sommets_mur:
            sommet[0] += i
            sommet[2] += j
        self.sommets += sommets_mur

        for face in faces_mur:
            for coin in face:
                coin[0] += self.nombre_face_mur*self.nombre_murs
        self.faces += faces_mur
        self.nombre_murs +=1

    def creer_pillier(self, j, i, epaisseur):
        e = epaisseur #epaisseur du pillier = du mur
        sommets_pillier = [ [0.0, 0.0,  0.0], [0.0,  0.0,  e], [0.0,  1.0,  0.0], [0.0,  1.0,  e], [e,  0.0,  0.0], [e,  0.0,  e], [e,  1.0,  0.0], [e,  1.0,  e] ]
        faces_pillier = [   [[1,1,1], [7,1,1], [5,1,1] ], [[1,1,1], [3,1,1], [7,1,1] ], [[1,1,3], [4,1,3], [3,1,3]] , [[1,1,3], [2,1,3], [4,1,3]], [[5,1,4], [7,1,4], [8,1,4]], [[5,1,4], [8,1,4], [6,1,4]], [[2,1,2], [6,1,2], [8,1,2]], [[2,1,2], [8,1,2], [4,1,2]]   ]
        self.nombre_face_pillier = len(faces_pillier)

        for sommet in sommets_pillier:
            sommet[0] += i
            sommet[2] += j

        self.sommets += sommets_pillier

        for face in faces_pillier:
            for coin in face:
                coin[0] += self.nombre_face_pillier * self.nombre_piliers + self.nombre_face_mur * self.nombre_murs

        self.faces += faces_pillier
        self.nombre_piliers +=1


def gen_maillage(mat,e):
    m = Maillage()
    TAILLE_LABY = len(mat[0])
    for i in range(TAILLE_LABY):
        for j in range(TAILLE_LABY):
            if mat[i][j] == 0:
                m.creer_mur(i,j,0,e)
            elif mat[i][j] == 3:
                m.creer_mur(i,j,1,e)
            elif mat[i][j] == 1:
                m.creer_mur(i,j,0,e)
                m.creer_mur(i,j,1,e)
    for i in range(TAILLE_LABY):
        for j in range(TAILLE_LABY):
            m.creer_pillier(i,j,e)
    print("Il y a ", m.nombre_murs, " murs dans le labyrinthe.")
    return m

def maillage_vers_obj(m, chemin_fichier):

    with open(chemin_fichier, 'w') as f:
        f.write("# OBJ file\n")

        for v in m.sommets:
            f.write("v ")
            f.write(''.join(str(x) + ' ' for x in v) )
            f.write("\n")

        for vt in m.textures:
            f.write("vt ")
            f.write(''.join(str(x) + ' ' for x in vt) )
            f.write("\n")

        for vn in m.normales:
            f.write("vn ")
            f.write(''.join(str(x) + ' ' for x in vn) )
            f.write("\n")

        for face in m.faces:
            f.write("f ")
            for coin in face:
                    f.write(str(coin[0]) + '/' + str(coin[1]) + '/' + str(coin[2]) + ' ')
            f.write("\n")

def nouveau_obj_laby(matrice_laby, chemin_fichier, e):
    #print(np.array(matrice_laby))
    m = gen_maillage(matrice_laby,e)
    maillage_vers_obj(m, chemin_fichier)

if __name__ == '__main__':
    nouveau_obj_laby(10,'laby.obj')

    
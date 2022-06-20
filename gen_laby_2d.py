
#on gere nos collisions en 2D, et on va les optimiser avec ce programme
#on va generer une grille en 2D (c est juste un tableau) ou chaque case va contenir une reference a tout les murs qui l entoure
#au lieu de tester tout les murs du laby, on va tester seulement les 12 murs autours d une case

from collision import Rectangle
import gen_laby_mat
import numpy as np

class Murs():
    def __init__(self, mat, eppaiseur_mur):

        self.TAILLE = len(mat[0]) - 1 #nombre de case sur un cote du laby, taille de la grille donc
        self.LIMITE = self.TAILLE + 2 # taille de self.mat
        self.grille = [[[] for _ in range(self.TAILLE)] for _ in range(self.TAILLE)]
        self.e = eppaiseur_mur
        self.u = 1

        self.mat = self.maj_mat(mat) # de taille self.LIMITE


        self.matrice_vers_grille()

    def maj_mat(self, mat): #pour eviter les galeres d indices, on ajoute une ligne au dessus de mat et une colonne a gauche de mat
        mat2 = [ [2]*(self.LIMITE) for _ in range(self.LIMITE)]
        for i in range(1,self.LIMITE):
            for j in range(1,self.LIMITE):
                mat2[i][j] = mat[i-1][j-1]
        return np.array(mat2)


    def matrice_vers_grille(self):
        #print('self.mat ', len(self.mat))
        #print('self.grille ', len(self.grille))

        #on parcours la matrice pour creer notre grille ON NE VA PAS SUR LES BORDS

        for i in range(0,self.TAILLE):
            p = i + 1
            for j in range(0,self.TAILLE):
                q = j + 1


                # 0 1 2
                # 3 4 5
                # 6 7 8

                #0 pas de murs interessants
                
                if self.mat[p-1][q] in [1,0]: #1
                    y = (i-1) * self.u
                    x = j * self.u
                    l = self.e
                    h = self.u

                    self.grille[i][j].append(Rectangle(x,y,l,h))

                if self.mat[p-1][q+1] in [1,0]: #2
                    y = (i-1) * self.u
                    x = (j+1) * self.u
                    l = self.e
                    h = self.u
                    self.grille[i][j].append(Rectangle(x,y,l,h))

                if self.mat[p][q-1] in [1,3]: #3
                    y = (i) * self.u
                    x = (j-1) * self.u
                    l = self.u
                    h = self.e
                    self.grille[i][j].append(Rectangle(x,y,l,h))

                if self.mat[p][q] in [1,3]: # 4 deux murs possibles
                    y = (i) * self.u
                    x = (j) * self.u
                    l = self.u
                    h = self.e
                    self.grille[i][j].append(Rectangle(x,y,l,h))
                if self.mat[p][q] in [1,0]: #4 deuxieme mur
                    y = (i) * self.u
                    x = (j) * self.u
                    l = self.e
                    h = self.u
                    self.grille[i][j].append(Rectangle(x,y,l,h))

                if self.mat[p][q+1] in [1,3]: # 5 deux murs possibles
                    y = (i) * self.u
                    x = (j+1) * self.u
                    l = self.u
                    h = self.e
                    self.grille[i][j].append(Rectangle(x,y,l,h))
                if self.mat[p][q+1] in [1,0]: #5 deuxieme mur
                    y = (i) * self.u
                    x = (j+1) * self.u
                    l = self.e
                    h = self.u
                    self.grille[i][j].append(Rectangle(x,y,l,h))

                if self.mat[p+1][q-1] in [1,3]: #6
                    y = (i+1) * self.u
                    x = (j-1) * self.u
                    l = self.u
                    h = self.e
                    self.grille[i][j].append(Rectangle(x,y,l,h))

                if self.mat[p+1][q] in [1,3]: # 7 deux murs possibles
                    y = (i+1) * self.u
                    x = (j) * self.u
                    l = self.u
                    h = self.e
                    self.grille[i][j].append(Rectangle(x,y,l,h))
                if self.mat[p+1][q] in [1,0]: #7 deuxieme mur
                    y = (i+1) * self.u
                    x = (j) * self.u
                    l = self.e
                    h = self.u
                    self.grille[i][j].append(Rectangle(x,y,l,h))

                if self.mat[p+1][q+1] in [1,3]: # 8 deux murs possibles
                    y = (i+1) * self.u
                    x = (j+1) * self.u
                    l = self.u
                    h = self.e
                    self.grille[i][j].append(Rectangle(x,y,l,h))
                if self.mat[p+1][q+1] in [1,0]: #8 deuxieme mur
                    y = (i+1) * self.u
                    x = (j+1) * self.u
                    l = self.e
                    h = self.u
                    self.grille[i][j].append(Rectangle(x,y,l,h))

                

if __name__ == '__main__':
    N = 5
    print("N = ", N)
    mat = gen_laby_mat.genere(N)
    murs = Murs(mat,0.09,1)




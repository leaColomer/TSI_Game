
#on gere nos collisions en 2D, et on va les optimiser avec ce programme
#on va generer une grille en 2D (c est juste un tableau) ou chaque case va contenir une reference a tout les murs qui l entoure
#au lieu de tester tout les murs du laby, on va tester seulement les 12 murs autours d une case

from collision import Rectangle
import gen_laby_mat
import numpy as np

class Murs():
    def __init__(self, mat, eppaiseur_mur, unite):
        self.mat = mat
        self.TAILLE = len(mat[0]) + 1
        self.grille = [ [[]]*self.TAILLE for _ in range(self.TAILLE)]
        self.e = eppaiseur_mur
        self.u = unite

        self.maj_mat()
        self.matrice_vers_grille()

    def maj_mat(self): #pour eviter les galeres d indices, on ajoute une ligne au dessus de mat et une colonne a gauche de mat
        mat2 = [ [2]*self.TAILLE for _ in range(self.TAILLE)]
        for i in range(1,self.TAILLE):
            for j in range(1,self.TAILLE):
                mat2[i][j] = self.mat[i-1][j-1]
        self.mat = mat2


    def matrice_vers_grille(self):


        #on parcours la matrice pour creer notre grille
        for i in range(1,self.TAILLE-1):
            for j in range(1,self.TAILLE-1):

                # 0 1 2
                # 3 4 5
                # 6 7 8

                #0 pas de murs interessants
                if self.mat[i-1][j] in [1,0]: #1
                    x = (i-1) * self.u
                    y = j * self.u
                    l = self.e
                    h = self.u
                    self.grille[i][j].append(Rectangle(x,y,l,h))

                if self.mat[i-1][j+1] in [1,0]: #2
                    x = (i-1) * self.u
                    y = (j+1) * self.u
                    l = self.e
                    h = self.u
                    self.grille[i][j].append(Rectangle(x,y,l,h))

                if self.mat[i][j-1] in [1,3]: #3
                    x = (i) * self.u
                    y = (j-1) * self.u
                    l = self.u
                    h = self.e
                    self.grille[i][j].append(Rectangle(x,y,l,h))

                if self.mat[i][j] in [1,3]: # 4 deux murs possibles
                    x = (i) * self.u
                    y = (j) * self.u
                    l = self.u
                    h = self.e
                    self.grille[i][j].append(Rectangle(x,y,l,h))
                if self.mat[i][j] in [1,0]: #4 deuxieme mur
                    x = (i) * self.u
                    y = (j) * self.u
                    l = self.e
                    h = self.u
                    self.grille[i][j].append(Rectangle(x,y,l,h))

                if self.mat[i][j+1] in [1,3]: # 5 deux murs possibles
                    x = (i) * self.u
                    y = (j+1) * self.u
                    l = self.u
                    h = self.e
                    self.grille[i][j].append(Rectangle(x,y,l,h))
                if self.mat[i][j+1] in [1,0]: #5 deuxieme mur
                    x = (i) * self.u
                    y = (j+1) * self.u
                    l = self.e
                    h = self.u
                    self.grille[i][j].append(Rectangle(x,y,l,h))

                if self.mat[i+1][j-1] in [1,3]: #6
                    x = (i+1) * self.u
                    y = (j-1) * self.u
                    l = self.u
                    h = self.e
                    self.grille[i][j].append(Rectangle(x,y,l,h))

                if self.mat[i+1][j] in [1,3]: # 7 deux murs possibles
                    x = (i+1) * self.u
                    y = (j) * self.u
                    l = self.u
                    h = self.e
                    self.grille[i][j].append(Rectangle(x,y,l,h))
                if self.mat[i+1][j] in [1,0]: #7 deuxieme mur
                    x = (i+1) * self.u
                    y = (j) * self.u
                    l = self.e
                    h = self.u
                    self.grille[i][j].append(Rectangle(x,y,l,h))

                if self.mat[i+1][j+1] in [1,3]: # 8 deux murs possibles
                    x = (i+1) * self.u
                    y = (j+1) * self.u
                    l = self.u
                    h = self.e
                    self.grille[i][j].append(Rectangle(x,y,l,h))
                if self.mat[i+1][j+1] in [1,0]: #8 deuxieme mur
                    x = (i+1) * self.u
                    y = (j+1) * self.u
                    l = self.e
                    h = self.u
                    self.grille[i][j].append(Rectangle(x,y,l,h))

if __name__ == '__main__':
    N = 3
    mat = gen_laby_mat.genere(N)
    murs = Murs(mat,0.09,1)


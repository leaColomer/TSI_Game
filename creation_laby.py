#Generation de labyrinthe par backtracking
#on par du centre du laby, on choisit une direction au hasard sur 4 et on creuse dans cette dir
#si sans issue, on revient sur nos pas jusqua une case avec une direction de libre et on reprend

#on sauvegarde le laby dans une matrice ou chaque case indique si il y a un mur a gauche, en haut ou les deux

from random import sample
import numpy as np
 
N, S, E, W = 1, 2, 4, 8
OPPOSITE = {N: S, S: N, E: W, W: E}
MOVE = {N: lambda x, y: (x, y-1),
        S: lambda x, y: (x, y+1),
        E: lambda x, y: (x+1, y),
        W: lambda x, y: (x-1, y)}
 
def chemins_aleatoire():
    return sample((N, S, E, W), 4)
 
def generation_laby(TAILLE):
    laby = [ [0]*TAILLE for _ in range(TAILLE)]
    dir_possibles = [(TAILLE//2, TAILLE//2, d) for d in chemins_aleatoire()]
 
    while dir_possibles:
        x, y, way = dir_possibles.pop()
        x_svnt, y_svnt = MOVE[way](x, y)
        if 0 <= y_svnt < TAILLE and 0 <= x_svnt < TAILLE and laby[y_svnt][x_svnt] == 0: #si la case suivante ne donne pas sur un couloir deja creuse ET si on ne sort pas du laby
            laby[y][x] |= way
            laby[y_svnt][x_svnt] |= OPPOSITE[way]
            dir_possibles += [(x_svnt, y_svnt, d) for d in chemins_aleatoire()] #on ajoute les 4 dir possibles de la case suivante
 
    return laby

def convertion(laby1):
    t = len(laby1) + 1
    laby2 = [ [2]*t for _ in range(t)]
    for i in range(t-1):
        for j in range(t-1):
            x = laby1[i][j]
            laby2[i][j] = (x+1)%2 + 2*(x>7)
    for i in range(t-1):
        laby2[i][t-1] = 0
    for j in range(t-1):
        laby2[t-1][j] = 3
    return laby2


def matrice_laby_alea(TAILLE):
    lab = generation_laby(TAILLE)
    return convertion(lab)


if __name__ == '__main__':

    laby = generation_laby(9)

    print(np.array(laby))
    print(np.array(convertion(laby)))

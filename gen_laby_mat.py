#Generation de labyrinthe par backtracking
#on par du centre du laby, on choisit une direction au hasard sur 4 et on creuse dans cette dir
#si sans issue, on revient sur nos pas jusqua une case avec une direction de libre et on reprend

#on sauvegarde le laby dans une matrice ou chaque case indique si il y a un mur a gauche, en haut ou les deux

from lib2to3.pytree import convert
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

#genere une matrice dont chaque element contient l'information de presence des 4 murs autour de lui
def generation_laby(TAILLE):
    laby = [ [0]*TAILLE for _ in range(TAILLE)]
    dir_possibles = [(TAILLE//2, TAILLE//2, N, 0)]

    case_finale = [TAILLE//2, TAILLE//2]
    longueur_max = 0
 
    while dir_possibles:
        x, y, dir, dist = dir_possibles.pop()
        x_svnt, y_svnt = MOVE[dir](x, y)
        if 0 <= y_svnt < TAILLE and 0 <= x_svnt < TAILLE and laby[y_svnt][x_svnt] == 0: #si la case suivante ne donne pas sur un couloir deja creuse ET si on ne sort pas du laby
            laby[y][x] |= dir
            laby[y_svnt][x_svnt] |= OPPOSITE[dir]
            dir_possibles += [(x_svnt, y_svnt, d, dist+1) for d in chemins_aleatoire()] #on ajoute les 4 dir possibles de la case suivante
        if longueur_max < dist+1:
            longueur_max = dist+1
            case_finale = [x, y]
    return laby, longueur_max, case_finale

#on reduit l'information aux murs superieur et gauche par case : ca permettra de generer les murs une seule fois plus tard
#on ne perd evidemment pas d'information sur le laby global
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


def genere(TAILLE):
    mat, longueur, [x,y] = generation_laby(TAILLE)
    return convertion(mat), longueur, [x,y]


#genere un laby dont la solution est de taille renseignee
def genere_spe(TAILLE,longueur_chem_parf,e_max):
    ecart = e_max + 1
    while ecart > e_max:
        mat, longueur, [x,y] = generation_laby(TAILLE)
        ecart = abs(longueur_chem_parf-longueur)
    return convertion(mat), longueur, [x,y]

if __name__ == '__main__':
    res = []
    for _ in range(100):
        mat, longueur, [x,y] = generation_laby(14)
        res.append(longueur)
    print(np.average(res))
    print(np.std(res))

    # print(np.array(mat))
    
    # print(np.array(convertion(mat)))

    # print('longueur max = ', longueur, x, y)
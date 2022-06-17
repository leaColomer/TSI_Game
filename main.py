from viewerGL import ViewerGL
import objets_ini

def main():
    viewer = ViewerGL()

    viewer.TRICHE = 0 # 0 pas de triche, 1 triche

    viewer.TAILLE_LABY = 14 #taille du cote du labyrinthe
    viewer.LONGUEUR_CHEMIN_PARFAIT = 97 #chemin de 97 cases c'est bien pour 60s
    viewer.epaisseur_mur = 0.09
    viewer.unite = 1 #longeur d'un mur OU PLUTOT D'UNE CASE DU LABY
    viewer.rayon_perso = 0.1 # 0.3*viewer.unite


    objets_ini.initialisation(viewer)



    viewer.run()


if __name__ == '__main__':
    main()
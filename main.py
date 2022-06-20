from viewerGL import ViewerGL
import objets_ini

def main():
    viewer = ViewerGL()

    viewer.TRICHE = 0 # 0 pas de triche, 1 triche

    viewer.SENSI = 0.005
    viewer.VITESSE = 1.5 # case par seconde



    viewer.TEMPS = 60
    viewer.TAILLE_LABY = 14 #taille du cote du labyrinthe  
    viewer.LONGUEUR_CHEMIN_PARFAIT = 98 #chemin de 98 cases c'est bien pour 60s, environ 5s de rab
    viewer.epaisseur_mur = 0.09
    viewer.rayon_perso = 0.1


    objets_ini.initialisation(viewer)



    viewer.run()


if __name__ == '__main__':
    main()
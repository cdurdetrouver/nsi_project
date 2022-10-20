from script.game import Game

if __name__ == "__main__":
    game = Game((720,480),"fusée", 60) # creation de la fenetre de jeu (taille, titre, FPS)
    game.run() # debut du jeu
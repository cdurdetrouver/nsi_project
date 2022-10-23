#recuperer la taille de l'ecran
from script.game.game import Game
import ctypes 
user32 = ctypes.windll.user32
screensize = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

if __name__ == "__main__":
    game = Game(screensize, "fusée") # creation de la fenetre de jeu (taille, titre, FPS)
    game.run() # debut du jeux
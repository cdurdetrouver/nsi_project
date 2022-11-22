from script.game.game import Game
import ctypes
user32 = ctypes.windll.user32
screensize = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)) # recuperer les dimanesions de l'ecran de l'utilisateur

MDP = "9phS7mUHz7UtTfTg" # mot de passe pour la base de donnees en ligne

if __name__ == "__main__":
    game = Game(screensize, "super fusée", MDP) # creation de la fenetre de jeu (taille, titre, FPS)
    game.run() # debut du jeux
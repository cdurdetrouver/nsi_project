from pymongo import MongoClient
import pygame

class Classement():
    def __init__(self, size):
        self.size = size

        self.connexion = None

        # texte du classement
        pygame.font.init()
        self.font = pygame.font.SysFont("font/font.ttf", 256) # police d'ecriture

        self.image_rang = self.font.render("Rang", True, (255,255,255))
        self.image_pseudo = self.font.render("Pseudo", True, (255,255,255))
        self.image_score = self.font.render("Score", True, (255,255,255))

    def connect(self):
        try : 
            self.liste_resultats = []
            self.cluster = MongoClient("mongodb+srv://user:Rs2Toxno8enOGj7Y@cluster0.vemkby5.mongodb.net/?retryWrites=true&w=majority")
            db = self.cluster["nsi_project"]
            self.collection = db["scores"]

            results = self.collection.find({})

            for result in results:
                self.liste_resultats.append(result)

            self.connexion = True
            
        except Exception as exc:
            self.connexion = False

    def get_connexion(self):
        return self.connexion
    
    def new_res(self, size):
        self.size = size

        self.image_rang = pygame.transform.scale(self.image_rang, (self.size[1] * 5/100 * self.image_rang.get_size()[0] / self.image_rang.get_size()[1],self.size[1] * 5/100))
        self.image_score = pygame.transform.scale(self.image_score, (self.size[1] * 5/100 * self.image_score.get_size()[0] / self.image_score.get_size()[1] ,self.size[1] * 5/100))
        self.image_pseudo = pygame.transform.scale(self.image_pseudo, (self.size[1] * 5/100 * self.image_pseudo.get_size()[0] / self.image_pseudo.get_size()[1] ,self.size[1] * 5/100))
        self.width = 20 + self.image_score.get_size()[0] + 20 + 40 + self.image_pseudo.get_size()[0] + 40 + 20 + self.image_rang.get_size()[0] + 20
        self.height = (20 + self.image_pseudo.get_size()[1]) * 10

    def update_classement(self, user_name, score):
        if not(self.connexion):
            return

        already = False

        for i in range(len(self.liste_resultats)):
            if self.liste_resultats[i]["name"] == user_name and score > self.liste_resultats[i]["score"]:
                self.collection.update_one(
                    { "name": user_name }, 
                    { "$set" :{ "score": score } }
                )
                already = True
            else:
                return

        if not(already):
            post = {
                "name" : user_name,
                "score" : score
            }
            self.collection.insert_one(post)

        self.liste_resultats = []

        results = self.collection.find({})

        for result in results:
            self.liste_resultats.append(result)

        self.tri_liste()

    def tri_liste(self):
        for i in range(len(self.liste_resultats)):
            for j in range(len(self.liste_resultats) - 1):
                if self.liste_resultats[j]["score"] < self.liste_resultats[j + 1]["score"]:
                    self.liste_resultats[j], self.liste_resultats[j + 1] = self.liste_resultats[j + 1], self.liste_resultats[j]

    def afficher(self, screen):

        if not(self.connexion):
            image = self.font.render("no connexion", True, (255,255,255))
            image = pygame.transform.scale(image,(self.size[0] * 30/100, image.get_size()[1]/image.get_size()[0] * self.size[0] * 30/100))
            screen.blit(image, (self.size[0]//2 - image.get_size()[0]//2, self.size[1]//2 - image.get_size()[1]//2))
            return
        
        screen.blit(self.image_rang, (self.size[0]//2 - self.width//2 + 20, self.size[1]//2 - self.height//2))
        screen.blit(self.image_pseudo, (self.size[0]//2 - self.width//2 + 80 + self.image_rang.get_size()[0], self.size[1]//2 - self.height//2))
        screen.blit(self.image_score, (self.size[0]//2 - self.width//2 + 140 + self.image_rang.get_size()[0] + self.image_pseudo.get_size()[0], self.size[1]//2 - self.height//2))

        for i in range(10):
            if i < len(self.liste_resultats):
                nb = self.font.render(str(i + 1), True , (255,255,255))
                nb = pygame.transform.scale(nb, (self.size[1] * 5/100 * nb.get_size()[0] / nb.get_size()[1],self.size[1] * 5/100))
                
                pseudo = self.font.render(self.liste_resultats[i]["name"], True , (255,255,255))
                pseudo = pygame.transform.scale(pseudo, (self.size[1] * 5/100 * pseudo.get_size()[0] / pseudo.get_size()[1],self.size[1] * 5/100))
                
                score = self.font.render(str(self.liste_resultats[i]["score"]), True , (255,255,255))
                score = pygame.transform.scale(score, (self.size[1] * 5/100 * score.get_size()[0] / score.get_size()[1],self.size[1] * 5/100))

                screen.blit(nb, (self.size[0]//2 - self.width//2 + 20 + self.image_rang.get_size()[0]//2 - nb.get_size()[0]//2,self.size[1]//2 - self.height//2 + self.image_rang.get_size()[1] + 10 + 10 * (i + 1) + nb.get_size()[1] * i))
                screen.blit(pseudo, (self.size[0]//2 - self.width//2 + 80 + self.image_rang.get_size()[0] + self.image_pseudo.get_size()[0]//2 - pseudo.get_size()[0]//2,self.size[1]//2 - self.height//2 + self.image_rang.get_size()[1] + 10 + 10 * (i + 1) + pseudo.get_size()[1] * i))
                screen.blit(score, (self.size[0]//2 - self.width//2 + 140 + self.image_rang.get_size()[0] + self.image_pseudo.get_size()[0] + self.image_score.get_size()[0]//2 - score.get_size()[0]//2,self.size[1]//2 - self.height//2 + self.image_rang.get_size()[1] + 10 + 10 * (i + 1) + score.get_size()[1] * i))

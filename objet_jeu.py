import objet_snake
from random import randint

class Jeu:
    
    def __init__(self):
        """
        Fonction de création du jeu
        possède toute les variable importante
        """
        
        self.taille_terrain = 16

        self.terrain = self.creation_terrain(self.taille_terrain)
        self.serpent = self.creation_serpent()
        
        self.mort = False
        self.spawn_pomme = False
        self.creation_pomme()
        
        
        
        while self.mort!= True:
            self.tour(randint(1,4))
           
            if self.mort == True:
                break

    def reset(self):
        """
        Fait le reset du jeu en remettant ses variables importante à leur valeur de départ
        """
        self.taille_terrain = 16

        self.terrain = self.creation_terrain(self.taille_terrain)
        self.serpent = self.creation_serpent()
        
        self.mort = False
        self.spawn_pomme = False
        self.creation_pomme()

    def creation_terrain(self,taille_terrain):
        """
        renvoie un tableau à deux dimension avec les bordures délimiter par les valeur 3 et 4
        taille_terrain -- longueur des cotés du terrain
        """
        
        self.terrain = [[0 for _ in range(taille_terrain)] for _ in range(taille_terrain)]
        
        #le 3 correspond au mur du haut et du bas
        #
        #le 4 correspond au mur de droite et de gauche
        for i in range(len(self.terrain[0])):
            self.terrain[0][i] = 4
        for i in range(len(self.terrain[-1])):
            self.terrain[-1][i] = 4
        for i in range(len(self.terrain)):
            self.terrain[i][0] = 3
        for i in range(len(self.terrain)):
            self.terrain[i][-1] = 3

        return self.terrain

    def affichage_terrain(self,terrain):
        """
        Permet d'écrire le terrain dans la console
        
        Sert à tester le fonctionnement du jeu avec uniquement les tableaux
        """
        for i in range(len(self.terrain)):
            print(self.terrain[i])
            
            
    def creation_serpent(self):
        """
        Place un objet serpent sur le terrain et le renvoie
        """
        self.serpent = objet_snake.serpent
        self.serpent.__init__(self.serpent)

        for v in self.serpent.position_corps:
            self.terrain[v[0]][v[1]] = 1
            
        return self.serpent


    def avancement(self):
        """
        Met à jour la position du serpent sur le terrain
        """
        self.terrain[self.serpent.position_tete[0]][self.serpent.position_tete[1]] = 1
        
        if self.spawn_pomme == False:
            self.terrain[self.serpent.position_corps[-1][0]][self.serpent.position_corps[-1][1]] = 0
                

    def test_mort(self):
        """
        Renvoie True si le serpent est sensé mourir sinon False
        """
        if not 0<self.serpent.position_tete[0]<self.taille_terrain-1 or not 0<self.serpent.position_tete[1]<self.taille_terrain-1:
            return True
        elif self.terrain[self.serpent.position_tete[0]][self.serpent.position_tete[1]] == 1:
            return True
        
        
        return False
    
    
    
    def creation_pomme(self):
        """
        Créer une nouvelle pomme sur le terrain
        """
        while True:
            self.x_pomme = randint(1,self.taille_terrain-2)
            self.y_pomme = randint(1,self.taille_terrain-2)
            
            if self.terrain[self.x_pomme][self.y_pomme] != 1:
                self.terrain[self.x_pomme][self.y_pomme] = 2
                break
    
    def sur_pomme(self):
        """
        Regarde si le serpent se trouve sur une pomme, si oui il renvoie True
        """
        if self.terrain[self.serpent.position_tete[0]][self.serpent.position_tete[1]] == 2:
            self.serpent.manger_pomme(self.serpent)
            self.spawn_pomme = True
        


    def tour(self,sens):
        """
        Fonction principale du jeu
        S'occupe de faire tous les mouvement du serpent et regarde si il mange une pomme ou si il est mort
        
        sens -- sens dans lequel le serpent avancera pour ce tour
        fonctionnement du sens :
            3
            |
        2---|---4
            |
            1
        """
        # Avance la tête du serpent
        self.serpent.mouvement(self.serpent,sens)
        
        
        # Traitement du programme
        # Regarde si le serpent est mort ou si il est sur une pomme
        self.mort = self.test_mort()
        self.sur_pomme()
        
        # Met à jour le tableau terrain
        self.avancement()

        # Actions à faire si il a mangé une pomme
        if self.spawn_pomme == True:
            self.creation_pomme()
            self.spawn_pomme = False
            
        # Met à jour les coordonnées du corps du serpent        
        self.serpent.mis_a_jour_corps(self.serpent)
        
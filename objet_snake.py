class serpent:
    def __init__(self):
        """      
        Fonction de création d'un objet serpent
        
        Créer toure les variables importantes de l'objet serpent       
        """
        
        
        self.taille = 3
        
        self.sens_actuel = 3
        #fonctionnement coordonnées du tableau :
        #tableau[y][x]      ex: [0,0]-[0,1]-[0,2]
        #                       [1,0]-[1,1]-[1,2]
        #                       [2,0]-[2,1]-[2,2]
        self.position_corps = [[y,7] for y in range(7,10)]
        self.position_tete = [7,7]
        
    
    def mouvement(self,sens):
        """
        Bouge la tête du serpent suite à un mouvement
        
        sens -- sens dans lequel part le serpent
        fonctionnement du sens :
            3
            |
        2---|---4
            |
            1
        """
        
        #Si le serpent veut partir au sens opposé de son sens actuel
        #l'absolue de la valeur de son sens moins celui de son opposé vaudra
        #forcément 2.
        #Dans ce cas là, le serpent continura son chemin tout droit pour ne pas
        #partir sur sa queue
        if abs(self.sens_actuel - sens) != 2:
            self.sens_actuel = sens
        
        if self.sens_actuel == 3:
            self.position_tete[0] -=1
        elif self.sens_actuel == 4:
            self.position_tete[1] -=1
        elif self.sens_actuel == 1:
            self.position_tete[0] +=1
        else:
            self.position_tete[1] +=1
            
    def mis_a_jour_corps(self):
        """
        Met en place les coordonnés actuel du serpent pour qu'ils puissent ainsi être utiliser
        correctement
        """
        del self.position_corps[-1]
        self.position_corps.insert(0,[self.position_tete[0],self.position_tete[1]])
                
    
    def manger_pomme(self):
        """
        Augmente la taille du serpent
        """
        self.taille += 1
        
        #Lors la fonction 'mis_a_jour_corps',qui est forcément appelé à chaque tour, on supprime le dernier
        #élément de position_corps, on dupplique son dernier élément pour que le serpent
        #puisse grandir
        self.position_corps.append([self.position_corps[-1][0],self.position_corps[-1][1]])           
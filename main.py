import curses
import math
from objet_jeu import Jeu
import sys

# ====> A LIRE <====
# Il faut que la fenettre ne soit pas trop petite
# Si vous avez une erreur cela peut venir du manque de : pip install windows-curses


# TEXTES AFFICHAGES
TITLE_SNAKE = [
    "      ___           ___           ___           ___           ___     ",
    "     /  /\         /  /\         /  /\         /  /\         /  /\    ",
    "    /  /::\       /  /::|       /  /::\       /  /:/        /  /::\   ",
    "   /__/:/\:\     /  /:|:|      /  /:/\:\     /  /:/        /  /:/\:\  ",
    "  _\_ \:\ \:\   /  /:/|:|__   /  /::\ \:\   /  /::\____   /  /::\ \:\ ",
    " /__/\ \:\ \:\ /__/:/ |:| /\ /__/:/\:\_\:\ /__/:/\:::::\ /__/:/\:\ \:\\",
    " \  \:\ \:\_\/ \__\/  |:|/:/ \__\/  \:\/:/ \__\/~|:|~~~~ \  \:\ \:\_\/",
    "  \  \:\_\:\       |  |:/:/       \__\::/     |  |:|      \  \:\ \:\  ",
    "   \  \:\/:/       |__|::/        /  /:/      |  |:|       \  \:\_\/  ",
    "    \  \::/        /__/:/        /__/:/       |__|:|        \  \:\    ",
    "     \__\/         \__\/         \__\/         \__\|         \__\/    ",
]

GAME_OVER = [
    "   ______                                    ____                      ",
    "  / ____/  ____ _   ____ ___   ___          / __ \ _   __  ___    _____",
    " / / __   / __ `/  / __ `__ \ / _ \        / / / /| | / / / _ \  / ___/",
    "/ /_/ /  / /_/ /  / / / / / //  __/       / /_/ / | |/ / /  __/ / /    ",
    "\____/   \__,_/  /_/ /_/ /_/ \___/        \____/  |___/  \___/ /_/     ",
                                                                       
]


# FONCTIONS UTILES / AFFICHAGES
def getCenter(parentSize, childSize):
    """
    Retourne une coorodonnée pour aligner au centre un élément:
    parentSize  -- taille de l'élément contenant l'élement plus petit
    childSize   -- taille de l'élément rentrant dans l'autre
    
    """
    return math.floor(parentSize/2.0) - math.floor(childSize/2.0)

def getCenterCo(lines, columns, width, height):
    """
    Retourne les coordonnées pour aligne un élément sur l'abscisse et les ordonnées
    lines   -- nombre de lignes de l'élément parent
    columns -- nombre de colones de l'élément parent
    width   -- largeur de l'élément enfant
    height  -- hauteur de l'élément enfant

    """
    return getCenter(columns, width), getCenter(lines, height)

def showText(window, text, x, y, center = False, effect=None, *args):
    """
    Affiche du texte dans une fenêtre curses 
    window -- fenetre curses où on met le text
    text   -- texte affiché
    x      -- coordonnée x
    y      -- coordonnée y
    center -- aligner au centre en origine et en ordonné (mettre x et y à 0)
    effect -- appliquer un effet d'apparition (None : basique, taper : comme si on écrivait au clavier)
    args   -- ajouter des propriétées 

    """

    lines, columns = window.getmaxyx()
    width, height = len(text), 1

    if center:
        x, y = getCenterCo(lines, columns-x, width, height-y)

    if effect == None: 
        window.addstr(y, x, text, *args)
    
    elif effect == "taper": # comme si on écrivait au clavier
        i = 0
        for l in text: # affiche colone par colone
            window.addstr(y, x+i, l, *args)
            curses.napms(80)

            window.refresh()
            i +=1

    return (y, x), (y, x + len(text))

def showArray(window, array, x, y, center = False, *args):
    """
    Affiche différente ligne d'un tableau dans une fenêtre curses 
    window -- fenetre curses où on met le text
    array  -- tableau affiché
    x      -- coordonnée x
    y      -- coordonnée y
    center -- aligner au centre en origine et en ordonné (mettre x et y à 0)
    args   -- ajouter des propriétées 

    """
    i = 0
    lines, columns = window.getmaxyx()
    width, height = len(array[0]), len(array)



    if width + x <= columns and height + y <= lines:
        if center:
            x, y = getCenterCo(lines, columns-x, width, height-y)

        for text in array:
            window.addstr(y+i, x, text, *args)
            
            i += 1
    else:
        window.addstr(y,x,"[Espace insuffisant]") # si la fenêtre est trop petite

def clearArea(window, starty, startx, endy, endx):
    """
    Effacer une zone précise (forme de rectangle)
    window -- fenetre curses où on efface
    starty -- coordonnée x du premier point
    startx -- coordonnée y du premier point
    endy   -- coordonnée x du second point
    endx   -- coordonnée y du second point
    
    """
    for y in range(starty, endy+1):        
        for x in range(startx, endx):
            window.addch(y, x, " ")

def beautifulClear(window, color=1, time=5):
    """
    Effacer toute la fenêtre de gauche vers la droite 
    window -- fenetre curses où on efface
    color  -- code couleur défenis avant
    time   -- temps d'attente entre chaques colones
     
    """
    for x in range(0, curses.COLS):
        for y in range(curses.LINES):
            try:
                window.addch(y, x, " ", curses.color_pair(color))
            except: pass

        window.refresh()
        curses.napms(time)
        

# FONCTIONS PRINCIPALES
def startMenuGame():
    """
    Afficher le menu du démarage 
    """

    # Paramètres curses
    curses.noecho()
    screen.bkgd(' ', curses.color_pair(2))

    # Première Frame
    showArray(screen, TITLE_SNAKE, 0,-10, center=True)
    areaText = showText(screen, "Cliquer sur entree pour lancer le jeu !", 0, 10, center=True, effect="taper")
    screen.refresh()

    screen.getch() # attend une entrée
    
    # Seconde Frame
    clearArea(screen, *areaText[0], *areaText[1])
    curses.echo()
    areaText = showText(screen, "Tapes ton pseudo : ", 0, 10, center=True, effect="taper")
    name = screen.getstr().decode()
    curses.noecho()

    screen.refresh()

    # Denière Frame
    clearArea(screen, *areaText[0], areaText[1][0], areaText[1][1] + len(name))
    areaText = showText(screen, f"Bonne partie {name}!", 0, 10, center=True, effect="taper")
    screen.refresh()

    curses.napms(1000)    
    beautifulClear(screen)

def startGame():
    """
    Lancer le snake, initialiser les variable de base et lancer la boucle infini du jeu.
    """

    screen.erase()
    screen.bkgd(' ', curses.color_pair(2))

    updateDisplayGame(screen, game.terrain)
    screen.refresh()
    screen.keypad(True)

    while True:

        inputPlayer = screen.getch() # détecte les input du joueur

        if inputPlayer == KEY_RIGHT or inputPlayer == KEY_DOWN or inputPlayer == KEY_LEFT or inputPlayer == KEY_UP: 
            game.tour(move[inputPlayer])
            updateDisplayGame(screen, game.terrain)
        elif inputPlayer == ord("q") or inputPlayer == ord("Q"):
            curses.endwin()
            sys.exit()

        if game.mort == True:      
            break
    
        screen.refresh()

    # Si le joueur meurt
    screen.keypad(False) 
    curses.napms(1000)
    gameOver(screen, score=(game.serpent.taille-3)*100)

def updateDisplayGame(window, array2D):
    """
    Afficher / Mettre à jour l'affichage grâce au tableau de jeu
    window  -- fenetre curses
    array2D -- tableau à deux dimensions contenant "le plateau de jeu"
    
    """

    window.erase()
  
    for i in range(len(array2D)):   
        for j in range(len(array2D[0])):             
            ch = array2D[i][j]+1
            window.addstr( getCenter(curses.LINES,len(array2D[0])) + i, getCenter(curses.COLS, len(array2D))  + j*2, "  ", curses.color_pair(ch))            
         
def gameOver(window,score=0):
    """ 
    Afficher le menu game over
    window -- fenetre curses 
    score  -- score du joueur

    """
    
    beautifulClear(window, 3)
    curses.napms(500)

    showArray(window, GAME_OVER, 0,-5, True, curses.color_pair(3))
    showText(screen, f"Votre score est de {score} pt", 0, 10, True, "taper", curses.color_pair(3))
    showText(screen, f"Entre pour rejouer ou q pour arreter", 0, 13,True, "taper", curses.color_pair(3))

    window.refresh()
    screen.getch()

    # Remet les variables à 0
    game.reset()
    startGame()


if __name__ == "__main__":

    # CONSTANTES

    # VS code Terminal (les valeurs changent suivant le terminal)
    # KEY_UP = 450
    # KEY_DOWN = 456
    # KEY_LEFT = 452
    # KEY_RIGHT = 454

    # Terminal de base
    KEY_UP = curses.KEY_UP
    KEY_DOWN = curses.KEY_DOWN
    KEY_LEFT = curses.KEY_LEFT
    KEY_RIGHT = curses.KEY_RIGHT

    move = {KEY_UP : 3, KEY_DOWN:1, KEY_RIGHT:2, KEY_LEFT:4}

    # INTIALISATION VARIABLES
    game = Jeu()
    game.reset()

    screen = curses.initscr() # créer la fenêtre

    # Parametres curses
    curses.noecho() # cacher les entrées
    screen.keypad(True) # activer le clavier

    # Activer la coulour
    if curses.has_colors():
        curses.start_color()

    # Intitialiser les Couleurs 
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) # fond noir

    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN) # serpent vert
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED) # pomme rouge

    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_WHITE) # bord blanc
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_WHITE) # bord blanc
    
    # AFICHAGE MENU DEMARAGE
    startMenuGame()

    # AFFICHAGE JEU SNAKE    
    startGame()
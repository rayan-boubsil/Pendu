import os
import random
import msvcrt

alphabet = [chr(i) for i in range(ord('a'), ord('z')+1)] #Crée notre alphabet.

###
repertoire = os.path.dirname(os.path.abspath(__file__))
fichier_mots = os.path.join(repertoire, "mots.txt")
"""print("Chemin :", fichier_mots)"""
###


def difficulty(niveau : int):
    """
    Sert à paramétrer la difficulté du pendu. Plus le chiffre est haut, plus la difficulté est élevée.
    """

    niveau_difficile = []
    niveau_intermediaire = []
    niveau_facile = []


    if niveau > 0 and niveau < 4:
        ###############################################
        """
            On ouvre notre fichier mot et on place chaque mot dans une liste 'mots'.
        """
        with open(fichier_mots, "r", encoding="utf-8") as f:
            mots = [ligne.strip() for ligne in f if ligne.strip()]
        ###############################################

        for mot in mots:
            if len(mot) > 5:
                if len(mot) == len(set(mot)): #"set" permet d'indiquer "lettre unique" -> Coucou = c, o, u.
                    niveau_difficile.append(mot)
                else: 
                    niveau_intermediaire.append(mot)
            else:
                niveau_facile.append(mot)
        
        ###############################################
        if niveau == 3:
            return random.choice(niveau_difficile)
        elif niveau == 2:
            return random.choice(niveau_intermediaire)
        elif niveau == 1:
            return random.choice(niveau_facile)
        ###############################################

    else:
        print(f"Le niveau '{niveau}' est invalide ; Choisissez parmis les niveaux suivant : 1,2 ou 3.")

def clavier():

    saisie = ""

    while True:
        if msvcrt.kbhit():
            touche = msvcrt.getch().decode('utf-8')
            if touche.lower() in alphabet:
                saisie += touche.lower()
            elif touche == '\r':
                print(saisie)
                return saisie
            else:
                print("Touche incorrecte.")

clavier()
print(clavier())
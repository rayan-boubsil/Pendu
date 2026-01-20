import pygame
import sys
import random
import os

# 1. Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Hangman - Final Version")

# --- FICHIER DE MOTS ---
REPERTOIRE = os.path.dirname(os.path.abspath(__file__))
FICHIER_MOTS = os.path.join(REPERTOIRE, "mots.txt")

# --- COULEURS ---
WHITE, BLACK, GOLD = (255, 255, 255), (0, 0, 0), (255, 215, 0)
RED, GREEN, GRAY, DARK_GRAY = (200, 0, 0), (0, 180, 0), (80, 80, 80), (20, 20, 20)
BROWN = (139, 69, 19)

# --- CHARGEMENT DES RESSOURCES ---
try:
    bg_image = pygame.image.load("background.jpg")
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    bg_image = None

# Polices avec fallback sur Arial
def get_font(name, size):
    try:
        return pygame.font.Font(name, size)
    except:
        return pygame.font.SysFont("Arial", size, bold=True)

font_title = get_font("Eater-Regular.ttf", 60)
font_button = get_font("Butcherman-Regular.ttf", 30)
font_small = get_font("Frijole-Regular.ttf", 14)
font_keys = pygame.font.SysFont("Arial", 20, bold=True)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def dessiner_pendu(surface, erreurs):
    """Dessine le pendu en fonction du nombre d'erreurs (0 à 7)"""
    # Position de base pour le dessin
    base_x, base_y = 750, 350
    
    # Fond du dessin
    pygame.draw.rect(surface, (30, 30, 30), (base_x - 100, base_y - 200, 200, 280), border_radius=10)
    pygame.draw.rect(surface, GOLD, (base_x - 100, base_y - 200, 200, 280), 2, border_radius=10)
    
    if erreurs >= 1:  # Base
        pygame.draw.line(surface, BROWN, (base_x - 80, base_y + 60), (base_x + 80, base_y + 60), 8)
    
    if erreurs >= 2:  # Poteau vertical
        pygame.draw.line(surface, BROWN, (base_x - 40, base_y + 60), (base_x - 40, base_y - 160), 8)
    
    if erreurs >= 3:  # Poteau horizontal
        pygame.draw.line(surface, BROWN, (base_x - 40, base_y - 160), (base_x + 40, base_y - 160), 8)
    
    if erreurs >= 4:  # Corde
        pygame.draw.line(surface, WHITE, (base_x + 40, base_y - 160), (base_x + 40, base_y - 130), 3)
    
    if erreurs >= 5:  # Tête
        pygame.draw.circle(surface, WHITE, (base_x + 40, base_y - 110), 20, 3)
        # Yeux (X X)
        pygame.draw.line(surface, RED, (base_x + 33, base_y - 115), (base_x + 37, base_y - 111), 2)
        pygame.draw.line(surface, RED, (base_x + 37, base_y - 115), (base_x + 33, base_y - 111), 2)
        pygame.draw.line(surface, RED, (base_x + 43, base_y - 115), (base_x + 47, base_y - 111), 2)
        pygame.draw.line(surface, RED, (base_x + 47, base_y - 115), (base_x + 43, base_y - 111), 2)
    
    if erreurs >= 6:  # Corps
        pygame.draw.line(surface, WHITE, (base_x + 40, base_y - 90), (base_x + 40, base_y - 30), 3)
    
    if erreurs >= 7:  # Bras + Jambes (dernière étape = mort complète)
        # Bras gauche
        pygame.draw.line(surface, WHITE, (base_x + 40, base_y - 75), (base_x + 15, base_y - 55), 3)
        # Bras droit
        pygame.draw.line(surface, WHITE, (base_x + 40, base_y - 75), (base_x + 65, base_y - 55), 3)
        # Jambe gauche
        pygame.draw.line(surface, WHITE, (base_x + 40, base_y - 30), (base_x + 20, base_y + 10), 3)
        # Jambe droite
        pygame.draw.line(surface, WHITE, (base_x + 40, base_y - 30), (base_x + 60, base_y + 10), 3)

def ajouter_mot_au_fichier(nouveau_mot):
    mot_propre = nouveau_mot.strip().upper()
    if not mot_propre or len(mot_propre) < 3: return "TROP_COURT"
    
    try:
        with open(FICHIER_MOTS, "r", encoding="utf-8") as f:
            existants = [l.strip().upper() for l in f.readlines()]
    except:
        existants = []
        
    if mot_propre in existants: return "DOUBLON"
    
    with open(FICHIER_MOTS, "a", encoding="utf-8") as f:
        f.write(mot_propre + "\n")
    return "SUCCES"

def menu_saisie_mot():
    input_text, msg, running = "", "", True
    input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 270, 400, 60)
    
    while running:
        screen.fill(DARK_GRAY)
        if bg_image:
            temp_bg = bg_image.copy()
            temp_bg.fill((40, 40, 40), special_flags=pygame.BLEND_RGB_MULT)
            screen.blit(temp_bg, (0, 0))
        
        draw_text("AJOUTER UN NOUVEAU MOT", font_button, WHITE, screen, SCREEN_WIDTH // 2, 150)
        pygame.draw.rect(screen, WHITE, input_rect, 3, border_radius=10)
        draw_text(input_text, font_button, RED, screen, SCREEN_WIDTH // 2, 300)

        # Feedbacks
        if msg == "SUCCES": draw_text("MOT ENREGISTRÉ !", font_small, GREEN, screen, SCREEN_WIDTH // 2, 380)
        elif msg == "DOUBLON": draw_text("DÉJÀ DANS LA LISTE !", font_small, GOLD, screen, SCREEN_WIDTH // 2, 380)
        elif msg == "TROP_COURT": draw_text("MOT TROP COURT (MIN 3) !", font_small, GRAY, screen, SCREEN_WIDTH // 2, 380)

        draw_text("ENTREE : VALIDER | ECHAP : RETOUR", font_small, WHITE, screen, SCREEN_WIDTH // 2, 520)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False
                elif event.key == pygame.K_RETURN:
                    msg = ajouter_mot_au_fichier(input_text)
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE: 
                    input_text = input_text[:-1]
                    msg = ""
                else:
                    if len(input_text) < 15 and event.unicode.isalpha():
                        input_text += event.unicode.upper()
                        msg = ""
        pygame.display.update()

def menu_difficulty():
    while True:
        if bg_image: screen.blit(bg_image, (0, 0))
        else: screen.fill((50, 50, 50))
        m_pos = pygame.mouse.get_pos()
        draw_text("LE PENDU", font_title, WHITE, screen, SCREEN_WIDTH // 2, 80)
        b_1 = pygame.Rect(SCREEN_WIDTH // 2 - 125, 250, 250, 60)
        b_2 = pygame.Rect(SCREEN_WIDTH // 2 - 125, 320, 250, 60)
        b_3 = pygame.Rect(SCREEN_WIDTH // 2 - 125, 390, 250, 60)
        for b, txt in [(b_1, "NIVEAU 1"), (b_2, "NIVEAU 2"),(b_3, "NIVEAU 3")]:
            c = RED if b.collidepoint(m_pos) else BLACK
            pygame.draw.rect(screen, c, b, border_radius=12)
            draw_text(txt, font_button, WHITE, screen, b.centerx, b.centery)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: 
                pygame.quit(); sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if b_1.collidepoint(m_pos): 
                    start_game(1)
                elif b_2.collidepoint(m_pos): 
                    start_game(2)
                elif b_3.collidepoint(m_pos): 
                    start_game(3)

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                main_menu()
        pygame.display.update()

def start_game(difficulty : int):
    continuer_jeu = True

    niveau_difficile = []
    niveau_intermediaire = []
    niveau_facile = []

    while continuer_jeu:
        # Recharger la liste à chaque manche pour inclure les nouveaux mots ajoutés

        with open(FICHIER_MOTS, "r", encoding="utf-8") as f:
            mots = [l.strip().upper() for l in f.readlines() if l.strip()]

        ###############################################
        if mots:
            for mot in mots:
                if len(mot) > 5:
                    if len(mot) == len(set(mot)): #"set" permet d'indiquer "lettre unique" -> Coucou = c, o, u.
                        niveau_difficile.append(mot)
                    else: 
                        niveau_intermediaire.append(mot)
                else:
                    niveau_facile.append(mot)
        else:
            mot_mystere = "INDICE"
        ###############################################
        if difficulty == 3:
            mot_mystere = random.choice(niveau_difficile)
        elif difficulty == 2:
            mot_mystere = random.choice(niveau_intermediaire)
        elif difficulty == 1:
            mot_mystere = random.choice(niveau_facile)
        ###############################################

        indice = random.choice(mot_mystere)
        lettres_trouvees = [l for l in mot_mystere if l == indice]
        vies, manche_en_cours = 7, True
        erreurs = 0  # Compteur d'erreurs pour le dessin du pendu

        # Clavier dynamique
        lettres_clavier = []
        taille, marge = 35, 8
        debut_x = (SCREEN_WIDTH - (13 * (taille + marge))) // 2
        for i, lettre in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            x = debut_x + (i % 13) * (taille + marge)
            y = 440 + (i // 13) * (taille + marge)
            statut = "indice" if lettre == indice else "libre"
            lettres_clavier.append({"lettre": lettre, "rect": pygame.Rect(x, y, taille, taille), "statut": statut, "clique": (lettre == indice)})

        while manche_en_cours:
            screen.fill(DARK_GRAY)
            if bg_image:
                temp_bg = bg_image.copy()
                temp_bg.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_MULT)
                screen.blit(temp_bg, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            draw_text(f"Chances : {vies} / 7", font_small, (RED if vies <= 2 else GREEN), screen, 100, 50)
            
            # Dessiner le pendu en temps réel
            dessiner_pendu(screen, erreurs)
            
            # Mot caché
            word_box = pygame.Rect(SCREEN_WIDTH // 2 - 280, 180, 560, 100)
            pygame.draw.rect(screen, (10, 10, 10), word_box, border_radius=15)
            pygame.draw.rect(screen, GOLD, word_box, 2, border_radius=15)
            affichage = "".join([l + " " if l in lettres_trouvees else "_ " for l in mot_mystere])
            draw_text(affichage, font_button, GOLD, screen, SCREEN_WIDTH // 2, 230)

            # Dessin Clavier
            for t in lettres_clavier:
                rect_c, text_c = WHITE, BLACK
                if t["statut"] == "indice": rect_c, text_c = GRAY, WHITE
                elif t["statut"] == "correct": rect_c, text_c = GREEN, WHITE
                elif t["statut"] == "incorrect": rect_c, text_c = RED, WHITE
                elif t["rect"].collidepoint(mouse_pos): rect_c = GOLD
                pygame.draw.rect(screen, rect_c, t["rect"], border_radius=5)
                draw_text(t["lettre"], font_keys, text_c, screen, t["rect"].centerx, t["rect"].centery)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for t in lettres_clavier:
                        if t["rect"].collidepoint(mouse_pos) and not t["clique"]:
                            t["clique"] = True
                            if t["lettre"] in mot_mystere:
                                lettres_trouvees.append(t["lettre"])
                                t["statut"] = "correct"
                            else:
                                vies -= 1
                                erreurs += 1  # Incrémenter le compteur d'erreurs
                                t["statut"] = "incorrect"
                ###
                if event.type == pygame.KEYDOWN:
                    lettre = event.unicode.upper() #On récupère l'entré de notre clavier.
                    if lettre.isalpha() and len(lettre) == 1: #On vérifie si 'lettre' est une lettre de l'alphabet et que l'entrée n'est pas plusieurs caractères.
                        for t in lettres_clavier:
                            if t["lettre"] == lettre and not t["clique"]:
                                t["clique"] = True
                                if lettre in mot_mystere:
                                    lettres_trouvees.append(lettre)
                                    t["statut"] = "correct"
                                else:
                                    vies -= 1
                                    erreurs += 1  # Incrémenter le compteur d'erreurs
                                    t["statut"] = "incorrect"
                                break
                ###

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        manche_en_cours = continuer_jeu = False

            # Victoire
            if all(l in lettres_trouvees for l in mot_mystere):
                draw_text("VICTOIRE !", font_title, GOLD, screen, SCREEN_WIDTH // 2, 350)
                pygame.display.update()
                pygame.time.delay(1200)
                manche_en_cours = False

            # Défaite
            elif vies <= 0:
                perdu = True
                while perdu:
                    screen.fill(BLACK)
                    draw_text("PERDU !", font_title, RED, screen, SCREEN_WIDTH // 2, 200)
                    draw_text(f"C'ÉTAIT : {mot_mystere}", font_button, WHITE, screen, SCREEN_WIDTH // 2, 300)
                    m_p = pygame.mouse.get_pos()
                    b_rej = pygame.Rect(SCREEN_WIDTH//2 - 220, 450, 200, 60)
                    b_men = pygame.Rect(SCREEN_WIDTH//2 + 20, 450, 230, 60)
                    for b, t_b in [(b_rej, "REJOUER"), (b_men, "MENU")]:
                        c = RED if b.collidepoint(m_p) else GRAY
                        pygame.draw.rect(screen, c, b, border_radius=10)
                        draw_text(t_b, font_button, WHITE, screen, b.centerx, b.centery)
                    for e in pygame.event.get():
                        if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                            if b_rej.collidepoint(m_p): perdu = manche_en_cours = False
                            if b_men.collidepoint(m_p): 
                                perdu = manche_en_cours
                                continuer_jeu = False
                                main_menu()
                    pygame.display.update()
            pygame.display.update()

def main_menu():
    while True:
        if bg_image: screen.blit(bg_image, (0, 0))
        else: screen.fill((50, 50, 50))
        m_pos = pygame.mouse.get_pos()
        draw_text("LE PENDU", font_title, WHITE, screen, SCREEN_WIDTH // 2, 80)
        b_play = pygame.Rect(SCREEN_WIDTH // 2 - 125, 250, 250, 60)
        b_add = pygame.Rect(SCREEN_WIDTH // 2 - 125, 320, 250, 60)
        b_exit = pygame.Rect(SCREEN_WIDTH // 2 - 125, 390, 250, 60)
        for b, txt in [(b_play, "JOUER"), (b_add, "AJOUTER MOT"),(b_exit, "QUITTER")]:
            c = RED if b.collidepoint(m_pos) else BLACK
            pygame.draw.rect(screen, c, b, border_radius=12)
            draw_text(txt, font_button, WHITE, screen, b.centerx, b.centery)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if b_play.collidepoint(m_pos): menu_difficulty()
                elif b_add.collidepoint(m_pos): menu_saisie_mot()
                elif b_exit.collidepoint(m_pos): pygame.quit(); sys.exit()
        pygame.display.update()

if __name__ == "__main__":
    main_menu()
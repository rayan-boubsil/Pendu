import pygame
import sys
import random

# 1. Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Le Pendu - Version Ultime")

# --- COULEURS ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (60, 60, 60)
LIGHT_GRAY = (180, 180, 180)
DARK_GRAY = (20, 20, 20)

# --- CHARGEMENT DES RESSOURCES ---
try:
    bg_image = pygame.image.load("background.jpg")
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    bg_image = None

# Polices avec sécurité (SysFont si fichier absent)
try:
    font_title = pygame.font.Font("Eater-Regular.ttf", 80)
    font_button = pygame.font.Font("Butcherman-Regular.ttf", 40)
    font_small = pygame.font.Font("Frijole-Regular.ttf", 18)
    font_keys = pygame.font.SysFont("Arial", 25, bold=True)
except:
    font_title = pygame.font.SysFont("Arial", 80, bold=True)
    font_button = pygame.font.SysFont("Arial", 40, bold=True)
    font_small = pygame.font.SysFont("Arial", 18)
    font_keys = pygame.font.SysFont("Arial", 25, bold=True)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


# --- LOGIQUE DE FICHIER ---


def ajouter_mot_au_fichier(nouveau_mot):
    """Nettoie le mot et vérifie les doublons avant l'écriture"""
    mot_propre = nouveau_mot.strip().upper()
    if not mot_propre:
        return "VIDE"

    try:
        with open("mots.txt", "r", encoding="utf-8") as f:
            existants = [l.strip().upper() for l in f.readlines()]
    except FileNotFoundError:
        existants = []

    if mot_propre in existants:
        return "DOUBLON"

    with open("mots.txt", "a", encoding="utf-8") as f:
        f.write(mot_propre + "\n")
    return "SUCCES"


# --- ÉCRAN AJOUTER MOT (DESIGN COMPLET) ---


def menu_saisie_mot():
    input_text = ""
    msg = ""
    running = True
    input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 270, 400, 60)

    while running:
        screen.fill(DARK_GRAY)
        if bg_image:
            temp_bg = bg_image.copy()
            temp_bg.fill((40, 40, 40), special_flags=pygame.BLEND_RGB_MULT)
            screen.blit(temp_bg, (0, 0))

        draw_text(
            "AJOUTER UN NOUVEAU MOT", font_button, WHITE, screen, SCREEN_WIDTH // 2, 150
        )

        # Champ de saisie
        pygame.draw.rect(screen, WHITE, input_rect, 3, border_radius=10)
        draw_text(input_text, font_button, RED, screen, SCREEN_WIDTH // 2, 300)

        # Retours utilisateurs
        if msg == "DOUBLON":
            draw_text(
                "CE MOT EXISTE DEJA !", font_small, GOLD, screen, SCREEN_WIDTH // 2, 380
            )
        elif msg == "SUCCES":
            draw_text(
                "MOT AJOUTE AVEC SUCCES !",
                font_small,
                GREEN,
                screen,
                SCREEN_WIDTH // 2,
                380,
            )
        elif msg == "VIDE":
            draw_text(
                "VEUILLEZ TAPER UN MOT",
                font_small,
                GRAY,
                screen,
                SCREEN_WIDTH // 2,
                380,
            )

        draw_text(
            "ENTREE : VALIDER | ECHAP : RETOUR",
            font_small,
            WHITE,
            screen,
            SCREEN_WIDTH // 2,
            520,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    msg = ajouter_mot_au_fichier(input_text)
                    if msg == "SUCCES":
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    msg = ""
                else:
                    if len(input_text) < 12 and event.unicode.isalpha():
                        input_text += event.unicode.upper()
                        msg = ""
        pygame.display.update()


# --- ÉCRAN DE JEU (DESIGN COMPLET + INDICE) ---


def start_game():
    try:
        with open("mots.txt", "r", encoding="utf-8") as f:
            mots = [l.strip().upper() for l in f.readlines() if l.strip()]
        mot_mystere = random.choice(mots) if mots else "PENDU"
    except:
        mot_mystere = "PENDU"

    # Logique de l'indice : on dévoile une lettre d'office
    indice = random.choice(mot_mystere)
    lettres_trouvees = [indice]

    vies = 7
    in_game = True

    # Initialisation du clavier
    lettres_clavier = []
    taille, marge = 45, 10
    debut_x = (SCREEN_WIDTH - (13 * (taille + marge))) // 2
    for i, lettre in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        x = debut_x + (i % 13) * (taille + marge)
        y = 440 + (i // 13) * (taille + marge)
        # La lettre indice est déjà marquée comme cliquée
        est_cliquee = lettre == indice
        lettres_clavier.append(
            {
                "lettre": lettre,
                "rect": pygame.Rect(x, y, taille, taille),
                "clique": est_cliquee,
            }
        )

    while in_game:
        screen.fill(DARK_GRAY)
        if bg_image:
            temp_bg = bg_image.copy()
            temp_bg.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_MULT)
            screen.blit(temp_bg, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        # Bloc du mot secret (Design Box)
        word_box = pygame.Rect(SCREEN_WIDTH // 2 - 250, 180, 500, 100)
        pygame.draw.rect(screen, (10, 10, 10), word_box, border_radius=15)
        pygame.draw.rect(screen, GOLD, word_box, 2, border_radius=15)

        affichage = "".join(
            [l + " " if l in lettres_trouvees else "_ " for l in mot_mystere]
        )
        draw_text(affichage, font_button, GOLD, screen, SCREEN_WIDTH // 2, 230)

        # UI : Vies et Indice
        vies_color = RED if vies <= 3 else GREEN
        draw_text(f"VIES : {vies} / 7", font_small, vies_color, screen, 150, 50)
        draw_text("INDICE OFFERT !", font_small, GOLD, screen, SCREEN_WIDTH - 150, 50)
        draw_text(
            "ECHAP POUR QUITTER LA PARTIE",
            font_small,
            GOLD,
            screen,
            SCREEN_HEIGHT - 195,
            575,
        )

        # Clavier visuel
        for t in lettres_clavier:
            if t["clique"]:
                color, t_color = DARK_GRAY, GRAY
            else:
                # Survol souris
                color = RED if t["rect"].collidepoint(mouse_pos) else WHITE
                t_color = BLACK

            pygame.draw.rect(screen, color, t["rect"], border_radius=5)
            draw_text(
                t["lettre"],
                font_keys,
                t_color,
                screen,
                t["rect"].centerx,
                t["rect"].centery,
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for t in lettres_clavier:
                    if t["rect"].collidepoint(mouse_pos) and not t["clique"]:
                        t["clique"] = True
                        if t["lettre"] in mot_mystere:
                            lettres_trouvees.append(t["lettre"])
                        else:
                            vies -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_game = False

        # Fin de partie
        if all(l in lettres_trouvees for l in mot_mystere):
            screen.fill(BLACK)
            draw_text("VICTOIRE !", font_title, GOLD, screen, SCREEN_WIDTH // 2, 300)
            pygame.display.update()
            pygame.time.delay(2000)
            in_game = False
        elif vies <= 0:
            screen.fill(BLACK)
            draw_text("PERDU !", font_title, RED, screen, SCREEN_WIDTH // 2, 250)
            draw_text(
                f"C'ÉTAIT : {mot_mystere}",
                font_button,
                WHITE,
                screen,
                SCREEN_WIDTH // 2,
                400,
            )
            pygame.display.update()
            pygame.time.delay(3000)
            in_game = False

        pygame.display.update()


# --- MENU PRINCIPAL ---


def main_menu():
    while True:
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill((50, 50, 50))

        mouse_pos = pygame.mouse.get_pos()
        draw_text("LE PENDU", font_title, WHITE, screen, SCREEN_WIDTH // 2, 80)

        btn_play = pygame.Rect(SCREEN_WIDTH // 2 - 175, 250, 350, 60)
        btn_add = pygame.Rect(SCREEN_WIDTH // 2 - 175, 330, 350, 60)
        btn_exit = pygame.Rect(SCREEN_WIDTH // 2 - 175, 410, 350, 60)

        for btn, txt in [
            (btn_play, "JOUER"),
            (btn_add, "AJOUTER MOT"),
            (btn_exit, "QUITTER"),
        ]:
            btn_color = RED if btn.collidepoint(mouse_pos) else BLACK
            pygame.draw.rect(screen, btn_color, btn, border_radius=12)
            draw_text(txt, font_button, WHITE, screen, btn.centerx, btn.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_play.collidepoint(mouse_pos):
                    start_game()
                elif btn_add.collidepoint(mouse_pos):
                    menu_saisie_mot()
                elif btn_exit.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


if __name__ == "__main__":
    main_menu()

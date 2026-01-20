import pygame
import sys
import random

# 1. Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Hangman")

try:
    logo = pygame.image.load("logo.jpg")
    pygame.display.set_icon(logo)
except:
    pass

# --- COULEURS ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (200, 0, 0)
GREEN = (0, 180, 0)
GRAY = (80, 80, 80)
DARK_GRAY = (20, 20, 20)

# --- CHARGEMENT DES RESSOURCES ---
try:
    bg_image = pygame.image.load("background.jpg")
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    bg_image = None

try:
    font_title = pygame.font.Font("Eater-Regular.ttf", 60)
    font_button = pygame.font.Font("Butcherman-Regular.ttf", 30)
    font_small = pygame.font.Font("Frijole-Regular.ttf", 14)
    font_keys = pygame.font.SysFont("Arial", 20, bold=True)
except:
    font_title = pygame.font.SysFont("Arial", 60, bold=True)
    font_button = pygame.font.SysFont("Arial", 30, bold=True)
    font_small = pygame.font.SysFont("Arial", 14)
    font_keys = pygame.font.SysFont("Arial", 20, bold=True)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


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
        pygame.draw.rect(screen, WHITE, input_rect, 3, border_radius=10)
        draw_text(input_text, font_button, RED, screen, SCREEN_WIDTH // 2, 300)

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
                    # Logique simplifiée ici pour la démo
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 12 and event.unicode.isalpha():
                        input_text += event.unicode.upper()
        pygame.display.update()


def start_game():
    continuer_jeu = True

    while continuer_jeu:
        # --- INITIALISATION DE LA MANCHE ---
        try:
            with open("mots.txt", "r", encoding="utf-8") as f:
                mots = [l.strip().upper() for l in f.readlines() if l.strip()]
            mot_mystere = random.choice(mots) if mots else "PENDU"
        except:
            mot_mystere = "PENDU"

        indice = random.choice(mot_mystere)
        lettres_trouvees = [l for l in mot_mystere if l == indice]
        vies = 7
        manche_en_cours = True

        lettres_clavier = []
        taille, marge = 35, 8
        debut_x = (SCREEN_WIDTH - (13 * (taille + marge))) // 2
        for i, lettre in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            x = debut_x + (i % 13) * (taille + marge)
            y = 440 + (i // 13) * (taille + marge)
            statut = "indice" if lettre == indice else "libre"
            lettres_clavier.append(
                {
                    "lettre": lettre,
                    "rect": pygame.Rect(x, y, taille, taille),
                    "statut": statut,
                    "clique": (lettre == indice),
                }
            )

        # --- BOUCLE DE LA MANCHE ---
        while manche_en_cours:
            screen.fill(DARK_GRAY)
            if bg_image:
                temp_bg = bg_image.copy()
                temp_bg.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_MULT)
                screen.blit(temp_bg, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            vies_color = RED if vies <= 3 else GREEN
            draw_text(f"Vies : {vies} / 7", font_small, vies_color, screen, 100, 50)

            # Mot secret
            word_box = pygame.Rect(SCREEN_WIDTH // 2 - 250, 180, 500, 100)
            pygame.draw.rect(screen, (10, 10, 10), word_box, border_radius=15)
            pygame.draw.rect(screen, GOLD, word_box, 2, border_radius=15)
            affichage = "".join(
                [l + " " if l in lettres_trouvees else "_ " for l in mot_mystere]
            )
            draw_text(affichage, font_button, GOLD, screen, SCREEN_WIDTH // 2, 230)

            # Clavier
            for t in lettres_clavier:
                rect_color = WHITE
                text_color = BLACK
                if t["statut"] == "indice":
                    rect_color, text_color = GRAY, WHITE
                elif t["statut"] == "correct":
                    rect_color, text_color = GREEN, WHITE
                elif t["statut"] == "incorrect":
                    rect_color, text_color = RED, WHITE
                elif t["rect"].collidepoint(mouse_pos):
                    rect_color = GOLD

                pygame.draw.rect(screen, rect_color, t["rect"], border_radius=5)
                draw_text(
                    t["lettre"],
                    font_keys,
                    text_color,
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
                                if t["lettre"] not in lettres_trouvees:
                                    lettres_trouvees.append(t["lettre"])
                                t["statut"] = "correct"
                            else:
                                vies -= 1
                                t["statut"] = "incorrect"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        manche_en_cours = False
                        continuer_jeu = False

            # GESTION DE LA VICTOIRE
            if all(l in lettres_trouvees for l in mot_mystere):
                draw_text(
                    "VICTOIRE !", font_title, GOLD, screen, SCREEN_WIDTH // 2, 350
                )
                pygame.display.update()
                pygame.time.delay(1200)
                manche_en_cours = False

            # GESTION DE LA DÉFAITE (Menu Rejouer/Quitter)
            elif vies <= 0:
                perdu = True
                while perdu:
                    screen.fill(BLACK)
                    draw_text(
                        "PERDU !", font_title, RED, screen, SCREEN_WIDTH // 2, 200
                    )
                    draw_text(
                        f"LE MOT ETAIT : {mot_mystere}",
                        font_button,
                        WHITE,
                        screen,
                        SCREEN_WIDTH // 2,
                        300,
                    )

                    mouse_perdu = pygame.mouse.get_pos()
                    btn_rejouer = pygame.Rect(SCREEN_WIDTH // 2 - 220, 450, 200, 60)
                    btn_menu = pygame.Rect(SCREEN_WIDTH // 2 + 20, 450, 230, 60)

                    for btn, txt in [
                        (btn_rejouer, "REJOUER"),
                        (btn_menu, "MENU PRINCIPAL"),
                    ]:
                        color = RED if btn.collidepoint(mouse_perdu) else GRAY
                        pygame.draw.rect(screen, color, btn, border_radius=10)
                        draw_text(
                            txt, font_button, WHITE, screen, btn.centerx, btn.centery
                        )

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if btn_rejouer.collidepoint(mouse_perdu):
                                perdu = False
                                manche_en_cours = False
                                # On reste dans la boucle continuer_jeu
                            if btn_menu.collidepoint(mouse_perdu):
                                perdu = False
                                manche_en_cours = False
                                continuer_jeu = False  # Retour au menu principal

                    pygame.display.update()

            pygame.display.update()


def main_menu():
    while True:
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill((50, 50, 50))
        mouse_pos = pygame.mouse.get_pos()
        draw_text("LE PENDU", font_title, WHITE, screen, SCREEN_WIDTH // 2, 80)
        btn_play = pygame.Rect(SCREEN_WIDTH // 2 - 125, 250, 250, 60)
        btn_add = pygame.Rect(SCREEN_WIDTH // 2 - 125, 320, 250, 60)
        btn_exit = pygame.Rect(SCREEN_WIDTH // 2 - 125, 390, 250, 60)
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

import pygame
import os
import sys
from interface import (
    SCREEN_WIDTH,
    DARK_GRAY,
    screen,
    bg_image,
    draw_text,
    font_button,
    WHITE,
    RED,
    font_small,
    GREEN,
    GOLD,
    GRAY,
)

# --- FICHIER DE MOTS ---
FICHIER_MOTS = "mots.txt"


def initialiser_fichier():
    """Crée le fichier avec quelques mots par défaut s'il n'existe pas."""
    if not os.path.exists(FICHIER_MOTS):
        with open(FICHIER_MOTS, "w", encoding="utf-8") as f:
            f.write("PYTHON\nPENDU\nPYGAME\nORDINATEUR\n")


initialiser_fichier()


def ajouter_mot_au_fichier(nouveau_mot):
    mot_propre = nouveau_mot.strip().upper()
    if not mot_propre or len(mot_propre) < 3:
        return "TROP_COURT"

    try:
        with open(FICHIER_MOTS, "r", encoding="utf-8") as f:
            existants = [l.strip().upper() for l in f.readlines()]
    except:
        existants = []

    if mot_propre in existants:
        return "DOUBLON"

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

        draw_text(
            "AJOUTER UN NOUVEAU MOT", font_button, WHITE, screen, SCREEN_WIDTH // 2, 150
        )
        pygame.draw.rect(screen, WHITE, input_rect, 3, border_radius=10)
        draw_text(input_text, font_button, RED, screen, SCREEN_WIDTH // 2, 300)

        # Feedbacks
        if msg == "SUCCES":
            draw_text(
                "MOT ENREGISTRÉ !", font_small, GREEN, screen, SCREEN_WIDTH // 2, 380
            )
        elif msg == "DOUBLON":
            draw_text(
                "DÉJÀ DANS LA LISTE !", font_small, GOLD, screen, SCREEN_WIDTH // 2, 380
            )
        elif msg == "TROP_COURT":
            draw_text(
                "MOT TROP COURT (MIN 3) !",
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
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    msg = ""
                else:
                    if len(input_text) < 15 and event.unicode.isalpha():
                        input_text += event.unicode.upper()
                        msg = ""
        pygame.display.update()

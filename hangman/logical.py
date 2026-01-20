import random
import pygame
import sys
from word import FICHIER_MOTS 
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
    BLACK,
    font_keys,
    font_title,
)

def start_game():
    continuer_jeu = True
    while continuer_jeu:
        # Recharger la liste à chaque manche pour inclure les nouveaux mots ajoutés
        try:
            with open(FICHIER_MOTS, "r", encoding="utf-8") as f:
                mots = [l.strip().upper() for l in f.readlines() if l.strip()]
            mot_mystere = random.choice(mots) if mots else "PENDU"
        except:
            mot_mystere = "PENDU"

        indice = random.choice(mot_mystere)
        lettres_trouvees = [l for l in mot_mystere if l == indice]
        vies, manche_en_cours = 7, True

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
                                t["statut"] = "incorrect"
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
                            if b_men.collidepoint(m_p): perdu = manche_en_cours = continuer_jeu = False
                    pygame.display.update()
            pygame.display.update()
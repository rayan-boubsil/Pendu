import pygame
import sys
from logical import start_game
from word import menu_saisie_mot
from interface import (
    SCREEN_WIDTH,
    screen,
    bg_image,
    draw_text,
    font_button,
    WHITE,
    RED,
    BLACK,
    font_title,
)

def main_menu():
    while True:
        if bg_image: screen.blit(bg_image, (0, 0))
        else: screen.fill((50, 50, 50))
        m_pos = pygame.mouse.get_pos()
        draw_text("LE PENDU", font_title, WHITE, screen, SCREEN_WIDTH // 2, 80)
        b_play = pygame.Rect(SCREEN_WIDTH // 2 - 125, 250, 250, 60)
        b_add = pygame.Rect(SCREEN_WIDTH // 2 - 125, 320, 250, 60)
        b_exit = pygame.Rect(SCREEN_WIDTH // 2 - 125, 390, 250, 60)
        for b, txt in [(b_play, "JOUER"), (b_add, "AJOUTER MOT"), (b_exit, "QUITTER")]:
            c = RED if b.collidepoint(m_pos) else BLACK
            pygame.draw.rect(screen, c, b, border_radius=12)
            draw_text(txt, font_button, WHITE, screen, b.centerx, b.centery)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if b_play.collidepoint(m_pos): start_game()
                elif b_add.collidepoint(m_pos): menu_saisie_mot()
                elif b_exit.collidepoint(m_pos): pygame.quit(); sys.exit()
        pygame.display.update()

if __name__ == "__main__":
    main_menu()
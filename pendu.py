import pygame
import sys

# 1. Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Le Pendu")

# --- CHARGEMENT DES RESSOURCES ---
try:
    bg_image = pygame.image.load("background.jpg")
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    bg_image = None
    print("Image 'background.jpg' non trouvée, utilisation d'un fond gris.")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)



# Polices
# Note : Assure-toi que les fichiers .ttf sont dans le même dossier
try:
    font_title = pygame.font.Font("Eater-Regular.ttf", 80)
    font_button = pygame.font.Font("Butcherman-Regular.ttf", 40)
    font_small = pygame.font.Font("Frijole-Regular.ttf", 20)
except:
    font_title = pygame.font.Font("Eater-Regular.ttf", 80)
    font_button = pygame.font.Font("Butcherman-Regular.ttf", 40)
    font_small = pygame.font.Font("Frijole-Regular.ttf", 20)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def ajouter_mot_au_fichier(nouveau_mot):
    """Enregistre le mot dans mots.txt"""
    mot = nouveau_mot.strip().upper()
    if mot:
        with open("mots.txt", "a", encoding="utf-8") as f:
            f.write(mot + "\n")


def menu_saisie_mot():
    """Écran pour taper un nouveau mot"""
    input_text = ""
    running = True
    while running:
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill((30, 30, 30))

        draw_text("NOUVEAU MOT :", font_button, WHITE, screen, SCREEN_WIDTH // 2, 150)
        # Affichage de la saisie en cours
        draw_text(input_text, font_button, RED, screen, SCREEN_WIDTH // 2, 395)
        draw_text(
            "Entrée pour valider - Echap pour annuler",
            font_small,
            WHITE,
            screen,
            SCREEN_WIDTH // 2,
            500,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    ajouter_mot_au_fichier(input_text)
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    # On limite à 15 lettres et on n'autorise que l'alphabet
                    if len(input_text) < 15 and event.unicode.isalpha():
                        input_text += event.unicode.upper()

        pygame.display.update()


def main_menu():
    while True:
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill((50, 50, 50))

        mouse_pos = pygame.mouse.get_pos()
        draw_text("LE PENDU", font_title, WHITE, screen, SCREEN_WIDTH // 2, 80)

        # Création des 3 boutons
        button_play = pygame.Rect(SCREEN_WIDTH // 2 - 175, 250, 350, 60)
        button_add = pygame.Rect(SCREEN_WIDTH // 2 - 175, 330, 350, 60)
        button_exit = pygame.Rect(SCREEN_WIDTH // 2 - 175, 410, 350, 60)

        # Logique de survol et dessin
        for btn, txt in [
            (button_play, "JOUER"),
            (button_add, "AJOUTER UN MOT"),
            (button_exit, "QUITTER"),
        ]:
            color = RED if btn.collidepoint(mouse_pos) else BLACK
            pygame.draw.rect(screen, color, btn, border_radius=12)
            draw_text(txt, font_button, WHITE, screen, btn.centerx, btn.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_play.collidepoint(mouse_pos):
                        start_game()
                    if button_add.collidepoint(mouse_pos):
                        menu_saisie_mot()
                    if button_exit.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()


def start_game():
    in_game = True
    while in_game:
        screen.fill(BLACK)
        draw_text(
            "LE JEU EST EN COURS",
            font_button,
            WHITE,
            screen,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
        )
        draw_text(
            "Appuyez sur ECHAP pour quitter",
            font_small,
            WHITE,
            screen,
            SCREEN_WIDTH // 2,
            550,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_game = False

        pygame.display.update()


if __name__ == "__main__":
    main_menu()

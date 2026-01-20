import pygame
# 1. Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Hangman - Final Version")

# --- COULEURS ---
WHITE, BLACK, GOLD = (255, 255, 255), (0, 0, 0), (255, 215, 0)
RED, GREEN, GRAY, DARK_GRAY = (200, 0, 0), (0, 180, 0), (80, 80, 80), (20, 20, 20)

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

# Permet l'affichage des texte 

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)
    
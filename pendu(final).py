import math
import pygame
import sys
import random
import os

# 1. Initialisation de Pygame
pygame.init()

# --- INITIALISATION AUDIO ---
pygame.mixer.init()

# Paramètres de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Le Pendu")

# Chargement et application de l'icône
icon = pygame.image.load("logo.jpg")
pygame.display.set_icon(icon)

# --- FICHIERS ---
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
WORDS_FILE = os.path.join(DIRECTORY, "mots.txt")
SCORES_FILE = os.path.join(DIRECTORY, "scores.txt")

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

# Filtre sombre pour la lisibilité
overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
overlay.set_alpha(190)
overlay.fill((25, 25, 25))


def load_audio_resources():
    sounds = {}
    try:
        if os.path.exists("mainsong.mp3"):
            pygame.mixer.music.load("mainsong.mp3")
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)

        if os.path.exists("correct.wav"):
            sounds["win"] = pygame.mixer.Sound("correct.wav")
        if os.path.exists("wrong.wav"):
            sounds["lose"] = pygame.mixer.Sound("wrong.wav")
    except:
        print("Audio indisponible")
    return sounds


sounds = load_audio_resources()


def apply_dark_filter():
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(DARK_GRAY)
    screen.blit(overlay, (0, 0))


def get_font(name, size):
    try:
        return pygame.font.Font(name, size)
    except:
        return pygame.font.SysFont("Arial", size, bold=True)


font_title = get_font("Eater-Regular.ttf", 60)
font_button = get_font("Butcherman-Regular.ttf", 30)
font_small = get_font("Frijole-Regular.ttf", 14)
font_keys = pygame.font.SysFont("Arial", 20, bold=True)


# --- LOGIQUE DES SCORES ---
def load_all_scores():
    scores_dict = {}
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    try:
                        name, pts = line.strip().split(":")
                        scores_dict[name] = max(scores_dict.get(name, 0), int(pts))
                    except:
                        continue
    return scores_dict


def load_best_scores():
    scores = load_all_scores()
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]


def save_score(name, score):
    with open(SCORES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{name}:{score}\n")


# --- INTERFACES ---

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(str(text), True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def draw_hangman(surface, errors):
    base_x, base_y = SCREEN_WIDTH // 2, 280
    pygame.draw.rect(
        surface, (10, 10, 10), (base_x - 115, base_y - 240, 230, 320), border_radius=10
    )
    pygame.draw.rect(
        surface, GOLD, (base_x - 115, base_y - 240, 230, 320), 2, border_radius=10
    )
    if errors >= 1:
        pygame.draw.line(surface, BROWN, (base_x - 90, base_y + 60), (base_x + 90, base_y + 60), 8)
    if errors >= 2:
        pygame.draw.line(surface, BROWN, (base_x - 45, base_y + 60), (base_x - 45, base_y - 180), 8)
    if errors >= 3:
        pygame.draw.line(surface, BROWN, (base_x - 45, base_y - 180), (base_x + 45, base_y - 180), 8)
    if errors >= 4:
        pygame.draw.line(surface, WHITE, (base_x + 45, base_y - 180), (base_x + 45, base_y - 145), 3)
    if errors >= 5:
        pygame.draw.circle(surface, WHITE, (base_x + 45, base_y - 125), 20, 3)
    if errors >= 6:
        pygame.draw.line(surface, WHITE, (base_x + 45, base_y - 105), (base_x + 45, base_y - 40), 3)
    if errors >= 7:
        pygame.draw.line(surface, WHITE, (base_x + 45, base_y - 90), (base_x + 20, base_y - 70), 3)
        pygame.draw.line(surface, WHITE, (base_x + 45, base_y - 90), (base_x + 70, base_y - 70), 3)
        pygame.draw.line(surface, WHITE, (base_x + 45, base_y - 40), (base_x + 25, base_y + 10), 3)
        pygame.draw.line(surface, WHITE, (base_x + 45, base_y - 40), (base_x + 65, base_y + 10), 3)


def leaderboard_menu():
    running = True
    while running:
        apply_dark_filter()
        scores = load_best_scores()
        draw_text("TOP 5 MEILLEURS SCORES", font_button, GOLD, screen, SCREEN_WIDTH // 2, 100)
        for i, (name, pts) in enumerate(scores):
            draw_text(
                f"{i+1}. {name} : {pts} PTS",
                font_button,
                WHITE,
                screen,
                SCREEN_WIDTH // 2,
                200 + i * 60,
            )
        draw_text(
            "ECHAP POUR RETOURNER AU MENU",
            font_small,
            GRAY,
            screen,
            SCREEN_WIDTH // 2,
            600,
        )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        pygame.display.update()


def name_input_menu():
    name, running = "", True
    existing_scores = load_all_scores()
    loaded_score = 0

    while running:
        apply_dark_filter()
        draw_text("IDENTIFICATION", font_title, WHITE, screen, SCREEN_WIDTH // 2, 120)
        draw_text("ENTRE TON NOM :", font_button, GOLD, screen, SCREEN_WIDTH // 2, 280)

        pygame.draw.rect(
            screen, WHITE, (SCREEN_WIDTH // 2 - 200, 330, 400, 60), 3, border_radius=10
        )
        draw_text(name, font_button, RED, screen, SCREEN_WIDTH // 2, 360)

        if name in existing_scores:
            loaded_score = existing_scores[name]
            draw_text(
                f"SCORE CHARGÉ : {loaded_score} PTS",
                font_small,
                GREEN,
                screen,
                SCREEN_WIDTH // 2,
                420,
            )
            draw_text(
                "[R] POUR RÉINITIALISER",
                font_small,
                GRAY,
                screen,
                SCREEN_WIDTH // 2,
                450,
            )
        elif len(name) > 0:
            draw_text("NOUVEAU JOUEUR", font_small, GRAY, screen, SCREEN_WIDTH // 2, 420)

        draw_text("ENTREE POUR VALIDER", font_small, WHITE, screen, SCREEN_WIDTH // 2, 550)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) > 0:
                    return name, loaded_score
                elif event.key == pygame.K_r and name in existing_scores:
                    loaded_score = 0
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return None, 0
                else:
                    if len(name) < 12 and event.unicode.isalnum():
                        name += event.unicode.upper()
        pygame.display.update()


def start_game(difficulty):
    player_name, global_score = name_input_menu()
    if not player_name:
        return

    # Boucle de manches
    play_round = True
    while play_round:
        try:
            with open(WORDS_FILE, "r", encoding="utf-8") as f:
                words = [l.strip().upper() for l in f.readlines() if l.strip()]
        except:
            words = ["PYTHON", "HANGMAN", "PYGAME"]

        easy = [m for m in words if len(m) <= 5]
        medium = [m for m in words if 5 < len(m) <= 8]
        hard = [m for m in words if len(m) > 8]

        if difficulty == 3:
            mystery_word = random.choice(hard if hard else words)
        elif difficulty == 2:
            mystery_word = random.choice(medium if medium else words)
        else:
            mystery_word = random.choice(easy if easy else words)

        hint_letter = random.choice(mystery_word)
        found_letters = [l for l in mystery_word if l == hint_letter or l == "-"]
        lives, errors = 7, 0

        keyboard_letters = []
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            x = 80 + (i % 13) * 60
            y = 540 + (i // 13) * 60
            status = "hint" if letter == hint_letter else "free"
            keyboard_letters.append(
                {
                    "letter": letter,
                    "rect": pygame.Rect(x, y, 45, 45),
                    "status": status,
                    "clicked": (letter == hint_letter),
                }
            )

        in_game = True
        while in_game:
            apply_dark_filter()
            draw_text(f"JOUEUR : {player_name}", font_small, WHITE, screen, 120, 30)
            draw_text(f"SCORE : {global_score}", font_small, GOLD, screen, 120, 55)
            draw_text(f"VIES : {lives}/7", font_small, RED, screen, 120, 80)
            draw_hangman(screen, errors)

            pygame.draw.rect(
                screen, (10, 10, 10), (SCREEN_WIDTH // 2 - 250, 380, 500, 80), border_radius=15
            )
            display_word = "".join([l + " " if l in found_letters else "_ " for l in mystery_word])
            draw_text(display_word, font_button, GOLD, screen, SCREEN_WIDTH // 2, 420)

            m_pos = pygame.mouse.get_pos()
            for t in keyboard_letters:
                c_rect = GOLD if t["rect"].collidepoint(m_pos) and not t["clicked"] else WHITE
                if t["status"] == "correct":
                    c_rect = GREEN
                elif t["status"] == "wrong":
                    c_rect = RED
                elif t["status"] == "hint":
                    c_rect = GRAY
                pygame.draw.rect(screen, c_rect, t["rect"], border_radius=5)
                draw_text(
                    t["letter"],
                    font_keys,
                    BLACK if c_rect == WHITE or c_rect == GOLD else WHITE,
                    screen,
                    t["rect"].centerx,
                    t["rect"].centery,
                )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # --- GESTION SOURIS AVEC SONS ---
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for t in keyboard_letters:
                        if t["rect"].collidepoint(m_pos) and not t["clicked"]:
                            t["clicked"] = True
                            if t["letter"] in mystery_word:
                                found_letters.append(t["letter"])
                                t["status"] = "correct"
                                if "win" in sounds:
                                    sounds["win"].play()
                            else:
                                lives -= 1
                                errors += 1
                                t["status"] = "wrong"
                                if "lose" in sounds:
                                    sounds["lose"].play()

                # --- GESTION CLAVIER AVEC SONS ---
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    key_pressed = event.unicode.upper()
                    for t in keyboard_letters:
                        if t["letter"] == key_pressed and not t["clicked"]:
                            t["clicked"] = True
                            if t["letter"] in mystery_word:
                                found_letters.append(t["letter"])
                                t["status"] = "correct"
                                if "win" in sounds:
                                    sounds["win"].play()
                            else:
                                lives -= 1
                                errors += 1
                                t["status"] = "wrong"
                                if "lose" in sounds:
                                    sounds["lose"].play()

            # --- VICTOIRE ---
            if all(l in found_letters for l in mystery_word):
                if "win" in sounds:
                    sounds["win"].play()
                global_score += (lives * 10) * difficulty
                draw_text("VICTOIRE !", font_title, GOLD, screen, SCREEN_WIDTH // 2, 300)
                pygame.display.update()
                pygame.time.delay(1200)
                in_game = False

            # --- DEFAITE (GAME OVER) ---
            if lives <= 0:
                if "lose" in sounds:
                    sounds["lose"].play()
                save_score(player_name, global_score)
                lost_menu = True
                while lost_menu:
                    screen.fill(BLACK)
                    draw_text("GAME OVER", font_title, RED, screen, SCREEN_WIDTH // 2, 180)
                    draw_text(f"LE MOT ÉTAIT : {mystery_word}", font_button, WHITE, screen, SCREEN_WIDTH // 2, 280)
                    draw_text(f"SCORE FINAL : {global_score}", font_button, GOLD, screen, SCREEN_WIDTH // 2, 350)

                    b_replay = pygame.Rect(SCREEN_WIDTH // 2 - 210, 450, 200, 60)
                    b_menu = pygame.Rect(SCREEN_WIDTH // 2 + 10, 450, 200, 60)
                    m_p = pygame.mouse.get_pos()

                    for b, txt in [(b_replay, "REJOUER"), (b_menu, "MENU")]:
                        pygame.draw.rect(
                            screen,
                            RED if b.collidepoint(m_p) else GRAY,
                            b,
                            border_radius=10,
                        )
                        draw_text(txt, font_button, WHITE, screen, b.centerx, b.centery)

                    for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                            if b_replay.collidepoint(m_p):
                                lost_menu = False
                                in_game = False
                            if b_menu.collidepoint(m_p):
                                return
                    pygame.display.update()
            pygame.display.update()


def word_input_menu():
    input_text, msg, msg_color = "", "", (0, 180, 0)
    scroll_y = 0
    running = True

    f_title = get_font("Butcherman-Regular.ttf", 35)
    f_list = get_font("Frijole-Regular.ttf", 14)

    # Chargement initial optimisé
    def load_words():
        if os.path.exists(WORDS_FILE):
            with open(WORDS_FILE, "r", encoding="utf-8") as f:
                return sorted([line.strip().upper() for line in f.readlines() if line.strip()])
        return []

    current_words = load_words()

    while running:
        apply_dark_filter()

        # --- LISTE DES MOTS ---
        pygame.draw.rect(screen, (20, 20, 20), (50, 100, 250, 500), border_radius=10)
        pygame.draw.rect(screen, (255, 215, 0), (50, 100, 250, 500), 2, border_radius=10)
        draw_text(f"DICTIONNAIRE ({len(current_words)})", f_list, (255, 215, 0), screen, 175, 80)

        for i, m in enumerate(current_words):
            y_pos = 120 + i * 30 - scroll_y
            if 110 < y_pos < 580:
                txt_surf = f_list.render(m, True, (255, 255, 255))
                screen.blit(txt_surf, (75, y_pos))

        # --- ZONE DE SAISIE ---
        draw_text("AJOUTER / SUPPRIMER", f_title, (255, 255, 255), screen, 600, 150)
        pygame.draw.rect(screen, (255, 255, 255), (450, 250, 300, 60), 3, border_radius=10)
        draw_text(input_text, f_title, (200, 0, 0), screen, 600, 280)

        if msg:
            draw_text(msg, f_list, msg_color, screen, 600, 340)

        # --- AIDE ---
        commands = [
            ("MOLETTE : DEFILER", (80, 80, 80)),
            ("[ENTREE] : VALIDER", (0, 180, 0)),
            ("[SUPPR] : SUPPRIMER", (200, 0, 0)),
            ("[ECHAP] : RETOUR", (255, 255, 255)),
        ]
        for idx, (txt, col) in enumerate(commands):
            draw_text(txt, f_list, col, screen, 600, 450 + idx * 35)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll_y = max(0, scroll_y - 40)
                if event.button == 5:
                    scroll_y += 40

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_RETURN and input_text:
                    if input_text in current_words:
                        msg, msg_color = "DEJA PRESENT", (200, 0, 0)
                    else:
                        with open(WORDS_FILE, "a", encoding="utf-8") as f:
                            f.write(f"\n{input_text}")
                        current_words.append(input_text)
                        current_words.sort()
                        msg, msg_color = "MOT ENREGISTRE", (0, 180, 0)
                        input_text = ""

                elif event.key == pygame.K_DELETE:
                    if input_text in current_words:
                        current_words.remove(input_text)
                        with open(WORDS_FILE, "w", encoding="utf-8") as f:
                            f.write("\n".join(current_words))
                        msg, msg_color = "SUPPRIME", (255, 215, 0)
                        input_text = ""

                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    msg = ""
                else:
                    if len(input_text) < 18 and (event.unicode.isalpha() or event.unicode == "-"):
                        input_text += event.unicode.upper()
                        msg = ""

        pygame.display.update()


def difficulty_menu():
    while True:
        apply_dark_filter()
        m_pos = pygame.mouse.get_pos()
        draw_text("DIFFICULTÉ", font_title, WHITE, screen, SCREEN_WIDTH // 2, 100)
        btns = [
            (pygame.Rect(SCREEN_WIDTH // 2 - 125, 250, 250, 60), "FACILE", 1),
            (pygame.Rect(SCREEN_WIDTH // 2 - 125, 330, 250, 60), "MOYEN", 2),
            (pygame.Rect(SCREEN_WIDTH // 2 - 125, 410, 250, 60), "EXPERT", 3),
        ]
        for b, t, d in btns:
            pygame.draw.rect(
                screen, RED if b.collidepoint(m_pos) else BLACK, b, border_radius=12
            )
            draw_text(t, font_button, WHITE, screen, b.centerx, b.centery)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for b, t, d in btns:
                    if b.collidepoint(m_pos):
                        start_game(d)
                        return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return
        pygame.display.update()


def main_menu():
    angle = 0  # Variable pour l'oscillation
    clock = pygame.time.Clock()  # Pour stabiliser la vitesse
    while True:
        apply_dark_filter()
        m_pos = pygame.mouse.get_pos()
        angle += 0.01
        offset_y = math.sin(angle) * 8  # Fait osciller le titre
        
        draw_text("LE PENDU", font_title, WHITE, screen, SCREEN_WIDTH // 2, 100 + offset_y)
        
        btns = [
            (pygame.Rect(SCREEN_WIDTH // 2 - 125, 220, 250, 60), "JOUER"),
            (pygame.Rect(SCREEN_WIDTH // 2 - 125, 300, 250, 60), "SCORES"),
            (pygame.Rect(SCREEN_WIDTH // 2 - 125, 380, 250, 60), "MOTS"),
            (pygame.Rect(SCREEN_WIDTH // 2 - 125, 460, 250, 60), "QUITTER"),
        ]
        for b, t in btns:
            pygame.draw.rect(
                screen, RED if b.collidepoint(m_pos) else BLACK, b, border_radius=12
            )
            draw_text(t, font_button, WHITE, screen, b.centerx, b.centery)
            
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if btns[0][0].collidepoint(m_pos):
                    difficulty_menu()
                elif btns[1][0].collidepoint(m_pos):
                    leaderboard_menu()
                elif btns[2][0].collidepoint(m_pos):
                    word_input_menu()
                elif btns[3][0].collidepoint(m_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


if __name__ == "__main__":
    main_menu()
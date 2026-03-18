import pygame
import json
from minigame import settings

HIGHSCORE_FILE = "minigame/highscore.json"

def load_highscore():
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return json.load(f).get("highscore", 0)
    except:
        return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump({"highscore": score}, f)

def show_end_screen(screen, score, player_rect):
    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()
    highscore = load_highscore()
    new_record = False

    if score > highscore:
        highscore = score
        save_highscore(score)
        new_record = True

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        screen.fill(settings.BLACK)
        y = settings.SCREEN_HEIGHT//2 - 50
        title = "NEW RECORD!" if new_record else "GAME OVER"
        title_surf = font.render(title, True, settings.WHITE)
        screen.blit(title_surf, (settings.SCREEN_WIDTH//2 - title_surf.get_width()//2, y))

        score_surf = font.render(f"Your Score: {score}", True, settings.WHITE)
        screen.blit(score_surf, (settings.SCREEN_WIDTH//2 - score_surf.get_width()//2, y + 50))

        highscore_surf = font.render(f"Highscore: {highscore}", True, settings.WHITE)
        screen.blit(highscore_surf, (settings.SCREEN_WIDTH//2 - highscore_surf.get_width()//2, y + 100))

        retry_surf = font.render("Click anywhere to retry", True, settings.WHITE)
        screen.blit(retry_surf, (settings.SCREEN_WIDTH//2 - retry_surf.get_width()//2, y + 150))

        pygame.display.flip()
        clock.tick(60)
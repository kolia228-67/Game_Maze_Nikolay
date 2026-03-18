import os
import pygame
from avatar_select import AvatarSelector
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, AVATAR_SIZE
from minigame.game import Game  # <-- импорт мини-игры
pygame.font.init()

class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.nickname = ""
        self.selected_avatar = None
        self.play_pressed = False
        self.font = pygame.font.SysFont(None, 40)
        self.input_rect = pygame.Rect(screen_width//2 - 200, screen_height//2 - 25, 300, 50)
        self.active_input = False

        # путь: загружаем аватар относительно файла menu.py (устойчиво к cwd)
        base_dir = os.path.dirname(__file__)
        default_avatar_path = os.path.join(base_dir, "assets", "avatars", "default.png")
        try:
            default_avatar = pygame.image.load(default_avatar_path).convert_alpha()
        except Exception:
            # fallback на старый относительный путь (на случай, если структура неожиданно другая)
            try:
                default_avatar = pygame.image.load("assets/avatars/default.png").convert_alpha()
            except Exception:
                # окончательный fallback — пустой спрайт, чтобы UI не ломался
                default_avatar = pygame.Surface((AVATAR_SIZE, AVATAR_SIZE), pygame.SRCALPHA)
                default_avatar.fill((180, 180, 180, 255))

        self.selected_avatar = pygame.transform.scale(default_avatar, (AVATAR_SIZE, AVATAR_SIZE))
        self.avatar_rect = pygame.Rect(self.input_rect.right + 10, self.input_rect.y, AVATAR_SIZE, AVATAR_SIZE)
        plus_size = 20
        self.plus_rect = pygame.Rect(
            self.avatar_rect.centerx - plus_size//2,
            self.avatar_rect.bottom + 5,
            plus_size,
            plus_size
        )
        self.play_rect = pygame.Rect(screen_width//2 - 150, screen_height - 80, 300, 60)
        self.avatar_selector = AvatarSelector(screen_width, screen_height)

    def start_minigame(self):
        """Запуск мини-игры"""
        game = Game(self.nickname, self.selected_avatar)
        game.run()

    def handle_event(self, event):
        if not self.avatar_selector.open:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.active_input = True
                else:
                    self.active_input = False
                if self.plus_rect.collidepoint(event.pos):
                    self.avatar_selector.open = True
                if self.play_rect.collidepoint(event.pos) and self.nickname.strip():
                    self.play_pressed = True
                    # --- вызов мини-игры ---
                    self.start_minigame()
            elif event.type == pygame.KEYDOWN and self.active_input:
                if event.key == pygame.K_BACKSPACE:
                    self.nickname = self.nickname[:-1]
                elif len(self.nickname) < 15:
                    self.nickname += event.unicode
        else:
            self.avatar_selector.handle_event(event)
            if self.avatar_selector.selected_avatar:
                self.selected_avatar = pygame.transform.scale(
                    self.avatar_selector.selected_avatar,
                    (AVATAR_SIZE, AVATAR_SIZE)
                )
                self.avatar_selector.selected_avatar = None

    def update(self):
        if self.avatar_selector.open:
            self.avatar_selector.update()

    def draw(self, screen):
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, self.input_rect, 2)
        nick_surface = self.font.render(self.nickname, True, WHITE)
        screen.blit(nick_surface, (self.input_rect.x + 5, self.input_rect.y + 10))
        screen.blit(self.selected_avatar, self.avatar_rect.topleft)
        pygame.draw.rect(screen, WHITE, self.plus_rect)
        plus_font = pygame.font.SysFont(None, 20)
        plus_surf = plus_font.render("+", True, BLACK)
        plus_rect_text = plus_surf.get_rect(center=self.plus_rect.center)
        screen.blit(plus_surf, plus_rect_text)
        pygame.draw.rect(screen, WHITE, self.play_rect)
        play_surf = self.font.render("Play", True, BLACK)
        play_rect_text = play_surf.get_rect(center=self.play_rect.center)
        screen.blit(play_surf, play_rect_text)
        if self.avatar_selector.open:
            self.avatar_selector.draw(screen)
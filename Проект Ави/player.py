import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

try:
    from settings import TOP_MARGIN
except Exception:
    try:
        from minigame.settings import TOP_MARGIN
    except Exception:
        TOP_MARGIN = 0

import minigame.maze as maze_module


class Player:
    # --------------------------------------------------
    # фиксированная стартовая позиция игрока
    # чуть левее центра карты, чтобы не спавниться в стене
    # --------------------------------------------------
    START_POS = (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)

    def __init__(self):
        self.speed = 1.25
        self.direction = "idle"

        self.frame_index = 0
        self.frame_counter = 0
        self.frame_speed = 10
        self.scale = 0.2

        # --------------------------------------------------
        # загрузка спрайтов игрока
        # --------------------------------------------------
        def load_image(path):
            try:
                img = pygame.image.load(path).convert_alpha()
            except Exception:
                img = pygame.Surface((64, 64), pygame.SRCALPHA)
                img.fill((200, 200, 200, 255))
            w = max(1, int(img.get_width() * self.scale))
            h = max(1, int(img.get_height() * self.scale))
            return pygame.transform.scale(img, (w, h))

        self.sprites = {
            "idle": [load_image("Персонажи/Игрок/player_idle.png")],
            "down": [load_image("Персонажи/Игрок/player_down_1.png"), load_image("Персонажи/Игрок/player_down_2.png")],
            "up": [load_image("Персонажи/Игрок/player_up_1.png"), load_image("Персонажи/Игрок/player_up_2.png")],
            "left": [load_image("Персонажи/Игрок/player_left_1.png"), load_image("Персонажи/Игрок/player_left_2.png")],
            "right": [load_image("Персонажи/Игрок/player_right_1.png"), load_image("Персонажи/Игрок/player_right_2.png")]
        }

        self.image = self.sprites["idle"][0]
        self.rect = self.image.get_rect()

        # --------------------------------------------------
        # ставим игрока в фиксированную стартовую позицию
        # --------------------------------------------------
        self.rect.topleft = Player.START_POS
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

        # --------------------------------------------------
        # проверка и исправление коллизии на старте (на всякий случай)
        # --------------------------------------------------
        self._fix_spawn()

    # --------------------------------------------------
    # проверка пересечения игрока со стенами лабиринта
    # --------------------------------------------------
    def _collides(self, rect):
        mask = getattr(maze_module, "WALL_MASK", None)
        maze_rect = getattr(maze_module, "MAZE_RECT", None)

        if mask is None or maze_rect is None:
            return False

        offset_x = rect.x - maze_rect.x
        offset_y = rect.y - maze_rect.y

        player_mask = pygame.mask.Mask((rect.width, rect.height), fill=True)

        try:
            overlap = mask.overlap_area(player_mask, (int(offset_x), int(offset_y)))
            return overlap > 0
        except Exception:
            return False

    # --------------------------------------------------
    # если игрок заспавнился внутри стены (редкий случай)
    # --------------------------------------------------
    def _fix_spawn(self):
        if not self._collides(self.rect):
            return

        # ищем ближайшее свободное место вокруг
        for radius in range(1, 200):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    test = self.rect.copy()
                    test.x += dx
                    test.y += dy

                    if not self._collides(test):
                        self.rect = test
                        self.pos_x = float(self.rect.x)
                        self.pos_y = float(self.rect.y)
                        return

    # --------------------------------------------------
    # движение игрока
    # --------------------------------------------------
    def move(self, keys):
        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed

        if dy < 0:
            self.direction = "up"
        elif dy > 0:
            self.direction = "down"
        elif dx < 0:
            self.direction = "left"
        elif dx > 0:
            self.direction = "right"
        else:
            self.direction = "idle"

        # движение по X
        new_rect = self.rect.copy()
        new_rect.x += dx
        if not self._collides(new_rect):
            self.rect = new_rect

        # движение по Y
        new_rect = self.rect.copy()
        new_rect.y += dy
        if not self._collides(new_rect):
            self.rect = new_rect

        self.pos_x = self.rect.x
        self.pos_y = self.rect.y

    # --------------------------------------------------
    # обновление анимации
    # --------------------------------------------------
    def update_animation(self):
        if self.direction == "idle":
            self.frame_index = 0
            return

        self.frame_counter += 1
        if self.frame_counter >= self.frame_speed:
            self.frame_counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.sprites[self.direction]):
                self.frame_index = 0

    # --------------------------------------------------
    # отрисовка игрока
    # --------------------------------------------------
    def draw(self, screen):
        self.image = self.sprites[self.direction][self.frame_index]
        screen.blit(self.image, self.rect)
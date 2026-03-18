import pygame
import random
from minigame import settings
from minigame import maze


class GameObject:

    def __init__(self, kind="normal"):
        self.kind = kind

        if kind == "normal":
            self.size = settings.OBJECT_SIZE
            self.color = settings.LIGHT_BLUE
        else:
            self.size = settings.SPECIAL_OBJECT_SIZE
            self.color = settings.YELLOW

        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.spawn_time = 0
        self.active = False

    def spawn(self, maze_img, objects=None):
        """Спавн объекта только в проходимом месте и не слишком близко к другим"""

        max_attempts = 200

        for _ in range(max_attempts):

            x = random.randint(0, settings.SCREEN_WIDTH - self.size)
            y = random.randint(settings.TOP_MARGIN, settings.SCREEN_HEIGHT - self.size)

            rect = pygame.Rect(x, y, self.size, self.size)

            # --- проверка стен (вся область объекта) ---
            wall_hit = False

            for px in range(rect.left, rect.right, 2):
                for py in range(rect.top, rect.bottom, 2):

                    mx = px
                    my = py - settings.TOP_MARGIN

                    if 0 <= mx < settings.SCREEN_WIDTH and 0 <= my < maze_img.get_height():
                        if maze.is_wall(maze_img, mx, my):
                            wall_hit = True
                            break
                if wall_hit:
                    break

            if wall_hit:
                continue

            # --- проверка расстояния между голубыми объектами ---
            if objects and self.kind == "normal":

                too_close = False

                for obj in objects:

                    if obj is self:
                        continue

                    if not obj.active:
                        continue

                    if obj.kind != "normal":
                        continue

                    distance = rect.centerx - obj.rect.centerx
                    distance = distance * distance + (rect.centery - obj.rect.centery) ** 2

                    min_dist = (settings.OBJECT_SIZE * 4) ** 2  # увеличено примерно в 2 раза

                    if distance < min_dist:
                        too_close = True
                        break

                if too_close:
                    continue

            # место найдено
            self.rect.topleft = (x, y)
            self.spawn_time = pygame.time.get_ticks()
            self.active = True
            return

        # если не нашли место
        self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.ellipse(screen, self.color, self.rect)
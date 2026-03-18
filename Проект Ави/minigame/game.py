import pygame
import random
from minigame import settings, maze, objects, end_screen
from player import Player

class Game:

    def __init__(self, nickname, avatar):
        self.nickname = nickname
        self.avatar = avatar
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)

        # Лабиринт
        self.maze_img, self.maze_rect = maze.load_maze()

        # Игрок
        self.player = Player()

        # Фиксированная стартовая позиция игрока
        self.set_fixed_player_spawn()

        # Объекты
        self.objects = [objects.GameObject("normal") for _ in range(settings.MAX_NORMAL_OBJECTS)]
        self.special = objects.GameObject("special")

        # Счёт и время
        self.score = 0
        self.start_time = pygame.time.get_ticks()

    # --------------------------------------------------
    # фиксированный спавн игрока (чуть левее центра)
    # --------------------------------------------------
    def set_fixed_player_spawn(self):
        center_x = self.maze_rect.left + self.maze_rect.width // 2
        center_y = self.maze_rect.top + self.maze_rect.height // 2

        fixed_x = center_x - self.player.rect.width // 2 - 50  # 50 пикселей левее центра
        fixed_y = center_y - self.player.rect.height // 2

        self.player.rect.topleft = (fixed_x, fixed_y)
        self.player.pos_x = float(self.player.rect.x)
        self.player.pos_y = float(self.player.rect.y)

        # поправка если заспавнился в стене
        self.player._fix_spawn()

    # --------------------------------------------------
    # проверка прямоугольника на пересечение со стеной
    # --------------------------------------------------
    def _rect_overlaps_wall(self, rect):
        img_w, img_h = self.maze_img.get_width(), self.maze_img.get_height()
        sample_points = [
            (rect.centerx, rect.centery),
            (rect.left + 1, rect.top + 1),
            (rect.right - 1, rect.top + 1),
            (rect.left + 1, rect.bottom - 1),
            (rect.right - 1, rect.bottom - 1),
        ]
        for sx, sy in sample_points:
            cx = int(sx)
            cy = int(sy - settings.TOP_MARGIN)
            if not (0 <= cx < img_w and 0 <= cy < img_h):
                return True
            try:
                if maze.is_wall(self.maze_img, cx, cy):
                    return True
            except Exception:
                return True
        return False

    # --------------------------------------------------
    # основной цикл игры
    # --------------------------------------------------
    def run(self):
        running = True
        while running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            old_rect = self.player.rect.copy()

            # движение игрока
            keys = pygame.key.get_pressed()
            try:
                self.player.move(keys)
            except Exception:
                self.player.rect = old_rect

            # проверка на стену
            if self._rect_overlaps_wall(self.player.rect):
                self.player.rect = old_rect

            # спавн обычных объектов
            for obj in self.objects:
                if not obj.active:
                    try:
                        obj.spawn(self.maze_img)
                    except Exception:
                        obj.active = False
                elif pygame.time.get_ticks() - obj.spawn_time > settings.NORMAL_OBJECT_LIFETIME * 1000:
                    obj.active = False

                if obj.active and self.player.rect.colliderect(obj.rect):
                    self.score += 1
                    obj.active = False

            # спавн особого объекта
            if not self.special.active and random.random() < 0.002:
                try:
                    self.special.spawn(self.maze_img)
                except Exception:
                    self.special.active = False

            if self.special.active:
                if pygame.time.get_ticks() - self.special.spawn_time > settings.SPECIAL_OBJECT_LIFETIME * 1000:
                    self.special.active = False
                if self.player.rect.colliderect(self.special.rect):
                    self.score += 3
                    self.special.active = False

            # отрисовка
            try:
                self.screen.fill(settings.BLACK)
                self.screen.blit(self.maze_img, self.maze_rect)
            except Exception:
                self.screen.fill(settings.BLACK)

            try:
                self.player.update_animation()
                self.player.draw(self.screen)
            except Exception:
                pygame.draw.rect(self.screen, settings.WHITE, self.player.rect)

            # HUD: аватарка и ник
            if self.avatar:
                try:
                    avatar_rect = self.avatar.get_rect(topleft=(10, 10))
                    self.screen.blit(self.avatar, avatar_rect)
                    nick_surf = self.font.render(self.nickname, True, settings.WHITE)
                    nick_rect = nick_surf.get_rect(midleft=(avatar_rect.right + 5, avatar_rect.centery))
                    self.screen.blit(nick_surf, nick_rect)
                except Exception:
                    nick_surf = self.font.render(self.nickname, True, settings.WHITE)
                    self.screen.blit(nick_surf, (10, 10))

            # объекты
            for obj in self.objects:
                try:
                    obj.draw(self.screen)
                except Exception:
                    pass
            try:
                self.special.draw(self.screen)
            except Exception:
                pass

            # таймер и счёт
            seconds = settings.GAME_DURATION - (pygame.time.get_ticks() - self.start_time) // 1000
            if seconds <= 0:
                running = False

            time_surf = self.font.render(f"Time: {seconds}", True, settings.WHITE)
            score_surf = self.font.render(f"Score: {self.score}", True, settings.WHITE)
            try:
                self.screen.blit(time_surf, (settings.SCREEN_WIDTH - 150, 10))
                self.screen.blit(score_surf, (settings.SCREEN_WIDTH - 150, 40))
            except Exception:
                pass

            pygame.display.flip()

        # конец игры
        try:
            end_screen.show_end_screen(self.screen, self.score, self.player.rect)
        except Exception:
            pass
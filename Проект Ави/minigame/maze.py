import os
import pygame
from minigame import settings

# модульные переменные (будут установлены при load_maze)
MAZE_IMG = None
MAZE_RECT = None
WALL_MASK = None

def _build_wall_mask_from_image(img, wall_color=(255, 255, 255), buffer=2):
    # Строит маску стен (pygame.mask.Mask) из изображения img
    # wall_color: цвет, считающийся стеной (RGB)
    # buffer: сколько пикселей расширить маску вокруг белых пикселей (диляция)
    w, h = img.get_width(), img.get_height()
    base = pygame.mask.Mask((w, h))
    for y in range(h):
        for x in range(w):
            try:
                if img.get_at((x, y))[:3] == wall_color:
                    base.set_at((x, y), 1)
            except Exception:
                base.set_at((x, y), 1)
    if buffer <= 0:
        return base
    dilated = pygame.mask.Mask((w, h))
    for y in range(h):
        for x in range(w):
            if base.get_at((x, y)):
                x0, x1 = max(0, x - buffer), min(w - 1, x + buffer)
                y0, y1 = max(0, y - buffer), min(h - 1, y + buffer)
                for yy in range(y0, y1 + 1):
                    for xx in range(x0, x1 + 1):
                        dilated.set_at((xx, yy), 1)
    return dilated

def load_maze(buffer=2):
    # Загружает maze.png и строит WALL_MASK
    global MAZE_IMG, MAZE_RECT, WALL_MASK

    # путь: файл maze.png относительно minigame/ (this file)
    base_dir = os.path.dirname(__file__)  # minigame/
    maze_path = os.path.normpath(os.path.join(base_dir, "..", "assets", "maps", "maze.png"))
    try:
        maze_img = pygame.image.load(maze_path).convert()
    except Exception:
        # fallback: пробуем старый относительный путь
        maze_img = pygame.image.load("assets/maps/maze.png").convert()

    maze_rect = maze_img.get_rect()
    maze_rect.topleft = (0, settings.TOP_MARGIN)

    try:
        mask = _build_wall_mask_from_image(maze_img, wall_color=(255, 255, 255), buffer=buffer)
    except Exception:
        mask = pygame.mask.Mask((maze_img.get_width(), maze_img.get_height()))

    MAZE_IMG = maze_img
    MAZE_RECT = maze_rect
    WALL_MASK = mask

    return maze_img, maze_rect

def is_wall(maze_img, x, y):
    # Проверяем стену по координате
    global WALL_MASK, MAZE_IMG
    if WALL_MASK is not None:
        w, h = WALL_MASK.get_size()
        if x < 0 or x >= w or y < 0 or y >= h:
            return True
        try:
            return bool(WALL_MASK.get_at((x, y)))
        except Exception:
            pass
    try:
        color = maze_img.get_at((x, y))[:3]
        return color == (255, 255, 255)
    except Exception:
        return True
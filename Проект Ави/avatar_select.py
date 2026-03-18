import pygame
from settings import BLACK, WHITE
import os

class AvatarSelector:

    def __init__(self, screen_width, screen_height):

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.open = False
        self.selected_avatar = None

        self.avatars = []
        self.avatar_rects = []

        avatar_files = sorted(os.listdir("assets/avatars"))

        size = 100
        margin = 10

        total_width = size*3 + margin*2
        total_height = size*3 + margin*2

        start_x = (screen_width - total_width)//2
        start_y = (screen_height - total_height)//2

        for i, file in enumerate(avatar_files):

            path = os.path.join("assets/avatars", file)
            img = pygame.image.load(path).convert_alpha()
            img = self.fit_square(img, size)

            self.avatars.append(img)

            row = i // 3
            col = i % 3

            rect = pygame.Rect(
                start_x + col*(size+margin),
                start_y + row*(size+margin),
                size,
                size
            )

            self.avatar_rects.append(rect)

        # большой крестик в левом верхнем углу
        self.exit_rect = pygame.Rect(30, 30, 80, 80)

    def fit_square(self, img, size):

        square = pygame.Surface((size, size))
        square.fill(BLACK)

        w, h = img.get_size()

        scale = min(size/w, size/h)

        new_w = int(w*scale)
        new_h = int(h*scale)

        img_scaled = pygame.transform.scale(img, (new_w, new_h))

        x_offset = (size - new_w)//2
        y_offset = (size - new_h)//2

        square.blit(img_scaled, (x_offset, y_offset))

        return square

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.exit_rect.collidepoint(event.pos):
                self.open = False
                return

            for i, rect in enumerate(self.avatar_rects):

                if rect.collidepoint(event.pos):

                    self.selected_avatar = self.avatars[i]
                    self.open = False

    def update(self):
        pass

    def draw(self, screen):

        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        screen.blit(overlay, (0,0))

        for img, rect in zip(self.avatars, self.avatar_rects):
            screen.blit(img, rect.topleft)

        pygame.draw.rect(screen, WHITE, self.exit_rect)

        font = pygame.font.SysFont(None, 60)
        text = font.render("X", True, BLACK)

        text_rect = text.get_rect(center=self.exit_rect.center)

        screen.blit(text, text_rect)
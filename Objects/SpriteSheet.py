import pygame
from time import time


class SpriteSheet:
    def __init__(self, image, w, h, duration=None):
        self.base_image = pygame.image.load(image)
        self.images = []
        self.duration = duration
        self.last_change = time()
        self.selected_image = 0
        sprite_w = self.base_image.get_width() / w
        sprite_h = self.base_image.get_height() / h

        x = 0
        y = 0
        for i in range(h):
            for i in range(w):
                self.images.append(self.get_image(x, y, sprite_w, sprite_h))
                x += sprite_w
            x = 0
            y += sprite_h

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.base_image, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 1))
        return image

    @property
    def current_image(self):
        if time() - self.last_change >= self.duration:
            self.selected_image += 1
            if self.selected_image >= len(self.images):
                self.selected_image = 0
            self.last_change = time()
        return self.images[self.selected_image]

import pygame

from Platformer.Objects.ObjectBase import ObjectBase
from Platformer.Objects.Cache import get_image


class Air(ObjectBase):
    def __init__(self, **kwargs):
        ObjectBase.__init__(self, **kwargs)
        self.solid = False


class Block(ObjectBase):
    def __init__(self, **kwargs):
        ObjectBase.__init__(self, **kwargs)

        self.color = None
        self.image = None
        if "color" in kwargs:
            self.color = kwargs["color"]
        else:
            self.image = get_image(kwargs["image"])

    def draw(self):
        if self.image is None:
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.w, self.h))
        else:
            self.screen.blit(self.image, (self.x, self.y))


class Player(ObjectBase):
    def __init__(self, **kwargs):
        ObjectBase.__init__(self, **kwargs)
        self.physics = True

    def draw(self):
        pygame.draw.circle(self.screen, (255, 255, 255), self.get_pos_int, 5)
        self.draw_hitbox()

import pygame

from PyGE.Objects.ObjectBase import ObjectBase
from PyGE.Objects.Cache import get_image, get_spritesheet
from ..exceptions import DisplayMethodNotDefinedException


class Air(ObjectBase):
    def __init__(self, **kwargs):
        ObjectBase.__init__(self, **kwargs)
        self.solid = False


class Block(ObjectBase):
    def __init__(self, **kwargs):
        ObjectBase.__init__(self, **kwargs)

        self.color = None
        self.image = None
        self.spritesheet = None
        if "color" in kwargs:
            self.color = kwargs["color"]
        elif "image" in kwargs:
            self.image = get_image(kwargs["image"])
        elif "spritesheet" in kwargs:
            self.spritesheet = get_spritesheet(kwargs["spritesheet"])
        else:
            raise DisplayMethodNotDefinedException("No Method Of Display Has Been Defined For An Object")

    def draw(self):
        if self.color is not None:
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.w, self.h))
        elif self.image is not None:
            self.screen.blit(self.image, (self.x, self.y))
        else:
            self.screen.blit(self.spritesheet.current_image, (self.x, self.y))



class Player(ObjectBase):
    def __init__(self, **kwargs):
        ObjectBase.__init__(self, **kwargs)
        self.physics = True

    def draw(self):
        pygame.draw.circle(self.screen, (255, 255, 255), self.get_pos_int, 5)
        self.draw_hitbox()

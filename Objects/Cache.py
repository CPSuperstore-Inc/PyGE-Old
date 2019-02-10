import pygame
import os

from SpriteSheet import SpriteSheet
from ..exceptions import NotInCacheException

Images = {}
SpriteSheets = {}
Font = {}


def add_image(name, path, w=None, h=None):
    img = pygame.image.load(path)
    if w is not None:
        img.transform.scale(w, h)
    Images[name] = img


def get_image(name):
    if name in Images:
        return Images[name]
    else:
        return pygame.image.load(name)


def add_spritesheet(name, image, w, h, changes_per_s=None, duration=None):
    if changes_per_s is not None:
        duration = 1.0 / changes_per_s
    SpriteSheets[name] = SpriteSheet(image, w, h, duration)


def get_spritesheet(name):
    if name in SpriteSheets:
        return SpriteSheets[name]
    else:
        raise NotInCacheException("'{}' Is Not In SpriteSheet Cache".format(name))


def add_font(name, font, size):
    if os.path.isfile(font):
        font = pygame.font.Font(font, size)
    else:
        font = pygame.font.SysFont(font, size)
    Font[name] = font


def get_font(name):
    if name in Font:
        return Font[name]
    else:
        raise NotInCacheException("'{}' Is Not In Font Cache".format(name))

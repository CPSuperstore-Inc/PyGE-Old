import pygame
import os

from PyGE.Objects.SpriteSheet import SpriteSheet
from PyGE.GlobalVariable import block_size
from ..exceptions import NotInCacheException

Images = {}
SpriteSheets = {}
Font = {}


def add_image(name:str, path:str, w:int=None, h:int=None):
    img = pygame.image.load(path)
    if w is None:
        w, h = block_size
    img = pygame.transform.scale(img, (w, h))
    Images[name] = img


def get_image(name:str):
    if name in Images:
        return Images[name]
    else:
        return pygame.image.load(name)


def add_spritesheet(name:str, image:str, w:int, h:int, changes_per_s:float=None, duration:float=None, final_size:float=None, invisible_color:tuple=(0, 0, 0)):
    if changes_per_s is not None:
        duration = 1.0 / changes_per_s
    SpriteSheets[name] = SpriteSheet(image, w, h, duration, final_size=final_size, invisible_color=invisible_color)


def get_spritesheet(name:str):
    if name in SpriteSheets:
        return SpriteSheets[name]
    else:
        raise NotInCacheException("'{}' Is Not In SpriteSheet Cache".format(name))


def add_font(name:str, font:str, size:int):
    if os.path.isfile(font):
        font = pygame.font.Font(font, size)
    else:
        font = pygame.font.SysFont(font, size)
    Font[name] = font


def get_font(name:str):
    if name in Font:
        return Font[name]
    else:
        raise NotInCacheException("'{}' Is Not In Font Cache".format(name))

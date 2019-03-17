import pygame
import os

from PyGE.Objects.SpriteSheet import SpriteSheet
from PyGE.GlobalVariable import block_size
from ..exceptions import NotInCacheException

Images = {}
SpriteSheets = {}
Font = {}


def add_image(name:str, path:str, w:int=None, h:int=None):
    """
    Adds a new image to the cache
    :param name: the image's alias (refrence name)
    :param path: the path to the image
    :param w: the width to make the image (If not specified, the block size will be used)
    :param h: the height to make the image (If not specified, the block size will be used)
    """
    img = pygame.image.load(path)
    if w is None:
        w, h = block_size
    img = pygame.transform.scale(img, (w, h))
    Images[name] = img


def get_image(name:str):
    """
    Returns the image from the cache by refrence name
    :param name: the name of the image (this can also be the path to a new image)
    :return: the image as a pygame surface
    """
    if name in Images:
        return Images[name]
    else:
        return pygame.image.load(name)


def add_spritesheet(name:str, image:str, w:int, h:int, changes_per_s:float=None, duration:float=None, final_size:float=None, invisible_color:tuple=(0, 0, 0)):
    """
    Adds a spritesheet to the cache
    :param name: the spritesheet's alias (refrence name)
    :param image: the path to the image of the sprite sheet - NOTE: Read left to right, top to bottom
    :param w: the width of each image segment
    :param h: the height of each image segment
    :param changes_per_s: the number of times per second to switch to the next image (specify either this, or duration)
    :param duration: the amount of time to stay on each image (specify either this, or changes_per_s)
    :param final_size: the size to scale each frame of the sprite sheet to
    :param invisible_color: the color which is invisible (DO NOT PICK A COLOR ON YOUR SPRITESHEET!)
    """
    if changes_per_s is not None:
        duration = 1.0 / changes_per_s
    SpriteSheets[name] = SpriteSheet(image, w, h, duration, final_size=final_size, invisible_color=invisible_color)


def get_spritesheet(name:str):
    """
    Returns the sprite sheet from the cache by refrence name
    :param name: the name of the sprite sheet
    :return: the sprite sheet as a SpriteSheet object
    """
    if name in SpriteSheets:
        return SpriteSheets[name]
    else:
        raise NotInCacheException("'{}' Is Not In SpriteSheet Cache".format(name))


def add_font(name:str, font:str, size:int):
    """
    Adds a font to the cache
    :param name: the font's alias (refrence name)
    :param font: the name of the font (can be System Font, or .ttf or .otf file)
    :param size: the size of the font (in pt)
    """
    if os.path.isfile(font):
        font = pygame.font.Font(font, size)
    else:
        font = pygame.font.SysFont(font, size)
    Font[name] = font


def get_font(name:str):
    """
    Returns the font from the cache by refrence name
    :param name: the name of the font
    :return: the font as a Pygame Font object
    """
    if name in Font:
        return Font[name]
    else:
        raise NotInCacheException("'{}' Is Not In Font Cache".format(name))

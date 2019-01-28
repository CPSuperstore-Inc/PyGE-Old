import pygame

Images = {}


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

import pygame

from PyGE.Objects.ObjectBase import ObjectBase


class Block(ObjectBase):
    def __init__(self, **kwargs):
        ObjectBase.__init__(self, **kwargs)


class Player(ObjectBase):
    def __init__(self, **kwargs):
        ObjectBase.__init__(self, **kwargs)
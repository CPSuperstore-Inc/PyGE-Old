import pygame

from PyGE.Objects.ObjectBase import ObjectBase


class Air(ObjectBase):
    def __init__(self, **kwargs):
        kwargs["visible"] = False
        ObjectBase.__init__(self, **kwargs)
        self.solid = False


class Block(ObjectBase):
    def __init__(self, **kwargs):
        ObjectBase.__init__(self, **kwargs)


class Player(ObjectBase):
    def __init__(self, **kwargs):
        ObjectBase.__init__(self, **kwargs)
        self.movable = True
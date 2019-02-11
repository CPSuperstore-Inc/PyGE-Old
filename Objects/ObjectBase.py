import pygame
from math import sin, cos, degrees
from time import time

import PyGE.Objects.GlobalVariable as GlobalVariable
from PyGE.Objects.Ticker import Ticker
from PyGE.Objects.Cache import get_image, get_spritesheet
from PyGE.utils import value_or_default
from ..exceptions import DisplayMethodNotDefinedException


class ObjectBase:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.screen = kwargs["screen"]
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.w = kwargs["w"]
        self.h = kwargs["h"]
        self.level = kwargs["level"]
        self.visible = value_or_default(kwargs, "visible", True)
        self.multi_jump = False
        self.speed = 100

        self.color = None
        self.image = None
        self.spritesheet = None

        if self.visible is True:
            if "color" in kwargs:
                self.color = kwargs["color"]
            elif "image" in kwargs:
                self.image = get_image(kwargs["image"])
            elif "spritesheet" in kwargs:
                self.spritesheet = get_spritesheet(kwargs["spritesheet"])
            else:
                raise DisplayMethodNotDefinedException("No Method Of Display Has Been Defined For Block Type '{}'".format(type(self).__name__))

        self.tick = Ticker()

        self.physics = False
        self.fall_start = False
        self.fall_velocity = 0
        self.movable = False

        self.clock = pygame.time.Clock()
        self.frame_delay = -1

        self.name = self.__get_optional_property("name")

        self.solid = True
        self.angle = 0

        self.last_x_change = 0
        self.last_y_change = 0

        self.vertical_velocity = False
        self.is_projectile = False

    @property
    def get_pos(self):
        return self.x, self.y

    @property
    def get_pos_int(self):
        return int(round(self.x, 0)), int(round(self.y, 0))

    @property
    def hitbox(self):
        return pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 1)

    def __get_optional_property(self, prop):
        if prop in self.kwargs:
            return self.kwargs[prop]

    def update(self):
        if self.movable:
            self.check_collision()
        self.frame_delay = self.tick.tick
        if self.physics is True:
            self.physics_update()

    def update_draw(self):
        self.update()
        self.draw()

    def physics_update(self):
        if self.physics is True:
            if self.vertical_velocity is not False:
                t = time() - self.fall_start
                self.is_projectile = True
                change = (self.vertical_velocity * t) + (0.5 * GlobalVariable.g * t ** 2)

                if change <= 0:
                    self.vertical_velocity = False
                    self.fall_start = time()
                    self.is_projectile = False
                for i in range(int(abs(change))):
                    self.y -= 1
                    if self.check_collision(collision_action=False):
                        self.y += 1
                        self.fall_start = False
                        self.is_projectile = False
            else:
                self.check_collision()
                if self.fall_start is not False:
                    self.is_projectile = True
                    change = int(GlobalVariable.g * (time() - self.fall_start))
                    for i in range(abs(change)):
                        self.y += 1
                        if self.check_collision(collision_action=False):
                            self.y -= 1
                            self.fall_start = False
                            self.is_projectile = False
                            break

    def draw_hitbox(self, color=None, thickness=1):
        if color is None:
            color = (255, 255, 255)
        pygame.draw.rect(self.screen, color, self.hitbox, thickness)

    def draw(self):
        if self.visible is True:
            if self.color is not None:
                pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.w, self.h))
            elif self.image is not None:
                self.screen.blit(self.image, (self.x, self.y))
            else:
                self.screen.blit(self.spritesheet.current_image, (self.x, self.y))

    def check_collision(self, collision_action=True):
        collide = False
        for item in self.level:
            if item == self or item.solid is False:
                continue
            if self.has_collided(item):
                if collision_action:
                    self.collision(item)
                    item.collision(self)
                collide = True
        if self.physics is True:
            if collide is False:
                if self.fall_start is False:
                    self.fall_start = time()
            else:
                self.fall_start = False
        return collide

    def directional_move(self, x_change, y_change, check_collision=True):
        x_change *= self.speed
        y_change *= self.speed
        self.x += x_change * self.frame_delay
        self.y += y_change * self.frame_delay
        self.last_x_change = x_change * self.frame_delay
        self.last_y_change = y_change * self.frame_delay

        if check_collision is True and self.movable:
            self.check_collision()

    def undo_last_move(self):
        self.x -= self.last_x_change
        self.y -= self.last_y_change

    def rotational_move(self, distance, angle=None):
        if angle is None:
            angle = self.angle

        self.last_x_change = distance * degrees(cos(angle))
        self.last_y_change = distance * degrees(sin(angle))
        self.x = self.last_x_change
        self.y = self.last_y_change

    def has_collided(self, other):
        x1 = self.x
        y1 = self.y
        x2 = x1 + self.w
        y2 = y1 + self.h
        rect = other.hitbox

        if rect.collidepoint(x1, y1):
            return True
        if rect.collidepoint(x1, y2):
            return True
        if rect.collidepoint(x2, y1):
            return True
        if rect.collidepoint(x2, y2):
            return True
        return False

    def collision(self, other):
        self.undo_last_move()

    def delete(self):
        if self not in GlobalVariable.delete_queue:
            GlobalVariable.delete_queue.append(self)

    def __del__(self):
        self.delete()

    def jump(self, jump_velocity):
        if self.multi_jump is True:
            self.vertical_velocity = jump_velocity
        elif self.is_projectile is False:
            self.fall_start = time()
            self.vertical_velocity = jump_velocity

import pygame

from math import sin, cos, degrees
from time import time

import PyGE.GlobalVariable as GlobalVariable
from PyGE.Objects.Cache import get_image, get_spritesheet
from PyGE.Objects.Ticker import Ticker
from PyGE.utils import value_or_default, get_mandatory_value
from ..exceptions import DisplayMethodNotDefinedException


class ObjectBase:
    """
    This is the class which every block/entity, which is placed in the level map MUST inherit from.
    This class takes care of all the basic functions for a block. You can overide anything you need.
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        # mandatory arguements
        self.screen = get_mandatory_value(kwargs, "screen")
        self.x = get_mandatory_value(kwargs, "x")
        self.y = get_mandatory_value(kwargs, "y")
        self.w = get_mandatory_value(kwargs, "w")
        self.h = get_mandatory_value(kwargs, "h")
        self.platformer = get_mandatory_value(kwargs, "platformer")
        self.level = get_mandatory_value(kwargs, "level")

        self.initial_x, self.initial_y = self.x, self.y

        # optional arge=uements
        self.state = value_or_default(kwargs, "state", "idle")
        self.visible = value_or_default(kwargs, "visible", True)
        self.multi_jump = False
        self.speed = 100

        self.color = None
        self.image = None
        self.spritesheet = None

        self.clicked = False

        if self.visible is True:
            if "color" in kwargs:
                self.color = kwargs["color"]
            elif "image" in kwargs:
                self.image = get_image(kwargs["image"])
            elif "spritesheet" in kwargs:
                self.spritesheet = get_spritesheet(kwargs["spritesheet"])
            else:
                raise DisplayMethodNotDefinedException(
                    "No Method Of Display Has Been Defined For Block Type '{}'".format(type(self).__name__))

        self.tick = Ticker()

        self.physics = False
        self.fall_start = False
        self.fall_velocity = 0
        self.movable = False
        self.collision_events = True

        self.clock = pygame.time.Clock()
        self.frame_delay = -1

        self.name = value_or_default(kwargs, "name", "Anonymous")

        self.solid = True
        self.angle = 0

        self.last_x_change = 0
        self.last_y_change = 0

        self.vertical_velocity = False
        self.is_projectile = False

    @property
    def get_pos(self):
        """
        Returns the x and y position of the top-left corner of the object as a tuple.
        This is the floating-point value of the coordinates.
        """
        return self.x, self.y

    @property
    def get_pos_int(self):
        """
        Returns the x and y position of the top-left corner of the object as a tuple.
        This is the rounded integer value of the coordinates.
        """
        return int(round(self.x, 0)), int(round(self.y, 0))

    @property
    def hitbox(self):
        """
        Returns the object's hitbox as Pygame.rect object.
        """
        return pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 1)

    def update(self):
        """
        Updates the object. This includes Physics, collision, and mouse updates. 
        """
        if self.movable:
            self.check_collision()
        self.frame_delay = self.tick.tick
        if self.physics is True:
            self.physics_update()
        if 1 in pygame.mouse.get_pressed():
            if self.hitbox.collidepoint(pygame.mouse.get_pos()) and self.clicked is False:
                self.clicked = True
                self.on_click(pygame.mouse.get_pressed())
        else:
            self.clicked = False

    def update_draw(self):
        """
        Updates the object, then draws it to the screen. 
        """
        self.update()
        self.draw()

    def physics_update(self):
        """
        Update's the object's physics (provided the object is marked as a physics object) 
        """
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

    def draw_hitbox(self, color:tuple=None, thickness:int=1):
        """
        Draws the hitbox of the object to the screen (handy for debugging).
        """
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

    def check_collision(self, collision_action:bool=True):
        """
        Checks collision between this object, and the rest of the objects in the level 
        """
        collide = False
        for item in self.level:
            if item == self:
                continue
            if self.has_collided(item):
                if collision_action:
                    self.on_collision(item)
                    item.on_collision(self)
                if item.solid:
                    collide = True
        if self.physics is True:
            if collide is False:
                if self.fall_start is False:
                    self.fall_start = time()
            else:
                self.fall_start = False
        return collide

    def directional_move(self, x_change, y_change, check_collision=True):
        """
        Moves the object along a directional vector (use rotational_move to move along an angle vector)
        """
        x_change *= self.speed
        y_change *= self.speed
        self.last_x_change = x_change * self.frame_delay
        self.last_y_change = y_change * self.frame_delay
        self.x += self.last_x_change
        self.y += self.last_y_change

        if check_collision is True and self.movable:
            self.check_collision()

    def undo_last_move(self):
        """
        Undoes the object's last movement 
        """
        self.x -= self.last_x_change
        self.y -= self.last_y_change

    def rotational_move(self, distance, angle=None):
        """
        Moves the object a set distance at a specified angle (degrees)
        """
        if angle is None:
            angle = self.angle

        self.last_x_change = distance * degrees(cos(angle))
        self.last_y_change = distance * degrees(sin(angle))
        self.x = self.last_x_change
        self.y = self.last_y_change

    def has_collided(self, other:'ObjectBase'):
        """
        Check if this object has collided with the specified object 
        """
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

    def delete(self):
        """
        Deletes this object 
        """
        if self not in GlobalVariable.delete_queue:
            GlobalVariable.delete_queue.append(self)

    def __del__(self):
        self.delete()

    def jump(self, jump_velocity):
        """
        Causes the object to jump at the specified jump velocity 
        """
        if self.multi_jump is True:
            self.vertical_velocity = jump_velocity
        elif self.is_projectile is False:
            self.fall_start = time()
            self.vertical_velocity = jump_velocity

    def set_state(self, state:str):
        """
        Set the object's state 
        """
        self.state = state
        self.on_state_change(state)

    def reset_pos(self):
        """
        Set the object's position to the initial x and y 
        """
        self.x, self.y = self.initial_x, self.initial_y

    def set_level(self, name:str):
        """
        Set the selected level 
        """
        self.platformer.set_level(name)

    def on_state_change(self, new_state):
        pass

    def on_collision(self, other: 'ObjectBase'):
        pass

    def on_click(self, clicked: tuple):
        pass

from typing import List

from multimethods import multimethod
from pygame import Surface, display

from PyGE.Objects.Level import Level
from PyGE.Objects.Cache import add_image, add_spritesheet, add_font, get_image
from PyGE.Objects.ObjectBase import ObjectBase
from PyGE.utils import value_or_none, value_or_default
from PyGE.exceptions import UndefinedLevelException


class Platformer:
    def __init__(self, screen:'Surface', levels:dict, properties:dict):
        """
        This object is for the project. You should only ever need to create one instance of this class per project
        :param screen: the pygame surface to draw the level to
        :param levels: the dictionary of level names to their respective "Level" objects
        :param properties: the project properties. This should conatin things like the items to load into the cache
        """
        self.screen = screen
        self.levels = {}
        self.selected_level = None
        self.level_changed = True

        for name, src in value_or_default(properties, "images", {}).items():
            add_image(name, src)

        for name in value_or_default(properties, "spritesheets", {}):
            vals = properties["spritesheets"][name]
            add_spritesheet(
                name, vals["image"], vals["x_images"], vals["y_images"],
                changes_per_s=value_or_none(vals, "changesPerSecond"), duration=value_or_none(vals, "duration"),
                final_size=value_or_none(vals, "resize"), invisible_color=value_or_default(vals, "invisible", (0, 0, 0))
            )

        for name in value_or_default(properties, "font", {}):
            vals = properties["font"][name]
            add_font(name, vals["font"], vals["size"])

        for name, l in levels.items():
            self.levels[name] = Level(screen, l, self)

    def set_level(self, name:str):
        """
        Sets the currently selected level to the level specified
        :param name: the level name to set as the current level
        """
        if name not in self.levels:
            raise UndefinedLevelException("'{}' Is Not A Valid Level Name. Check Your Spelling, And Try Again.".format(name))
        self.selected_level = self.levels[name]
        self.level_changed = True

    def get_object(self, name:str):
        """
        Returns an object by the provided name. Will return the first object only.
        To select all by name, see the get_objects_by_name method
        :param name: the name of the object
        :return: the object with that name
        """
        return self.selected_level.objects[name]

    def get_objects_by_name(self, name:str):
        """
        Gets a list of every object with the specified name
        :param name: the name to select by
        :return: a list of objects with the specified name
        """
        objects = []
        for block in self.selected_level.level:
            if block.name == name:
                objects.append(block)
        return objects

    def get_objects_except_name(self, name:str):
        """
        Gets a list of every object which does not have a specified name
        :param name: the name to select by
        :return: a list of objects without the specified name
        """
        objects = []
        for block in self.selected_level.level:
            if block.name != name:
                objects.append(block)
        return objects

    def update(self):
        """
        Updates each object in the currently selected level 
        """
        self.selected_level.update()

    def draw(self):
        """
        Draws each object in the currently selected level 
        """
        self.selected_level.draw()

    def update_draw(self):
        """
        Updates, and draws each object in the currently selected level 
        """
        self.selected_level.update()
        self.selected_level.draw()

    def move_all(self, objects:List['ObjectBase'], x:int, y:int, check_collision:bool=True):
        """
        Moves all of the specified object directionaly
        :param objects: the list of objects to move
        :param x: the x change
        :param y: the y change
        :param check_collision: if the objects should check collision when they move (default is True) 
        """
        for b in objects:
            b.directional_move(x, y, check_collision=check_collision)

    def move_all_with_undo(self, objects:List['ObjectBase'], x:int, y:int, player:'ObjectBase'):
        """
        Moves all of the specified object directionaly, 
        and undoes the change if the objects collide with the specified object
        :param objects: the list of objects to move
        :param x: the x change
        :param y: the y change
        :param player: this is what each object should check with when moved
        """
        for thing in objects:
            thing.directional_move(x, y, check_collision=False)
        if player.check_collision(True):
            for thing in objects:
                thing.undo_last_move()

    def undo_last_move(self, objects:List['ObjectBase']=None):
        """
        Undoes the last movement of the list of objects
        :param objects: the list of objects to undo (if not specified, undo all object's last movement) 
        """
        if objects is None:
            objects = self.selected_level.level
        for block in objects:
            block.undo_last_move()

    def move_one_with_undo(self, thing:'ObjectBase', x:int, y:int):
        """
        Moves one object directionaly, and undoes if the object collides with anything
        :param thing: the object to move
        :param x: the x change
        :param y: the y change
        """
        thing.directional_move(x, y, check_collision=False)
        if thing.check_collision():
            thing.undo_last_move()

    def center_world_about(self, center:ObjectBase):
        """
        Centers the entire map arround the specified object
        :param center: the object to center the wold arround
        """
        screen_center = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        player_center = (center.w / 2, center.h / 2)
        new_player_pos = (screen_center[0] - player_center[0], screen_center[1] - player_center[1])

        delta = (new_player_pos[0] - center.x, new_player_pos[1] - center.y)

        for o in self.selected_level.level:
            o.x += delta[0]
            o.y += delta[1]

    @property
    def has_level_changed(self):
        """
        Returns True if the level has changed since the last call to this property 
        """
        if self.level_changed:
            self.level_changed = False
            return True
        return False

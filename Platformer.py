from typing import List
from pygame import Surface

from PyGE.Objects.Level import Level
from PyGE.Objects.Cache import add_image, add_spritesheet, add_font
from PyGE.Objects.ObjectBase import ObjectBase
from PyGE.utils import value_or_none, value_or_default
from PyGE.exceptions import UndefinedLevelException


class Platformer:
    def __init__(self, screen:'Surface', levels:dict, properties:dict):
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
        if name not in self.levels:
            raise UndefinedLevelException("'{}' Is Not A Valid Level Name. Check Your Spelling, And Try Again.".format(name))
        self.selected_level = self.levels[name]
        self.level_changed = True

    def get_object(self, name:str):
        return self.selected_level.objects[name]

    def get_object_by_name(self, name:str):
        objects = []
        for block in self.selected_level.level:
            if block.name == name:
                objects.append(block)
        return objects

    def get_objects_except_name(self, name:str):
        objects = []
        for block in self.selected_level.level:
            if block.name != name:
                objects.append(block)
        return objects

    def update(self):
        self.selected_level.update()

    def draw(self):
        self.selected_level.draw()

    def update_draw(self):
        self.selected_level.update()
        self.selected_level.draw()

    def move_all(self, objects:List['ObjectBase'], x:int, y:int, check_collision:bool=True):
        for b in objects:
            b.directional_move(x, y, check_collision=check_collision)

    def move_all_with_undo(self, objects:List['ObjectBase'], x:int, y:int, player:'ObjectBase'):
        for thing in objects:
            thing.directional_move(x, y, check_collision=False)
        if player.check_collision(True):
            for thing in objects:
                thing.undo_last_move()

    def undo_last_move(self, objects:List['ObjectBase']=None):
        if objects is None:
            objects = self.selected_level.level
        for block in objects:
            block.undo_last_move()

    def move_one_with_undo(self, thing:'ObjectBase', x:int, y:int):
        thing.directional_move(x, y, check_collision=False)
        if thing.check_collision():
            thing.undo_last_move()

    def center_world_about(self, center:ObjectBase):
        screen_center = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        player_center = (center.w / 2, center.h / 2)
        new_player_pos = (screen_center[0] - player_center[0], screen_center[1] - player_center[1])

        delta = (new_player_pos[0] - center.x, new_player_pos[1] - center.y)

        for o in self.selected_level.level:
            o.x += delta[0]
            o.y += delta[1]

    @property
    def has_level_changed(self):
        if self.level_changed:
            self.level_changed = False
            return True
        return False

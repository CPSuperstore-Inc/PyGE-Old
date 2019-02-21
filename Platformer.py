from PyGE.Objects.Level import Level
from PyGE.Objects.Cache import add_image, add_spritesheet, add_font
from PyGE.utils import value_or_none, value_or_default
from PyGE.exceptions import UndefinedLevelException


class Platformer:
    def __init__(self, screen, levels, properties):
        self.screen = screen
        self.levels = {}
        self.selected_level = None

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
            self.levels[name] = Level(screen, l)

    def set_level(self, name):
        if name not in self.levels:
            raise UndefinedLevelException("'{}' Is Not A Valid Level Name. Check Your Spelling, And Try Again.".format(name))
        self.selected_level = self.levels[name]

    def get_object(self, name):
        return self.selected_level.objects[name]

    def get_object_by_name(self, name):
        objects = []
        for block in self.selected_level.level:
            if block.name == name:
                objects.append(block)
        return objects

    def get_objects_except_name(self, name):
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

    def move_all(self, objects, x, y, check_collision=True):
        for b in objects:
            b.directional_move(x, y, check_collision=check_collision)

    def move_all_with_undo(self, objects, x, y, player, collision_action=True):
        self.move_all(objects, x, y)
        if player.check_collision(collision_action=collision_action):
            self.undo_last_move(objects)

    def undo_last_move(self, objects=None):
        if objects is None:
            objects = self.selected_level.level
        for block in objects:
            block.undo_last_move()

    def move_one_with_undo(self, thing, x, y):
        thing.directional_move(x, y, check_collision=False)
        if thing.check_collision(collision_action=False):
            thing.undo_last_move()

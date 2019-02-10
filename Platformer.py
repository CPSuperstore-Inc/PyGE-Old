from PyGE.Objects.Level import Level
from PyGE.Objects.Cache import add_image, add_spritesheet, add_font
from PyGE.utils import value_or_none


class Platformer:
    def __init__(self, screen, levels, properties):
        self.screen = screen
        self.levels = {}
        self.selected_level = None

        for name, src in properties["images"].items():
            add_image(name, src)

        for name in properties["spritesheets"]:
            vals = properties["spritesheets"][name]
            add_spritesheet(
                name, vals["image"], vals["x_images"], vals["y_images"],
                changes_per_s=value_or_none(vals, "changesPerSecond"), duration=value_or_none(vals, "duration")
            )

        for name in properties["font"]:
            vals = properties["font"][name]
            add_font(name, vals["font"], vals["size"])

        for name, l in levels.items():
            self.levels[name] = Level(screen, l)

    def set_level(self, name):
        self.selected_level = self.levels[name]

    def get_object(self, name):
        return self.selected_level.objects[name]

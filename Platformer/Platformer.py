from Objects.Level import Level
from Objects.Cache import add_image


class Platformer:
    def __init__(self, screen, levels, properties):
        self.screen = screen
        self.levels = {}
        self.selected_level = None

        for name, src in properties["images"].items():
            add_image(name, src)

        for name, l in levels.items():
            self.levels[name] = Level(screen, l)

    def set_level(self, name):
        self.selected_level = self.levels[name]

    def get_object(self, name):
        return self.selected_level.objects[name]

from Blocks import *
import GlobalVariable


class Level:
    def __init__(self, screen, level_data):
        self.screen = screen
        self.level_data = level_data
        self.level = []
        self.objects = {}
        self.properties = {}
        self.block_size = (16, 16)

        self.create_map()

    def create_map(self, level_data=None):
        if level_data is None:
            level_data = self.level_data

        self.__get_blocks(level_data)

    def __get_blocks(self, ld):
        blocks = ld["blocks"]
        level = ld["map"]
        self.properties = ld["properties"]

        if "import" in blocks:
            for b in blocks["import"]:
                blocks.update(b)

            del blocks["import"]

        if "import" in self.properties:
            for p in self.properties["import"]:
                self.properties.update(p)

            del self.properties["import"]

        x, y = (0, 0)
        for row in level:
            for col in row:
                data = blocks[col]
                props = data.copy()
                del props["model"]
                props["screen"] = self.screen
                props["x"] = x
                props["y"] = y
                props["w"], props["h"] = self.block_size
                props["level"] = self.level
                thing = eval(data["model"])(**props)
                self.level.append(thing)
                if thing.name is not None:
                    self.objects[thing.name] = thing

                x += self.block_size[0]
            x = 0
            y += self.block_size[1]

    def update(self):
        self.cleanup()
        for block in self.level:
            block.update()

    def draw(self):
        for block in self.level:
            block.draw()

    def cleanup(self):
        for obj in GlobalVariable.delete_queue:
            if obj in GlobalVariable.delete_queue:
                self.level.remove(obj)
            GlobalVariable.delete_queue.remove(obj)

    def move(self, objects, x, y):
        for o in objects:
            o.x += x
            o.y += y

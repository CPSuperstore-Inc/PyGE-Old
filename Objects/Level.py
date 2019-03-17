from typing import List

# noinspection PyUnresolvedReferences
from PyGE.Objects.Blocks import *

try:
    from blocks import *
except ImportError:
    print("No Custom Blocks Defined")

import PyGE.GlobalVariable as GlobalVariable
from PyGE.Objects.Cache import get_font
from ..utils import value_or_default
from PyGE.exceptions import UndefinedBlockException
from pygame import Surface


class Level:
    def __init__(self, screen:'Surface', level_data:dict, platformer):
        """
        This class is a level (or, one single map) in the game
        :param screen: The pygame surface to draw the level to
        :param level_data: A dictionary containing all of the level data to render
        :param platformer: The instance of the Platformer class, which this level lives in
        """
        self.screen = screen
        self.level_data = level_data
        self.level = []
        self.objects = {}
        self.properties = {}
        self.text = []
        self.block_size = GlobalVariable.block_size
        self.platformer = platformer

        self.create_map()

    def create_map(self, level_data:dict=None):
        """
        Executes the creation of the level
        :param level_data: the dictionary of data to build the level with. If not specified, the initial level data will be used
        """
        if level_data is None:
            level_data = self.level_data

        self.__get_blocks(level_data)

    def __get_blocks(self, ld:dict):
        """
        Loads all of the level data into the level object
        :param ld: the data to load
        """

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

        if "text" in self.properties:
            for t in self.properties["text"]:
                font = get_font(t["font"])
                text = font.render(t['text'], value_or_default(t, "antialiasing", True), t['color'])
                self.text.append({"text": text, "x": t['x'], "y": t['y']})

        x, y = (0, 0)
        for row in level:
            for col in row:
                if col == 0 and 0 not in blocks:
                    x += self.block_size[0]
                    continue
                if col not in blocks:
                    raise UndefinedBlockException("Found Block ID: '{}' In The Map, Which Does Not Have A Definition In The 'Blocks' Section.".format(col))
                data = blocks[col]
                props = data.copy()
                del props["model"]
                props["screen"] = self.screen
                props["x"] = x
                props["y"] = y
                props["w"], props["h"] = self.block_size
                props["level"] = self.level
                props["platformer"] = self.platformer
                try:
                    thing = eval(data["model"])(**props)
                except NameError:
                    raise UndefinedBlockException("The Block Model '{}' Does Not Have Defined Class. Please Define It, And Try Again.".format(data["model"]))
                self.level.append(thing)
                if thing.name is not None:
                    self.objects[thing.name] = thing

                x += self.block_size[0]
            x = 0
            y += self.block_size[1]

    def update(self):
        """
        Updates each object in the level, as well as runs the garbage collector
        """
        self.cleanup()
        for block in self.level:
            block.update()

    def draw(self):
        """
        Draws each object in the level to the Pygame surface
        This includes blocks, and text
        """
        for block in self.level:
            block.draw()

        for t in self.text:
            self.screen.blit(t['text'], (t['x'], t['y']))

    def cleanup(self):
        """
        Deletes any objects which are queued for deletion
        """
        for obj in GlobalVariable.delete_queue:
            if obj in GlobalVariable.delete_queue:
                self.level.remove(obj)
            GlobalVariable.delete_queue.remove(obj)

    @staticmethod
    def move(objects: List['ObjectBase'], x:int, y:int):
        """
        Performs a directional movement on all of the objects
        :param objects: the list of objects to move
        :param x: the x change for each object
        :param y: the y object for each object
        """
        for o in objects:
            o.x += x
            o.y += y

    def reset_level(self):
        """
        Reset the position of each object in the level 
        """
        for l in self.level:
            l.reset_pos()

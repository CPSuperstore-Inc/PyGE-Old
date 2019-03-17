class NotInCacheException(Exception):
    """
    The exception thrown when the user attempts to access a resource from the cache, which does not exist
    """
    pass


class DisplayMethodNotDefinedException(Exception):
    """
    The exception thrown when a block has no specified displauy method (ex. no color, image, or sprite sheet)  
    """
    pass


class MissingMandatoryArguementException(Exception):
    """
    The exception thrown when the user attempts to access an item from a dict, which does not exist
    """
    pass


class UndefinedBlockException(Exception):
    """
    The exception thrown when the user attempts to use a block (either in the "map" section, or "blocks" section), which is not defined
    """
    pass


class UndefinedLevelException(Exception):
    """
    The exception thrown when the user attempts to switch to a level, which was not defined in the Platformer levels dictionary
    """
    pass
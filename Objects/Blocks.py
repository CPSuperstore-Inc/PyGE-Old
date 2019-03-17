from PyGE.Objects.ObjectBase import ObjectBase


class Block(ObjectBase):
    def __init__(self, **kwargs):
        """
        A generic block which can be used in any level
        :param kwargs: a dictionary of configurations (do not instantiate this class yourself)
        """
        ObjectBase.__init__(self, **kwargs)


class Player(ObjectBase):
    """
    A player block, which can be used in any level
    :param kwargs: a dictionary of configurations (do not instantiate this class yourself)
    """
    def __init__(self, **kwargs):
        ObjectBase.__init__(self, **kwargs)

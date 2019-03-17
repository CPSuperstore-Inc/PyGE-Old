from multimethods import multimethod
from pygame import Surface, display

from PyGE.Objects.Cache import get_image
from PyGE.exceptions import MissingMandatoryArguementException


def value_or_none(dic, key):
    """
    Returns the value of the key in the dictionary, or None if not in the dict
    :param dic: the dictionary to check
    :param key: the key to check
    :return: The value, or None
    """
    if key in dic:
        return dic[key]
    return None


def value_or_default(dic, key, default):
    """
    Returns the value of the key in the dictionary, or the default value if not in the dict
    :param dic: the dictionary to check
    :param key: the key to check
    :param default: the default value to return
    :return: the value, or the default value
    """
    if key in dic:
        return dic[key]
    return default


def get_mandatory_value(dic, key):
    """
    Returns the value of the key in the dictionary, or raises the MissingMandatoryArguementException
    :param dic: the dictionary to check
    :param key: the key to check
    :return: The value
    """
    if key in dic:
        return dic[key]
    raise MissingMandatoryArguementException("The Key '{}' Was Expected, But Not Defined".format(key))


def set_caption(caption: str):
    """
    Sets the main window's caption
    :param caption: the text to set
    """
    display.set_caption(caption)


@multimethod(Surface)
def set_icon(icon):
    """
    Sets the window icon from a Pygame Surface
    :param icon: the Surface
    """
    display.set_icon(icon)


@multimethod(str)
def set_icon(icon):
    """
    Sets the window icon from path, or image in the cache (checks cache first)
    :param icon: the name
    """
    display.set_icon(get_image(icon))

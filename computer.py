import win32api

settings = win32api.EnumDisplaySettings(win32api.EnumDisplayDevices().DeviceName, -1)

USER_REFRESH_RATE = settings.DisplayFrequency
USER_MONITOR_WIDTH = win32api.GetSystemMetrics(0)
USER_MONITOR_HEIGHT = win32api.GetSystemMetrics(1)


def get_refresh_rate():
    """
    :return: The refresh rate of the user's monitor 
    """
    return USER_REFRESH_RATE


def get_monitor_width():
    """
    :return: The width of the user's monitor
    """
    return USER_MONITOR_WIDTH


def get_monitor_height():
    """
    :return: The height of the user's monitor
    """
    return USER_MONITOR_HEIGHT


def get_monitor_size():
    """
    :return: The size of the user's monitor as a tuple (width x height)
    """
    return USER_MONITOR_WIDTH, USER_MONITOR_HEIGHT

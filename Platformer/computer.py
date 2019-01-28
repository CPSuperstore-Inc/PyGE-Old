import win32api

settings = win32api.EnumDisplaySettings(win32api.EnumDisplayDevices().DeviceName, -1)

USER_REFRESH_RATE = settings.DisplayFrequency
USER_MONITOR_WIDTH = win32api.GetSystemMetrics(0)
USER_MONITOR_HEIGHT = win32api.GetSystemMetrics(1)

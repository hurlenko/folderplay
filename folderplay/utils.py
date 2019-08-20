import os
import platform
import sys


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def is_os_64bit():
    return platform.machine().endswith("64")


def is_linux():
    return sys.platform == "linux" or sys.platform == "linux2"


def is_macos():
    return sys.platform == "darwin"


def is_windows():
    return sys.platform == "win32"


def get_registry_value(key, path, value_name):
    import winreg

    try:
        key = {
            "HKCU": winreg.HKEY_CURRENT_USER,
            "HKLM": winreg.HKEY_LOCAL_MACHINE,
        }[key]
        access = winreg.KEY_READ
        if is_os_64bit():
            access |= winreg.KEY_WOW64_64KEY

        hkey = winreg.OpenKey(key, path, 0, access)
        val, _ = winreg.QueryValueEx(hkey, value_name)
        winreg.CloseKey(hkey)
    except FileNotFoundError:
        return None
    else:
        return val

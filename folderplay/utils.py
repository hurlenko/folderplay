import ctypes
import os
import platform
import sys
from pathlib import Path

from PyQt5.QtWidgets import QMessageBox

WIN_PATH_PREFIX = "\\\\?\\"
WIN_MAX_PATH = 259


def resource_path(relative_path):
    path = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    return os.path.join(path, "assets", relative_path)


def is_os_64bit():
    return platform.machine().endswith("64")


def is_linux():
    return sys.platform in ("linux", "linux2")


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


def message_box(title, text, icon, buttons):
    import folderplay.gui.icons as icons

    msg = QMessageBox()
    msg.setWindowIcon(icons.main_icon())
    msg.setIcon(icon)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.setStandardButtons(buttons)
    return msg.exec_()


def format_size(num, suffix="B"):
    try:
        num = float(num)
    except (ValueError, TypeError):
        num = 0
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)


def format_duration(seconds):
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return "%dd %dh %dm %ds" % (days, hours, minutes, seconds)
    elif hours > 0:
        return "%dh %dm %ds" % (hours, minutes, seconds)
    elif minutes > 0:
        return "%dm %ds" % (minutes, seconds)
    else:
        return "%ds" % (seconds,)


if is_windows():
    from ctypes import wintypes

    _GetShortPathNameW = ctypes.windll.kernel32.GetShortPathNameW
    _GetShortPathNameW.argtypes = [
        wintypes.LPCWSTR,
        wintypes.LPWSTR,
        wintypes.DWORD,
    ]
    _GetShortPathNameW.restype = wintypes.DWORD


def win_short_path(long_name: Path) -> str:
    """
    Gets the short path name of a given long path.
    http://stackoverflow.com/a/23598461/200291
    """
    path = str(long_name)
    if not is_windows() or not len(path) > WIN_MAX_PATH:
        return path

    output_buf_size = 0
    while True:
        output_buf = ctypes.create_unicode_buffer(output_buf_size)
        needed = _GetShortPathNameW(path, output_buf, output_buf_size)
        if output_buf_size >= needed:
            path = output_buf.value
            break
        else:
            output_buf_size = needed
    if path.startswith(WIN_PATH_PREFIX):
        path = path[len(WIN_PATH_PREFIX) :]
    return path


def normpath(path: Path) -> Path:
    if is_windows() and len(str(path)) > WIN_MAX_PATH:
        return Path(WIN_PATH_PREFIX + str(path))
    return path

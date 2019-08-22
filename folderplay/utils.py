import datetime
import os
import platform
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


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
    msg = QMessageBox()
    msg.setWindowIcon(QIcon(resource_path("assets/icons/icon.ico")))
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
    return str(datetime.timedelta(seconds=seconds))

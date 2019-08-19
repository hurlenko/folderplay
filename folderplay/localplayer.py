import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox

from folderplay.constants import LOCAL_PLAYER_MEDIA_ARG
from folderplay.media import MediaItem
from folderplay.utils import is_os_64bit


class LocalPlayer(QThread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player_path = None
        self.args = None
        self.media = None

        self.find_local_player()
        if not self.is_found():
            self.not_found_warning()

    def command(self):
        command = [str(self.player_path)]
        media_path = str(self.media.path)
        args = self.args
        if args:
            if LOCAL_PLAYER_MEDIA_ARG in args:
                args.replace(LOCAL_PLAYER_MEDIA_ARG, media_path)
            args = shlex.split(args)
        else:
            args = [media_path]
        command.extend(args)
        return command

    def set_media(self, media: MediaItem):
        self.media = media

    def run(self):
        subprocess.run(self.command())

    def _darwin_players(self):
        return []

    def _linux_players(self):
        players = ["vlc", "totem"]
        res = []
        for p in players:
            bin_path = shutil.which(p)
            if bin_path:
                res.append(bin_path)
        return res

    def _windows_players(self):
        res = []
        import winreg

        try:
            access = winreg.KEY_READ
            if is_os_64bit():
                access |= winreg.KEY_WOW64_64KEY

            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"HKLM\Software\VideoLAN\VLC",
                0,
                access,
            )
            val, _ = winreg.QueryValueEx(key, "InstallDir")
            winreg.CloseKey(key)
        except FileNotFoundError:
            pass
        else:
            if val:
                res.append(val)

        return res

    def is_found(self):
        return self.player_path and self.player_path.is_file()

    def name(self) -> str:
        if self.player_path:
            return self.player_path.stem
        return "N/A"

    def not_found_warning(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("No local players were found")
        msg.setInformativeText(
            "FolderPlay was unable to find any local players.\n"
            "You can configure your local player in the advanced view."
        )
        msg.setWindowTitle("Local player not found")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def find_local_player(self):
        players = []
        if sys.platform == "linux" or sys.platform == "linux2":
            players = self._linux_players()
        elif sys.platform == "darwin":
            players = self._darwin_players()
        elif sys.platform == "win32":
            players = self._windows_players()

        for p in players:
            p = Path(p.format(**os.environ))
            if p.is_file():
                self.player_path = p
                return

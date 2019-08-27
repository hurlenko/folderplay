import logging
import os
import shlex
import shutil
import subprocess
from pathlib import Path

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox

from folderplay.constants import LOCAL_PLAYER_MEDIA_ARG
from folderplay.media import MediaItem
from folderplay.utils import (
    get_registry_value,
    is_linux,
    is_macos,
    is_windows,
    message_box,
)

logger = logging.getLogger(__name__)


class LocalPlayer(QThread):
    def __init__(self, path: Path = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player_path = path
        self.args = None
        self.media = None

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
        logger.info("Player command line: {}".format(command))
        return command

    def set_media(self, media: MediaItem):
        logger.info("Setting media: {}".format(media))
        self.media = media

    def set_player(self, path: str):
        logger.info("Setting player: {}".format(path))
        self.player_path = Path(path)

    def run(self):
        subprocess.run(self.command())

    def _darwin_players(self):
        players = [
            "/Applications/VLC.app/Contents/MacOS/VLC",
            "/Applications/QuickTime Player.app/Contents/MacOS/QuickTime Player",
        ]
        return players

    def _linux_players(self):
        players = ["vlc", "totem"]
        res = []
        for p in players:
            bin_path = shutil.which(p)
            if bin_path:
                logger.info("Found linux player: {}".format(bin_path))
                res.append(bin_path)
        return res

    def _windows_players(self):
        res = []

        locations = [
            ("HKLM", r"Software\VideoLAN\VLC", None),
            ("HKCU", r"Software\MPC-HC\MPC-HC", "ExePath"),
        ]
        for l in locations:
            player = get_registry_value(*l)
            if player:
                logger.info("Found windows player: {}".format(player))
                res.append(player)
        return res

    def is_found(self):
        return self.player_path and self.player_path.is_file()

    def name(self) -> str:
        if self.player_path:
            return self.player_path.stem
        return "N/A"

    def not_found_warning(self):
        message_box(
            title="Local player not found",
            text=(
                "FolderPlay was unable to find any local players.\n"
                "You can configure your local player in the advanced view."
            ),
            icon=QMessageBox.Warning,
            buttons=QMessageBox.Ok,
        )

    def find_local_player(self):
        players = []
        if is_linux():
            players = self._linux_players()
        elif is_macos():
            players = self._darwin_players()
        elif is_windows():
            players = self._windows_players()

        for p in players:
            p = Path(p.format(**os.environ))
            if p.is_file():
                logger.info("Setting player to: {}".format(p))
                self.player_path = p
                return

    def __repr__(self):
        return "<LocalPLayer {}, {}>".format(self.player_path, self.media)

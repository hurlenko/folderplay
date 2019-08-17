import datetime
import logging
from pathlib import Path

import vlc
from PyQt5.QtWidgets import QStyle

from constants import WATCHED_PREFIX
from gui import ListWidgetItem

logger = logging.getLogger(__name__)


class MediaItem(ListWidgetItem):
    vlc_instance = vlc.Instance()

    def __init__(self, path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = path
        self.media = None

        self.setup_info()

    def setup_info(self):
        self.media: vlc.Media = self.vlc_instance.media_new(str(self.path))
        self.media.parse()

        self.title.setText(self.get_title())
        duration = datetime.timedelta(
            seconds=int(self.media.get_duration() / 1000)
        )
        self.duration.setText(str(duration))
        icon = QStyle.SP_DialogNoButton
        if self.is_watched():
            icon = QStyle.SP_DialogYesButton
        self.icon.setPixmap(self.style().standardPixmap(icon))

    def is_watched(self):
        return self.path.name.startswith(WATCHED_PREFIX)

    def toggle_watched(self):
        if self.is_watched():
            new_path = self.path.with_name(
                self.path.name[len(WATCHED_PREFIX) :]
            )
        else:
            new_path = self.path.with_name(WATCHED_PREFIX + self.path.name)

        if new_path.exists():
            logger.error("Cannot rename, file already exists %s", new_path)
            return
        try:
            self.path.rename(new_path)
        except Exception:
            logger.exception("Error while renaming %s", self.path)
        else:
            self.path = new_path
            self.setup_info()

    def get_title(self):
        title = self.media.get_meta(0)
        if self.is_watched():
            return title[len(WATCHED_PREFIX) :]
        return title

    def __repr__(self):
        return f'<MediaItem "{self.get_title()}" {self.is_watched()}>'

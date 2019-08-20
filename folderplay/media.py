import logging
from pathlib import Path

from PyQt5.QtGui import QIcon

from folderplay.constants import WATCHED_PREFIX
from folderplay.gui import ListWidgetItem
from folderplay.utils import resource_path

logger = logging.getLogger(__name__)


class MediaItem(ListWidgetItem):
    def __init__(self, path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = path
        # self.media = None
        self.icon_unwatched = QIcon(
            resource_path("assets/icons/check_box_blank.svg")
        )
        self.icon_watched = QIcon(resource_path("assets/icons/check_box.svg"))

        self.setup_info()

    def setup_info(self):
        self.title.setText(self.get_title())
        # duration = datetime.timedelta(
        #     seconds=int(self.media.get_duration() / 1000)
        # )
        duration = 0
        self.duration.setText(str(duration))
        icon = self.icon_unwatched
        if self.is_watched():
            icon = self.icon_watched
        # QIcon("filepath.svg").pixmap(QSize())
        self.icon.setPixmap(icon.pixmap(44, 44))

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
        title = self.path.name
        if self.is_watched():
            return title[len(WATCHED_PREFIX) :]
        return title

    def __lt__(self, other):
        return self.path.__lt__(other.path)

    def __repr__(self):
        return f'<MediaItem "{self.get_title()}" {self.is_watched()}>'

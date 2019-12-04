import datetime
import logging
from pathlib import Path

from pymediainfo import MediaInfo

from folderplay.constants import WATCHED_PREFIX
from folderplay.gui.icons import IconSet
from folderplay.gui.listwidget import ListWidgetItem
from folderplay.utils import format_size, format_duration, win_short_path

logger = logging.getLogger(__name__)


class MediaItem(ListWidgetItem):
    def __init__(self, path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = path
        self._title_override = None
        self.icon_unwatched = IconSet.current.check_box_blank
        self.icon_watched = IconSet.current.check_box
        self.size = None
        self.duration = None
        self.width = None
        self.height = None
        # self.parse_media_info()
        self.setup_info()

    def parse_media_info(self):
        try:
            media_info = MediaInfo.parse(win_short_path(self.path))
        except Exception as e:
            logger.exception(e)
            return
        for track in media_info.tracks:
            if track.track_type == "Video":
                self.duration = int(float(track.duration)) // 1000
                self.width = track.width
                self.height = track.height
            elif track.track_type == "General":
                self.size = track.file_size

    def get_short_info(self):
        res = []
        if self.duration is not None:
            now = datetime.datetime.now()
            finishes = now + datetime.timedelta(seconds=self.duration)
            res.append(
                "{}/{}".format(
                    format_duration(self.duration), finishes.strftime("%H:%M")
                )
            )
        if self.size is not None:
            res.append(format_size(self.size))
        if all((self.width, self.height)):
            res.append("{}x{}".format(self.width, self.height))
        return ", ".join(res)

    def setup_info(self):
        self.title.setText(self.get_title())
        icon = self.icon_unwatched
        if self.is_watched():
            icon = self.icon_watched
        self.icon.setPixmap(icon.pixmap(30, 30))

    def is_watched(self):
        return self.path.name.startswith(WATCHED_PREFIX)

    def toggle_watched(self):
        if self.is_watched():
            new_path = self.path.with_name(
                self.path.name[len(WATCHED_PREFIX):]
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

    def set_watched(self):
        if not self.is_watched():
            self.toggle_watched()

    def set_unwatched(self):
        if self.is_watched():
            self.toggle_watched()

    def get_title(self) -> str:
        if self._title_override:
            return self._title_override
        title = self.path.name
        if self.is_watched():
            return title[len(WATCHED_PREFIX):]
        return title

    def set_title(self, title: str):
        self._title_override = title
        self.title.setText(self.get_title())

    def __lt__(self, other):
        return self.get_title().__lt__(other.get_title())

    def __repr__(self):
        return '<MediaItem "{}" ({})>'.format(
            self.get_title(), "watched" and self.is_watched() or "unwatched"
        )

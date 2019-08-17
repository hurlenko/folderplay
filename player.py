import logging
import re
from pathlib import Path

import vlc
from PyQt5.QtWidgets import QListWidgetItem, QMenu, QStyle, QAbstractItemView

from constants import EXTENSIONS_MEDIA
from gui import MainWindow
from media import MediaItem

logger = logging.getLogger(__name__)


class Player(MainWindow):
    def __init__(self, media_dir: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.media_dir = Path(media_dir)
        # Create a basic vlc instance
        self.instance = vlc.Instance()

        # Create an empty vlc media player
        self.mediaplayer = vlc.MediaPlayer()
        self.filters = [self.hide_regex_not_match, self.hide_watched]

        # self.media_event = self.mediaplayer.event_manager()
        # self.media_event.event_attach(
        #     vlc.EventType.MediaPlayerEndReached, self.SongFinished, 1
        # )
        # self.media_event.event_attach(
        #     vlc.EventType.MediaPlayerMediaChanged, self.nextItemSet, 1
        # )
        #
        # logging.getLogger("vlc").setLevel(logging.NOTSET)
        # logging.getLogger("mpgatofixed32").setLevel(logging.NOTSET)
        # logging.getLogger("core vout").setLevel(logging.NOTSET)

        self.btnPlay.pressed.connect(self.play)
        self.chkHideWatched.stateChanged.connect(self.filter_medias)
        self.chkRegex.stateChanged.connect(self.filter_medias)
        self.searchBox.textEdited.connect(self.filter_medias)
        self.btnRefresh.pressed.connect(self.load_media)
        self.lstFiles.customContextMenuRequested.connect(
            self.media_context_menu
        )

        self.load_media()

    def filter_medias(self):
        total = self.lstFiles.count()
        for i in range(total):
            item = self.lstFiles.item(i)

            media: MediaItem = self.lstFiles.itemWidget(item)
            hidden = False
            for f in self.filters:
                if f(media) is True:
                    hidden = True
                    break
            item.setHidden(hidden)
        self.init_unwatched()

    def hide_watched(self, media: MediaItem) -> bool:
        return self.chkHideWatched.isChecked() and media.is_watched()

    def hide_regex_not_match(self, media: MediaItem) -> bool:
        pattern = self.searchBox.text()
        if not self.chkRegex.isChecked():
            pattern = re.escape(pattern)
        try:
            pattern = re.compile(pattern, re.IGNORECASE)
        except re.error as e:
            logger.warning("Failed to compile regex: %s", e)
            # Failed pattern should not hide the whole list of medias
            return False

        found = bool(pattern.search(media.get_title()))
        return not found

    def media_context_menu(self, position):
        # // Create menu and insert some actions
        menu = QMenu()
        menu.addAction(
            self.style().standardIcon(QStyle.SP_ArrowRight),
            "Toggle watched",
            self.toggle_media_status,
        )
        menu.exec_(self.lstFiles.mapToGlobal(position))

    def toggle_media_status(self):
        for item in self.lstFiles.selectedItems():
            media: MediaItem = self.lstFiles.itemWidget(item)
            media.toggle_watched()
        self.filter_medias()

    def load_media(self):
        # https://stackoverflow.com/a/25188862/8014793
        self.lstFiles.clear()
        medias = []
        for f in self.media_dir.rglob("*"):
            if f.suffix in EXTENSIONS_MEDIA:
                medias.append(MediaItem(f))
        medias.sort()
        for m in medias:
            item = QListWidgetItem(self.lstFiles)
            # Set size hint
            item.setSizeHint(m.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.lstFiles.addItem(item)
            self.lstFiles.setItemWidget(item, m)
        self.filter_medias()

    def init_unwatched(self):
        self.lstFiles.clearSelection()
        total = self.lstFiles.count()
        watched = 0
        for i in range(total):
            item = self.lstFiles.item(i)
            media: MediaItem = self.lstFiles.itemWidget(item)
            if media.is_watched():
                watched += 1
            elif len(self.lstFiles.selectedItems()) == 0:
                # self.lstFiles.setCurrentItem(item)
                item.setSelected(True)
                self.lstFiles.scrollToItem(
                    item, QAbstractItemView.PositionAtCenter
                )

        self.progressBar.setMaximum(total)
        self.progressBar.setValue(watched)
        self.progressBar.setToolTip(f"{total - watched} left to watch")

    def disable_widgets(self):
        for w in self.basic_view_widgets + self.advanced_view_widgets:
            w.setDisabled(True)

    def play(self):
        self.init_unwatched()
        selected = self.lstFiles.selectedItems()
        if len(selected) == 0:
            return

        item = self.lstFiles.itemWidget(selected[0])
        self.mediaplayer.set_media(item.media)
        self.disable_widgets()
        self.mediaplayer.play()

from pathlib import Path

import vlc
from PyQt5.QtWidgets import QListWidgetItem, QMenu, QStyle

from constants import EXTENSIONS_MEDIA
from gui import MainWindow
from media import MediaItem


class Player(MainWindow):
    def __init__(self, media_dir: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.media_dir = Path(media_dir)
        # Create a basic vlc instance
        self.instance = vlc.Instance()

        # Create an empty vlc media player
        self.mediaplayer = vlc.MediaPlayer()

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
        self.chkHideWatched.stateChanged.connect(self.hide_watched)
        self.btnRefresh.pressed.connect(self.load_media)
        self.lstFiles.customContextMenuRequested.connect(
            self.media_context_menu
        )

        self.load_media()

    def hide_watched(self):
        total = self.lstFiles.count()
        for i in range(total):
            item = self.lstFiles.item(i)

            media: MediaItem = self.lstFiles.itemWidget(item)
            item.setHidden(
                self.chkHideWatched.isChecked() and media.is_watched()
            )

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
        self.init_unwatched()

    def load_media(self):
        # https://stackoverflow.com/a/25188862/8014793
        self.lstFiles.clear()
        for f in self.media_dir.rglob("*"):
            if f.suffix in EXTENSIONS_MEDIA:
                media = MediaItem(f)
                item = QListWidgetItem(self.lstFiles)
                # Set size hint
                item.setSizeHint(media.sizeHint())
                # Add QListWidgetItem into QListWidget
                self.lstFiles.addItem(item)
                self.lstFiles.setItemWidget(item, media)
        self.hide_watched()
        self.init_unwatched()

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

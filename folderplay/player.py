import logging
import re
from pathlib import Path

from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QListWidgetItem,
    QMenu,
    QAbstractItemView,
    QDialog,
    QMessageBox,
)

from folderplay.constants import EXTENSIONS_MEDIA
from folderplay.gui import MainWindow
from folderplay.localplayer import LocalPlayer
from folderplay.media import MediaItem
from folderplay.utils import resource_path

logger = logging.getLogger(__name__)


class Player(MainWindow):
    def __init__(self, media_dir: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.media_dir = Path(media_dir)
        self.local_player = LocalPlayer()
        self.update_player_info()
        self.local_player.started.connect(self.playback_started)
        self.local_player.finished.connect(self.playback_finished)

        self.filters = [self.hide_regex_not_match, self.hide_watched]

        self.btnPlay.pressed.connect(self.play)
        self.btn_change_player.pressed.connect(self.select_new_player)
        self.chkHideWatched.stateChanged.connect(self.filter_medias)
        self.chkRegex.stateChanged.connect(self.filter_medias)
        self.searchBox.textEdited.connect(self.filter_medias)
        self.btnRefresh.pressed.connect(self.load_media)
        self.lstFiles.customContextMenuRequested.connect(
            self.media_context_menu
        )

        self.load_media()

    def update_player_info(self):
        self.player_name_label.setText(self.local_player.name())

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
        menu = QMenu("Options")
        font = menu.font()
        font.setPointSize(10)
        menu.setFont(font)
        menu.addAction(
            QIcon(resource_path("assets/icons/swap.svg")),
            "Toggle watched",
            self.toggle_media_status,
        )
        menu.exec_(self.lstFiles.mapToGlobal(position))

    def select_new_player(self):
        if self.player_open_dialog.exec_() == QDialog.Accepted:
            files = self.player_open_dialog.selectedFiles()
            if len(files) > 0:
                file_path = files[0]
                file_info = QFileInfo(file_path)
                if not file_info or not file_info.isExecutable():
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("File must be an executable binary")
                    msg.setWindowTitle("Invalid file")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
                else:
                    self.local_player.set_player(file_path)
                    self.update_player_info()

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
                item.setSelected(True)
                self.lstFiles.scrollToItem(
                    item, QAbstractItemView.PositionAtCenter
                )

        self.progressBar.setMaximum(total)
        self.progressBar.setValue(watched)
        self.progressBar.setToolTip(f"{total - watched} left to watch")

    def playback_started(self):
        for w in self.basic_view_widgets + self.advanced_view_widgets:
            w.setDisabled(True)

    def playback_finished(self):
        for w in self.basic_view_widgets + self.advanced_view_widgets:
            w.setEnabled(True)
        self.local_player.media.toggle_watched()
        self.filter_medias()

    def get_first_unwatched(self):
        total = self.lstFiles.count()
        for i in range(total):
            item = self.lstFiles.item(i)
            media: MediaItem = self.lstFiles.itemWidget(item)
            if media.is_watched():
                return media
        return None

    def play(self):
        media = self.get_first_unwatched()
        if not media:
            return

        if self.local_player.is_found():
            self.local_player.set_media(media)
            self.local_player.start()
        else:
            self.local_player.not_found_warning()

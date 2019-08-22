import datetime
import logging
import re
from pathlib import Path

import click
from PyQt5.QtCore import QFileInfo, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QListWidgetItem,
    QMenu,
    QAbstractItemView,
    QDialog,
    QMessageBox,
    QAction,
    QApplication,
)

from folderplay import __version__ as about
from folderplay.constants import (
    EXTENSIONS_MEDIA,
    SettingsKeys,
    NOT_AVAILABLE,
    FINISHED,
)
from folderplay.gui import MainWindow
from folderplay.localplayer import LocalPlayer
from folderplay.media import MediaItem
from folderplay.utils import resource_path, message_box

logger = logging.getLogger(__name__)


class Player(MainWindow):
    def __init__(self, media_dir: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.media_dir = Path(media_dir)
        self.settings = QSettings(
            self.media_dir.joinpath(
                f"{about.__title__}.{about.__version__}.ini"
            ).as_posix(),
            QSettings.IniFormat,
        )
        self.local_player = LocalPlayer()

        self.local_player.started.connect(self.playback_started)
        self.local_player.finished.connect(self.playback_finished)

        self.filters = [self.hide_regex_not_match, self.hide_watched]

        self.btnPlay.pressed.connect(self.play_button_pressed)
        self.btn_change_player.pressed.connect(self.select_new_player)
        self.chkHideWatched.stateChanged.connect(self.filter_medias)
        self.chkRegex.stateChanged.connect(self.filter_medias)
        self.searchBox.textEdited.connect(self.filter_medias)
        self.btnRefresh.pressed.connect(self.load_media)
        self.lstFiles.customContextMenuRequested.connect(
            self.media_context_menu
        )
        self.load_media()
        self.read_settings()

    def read_settings(self):
        local_player_path = self.settings.value(SettingsKeys.PLAYER_PATH)
        if local_player_path:
            self.local_player.set_player(local_player_path)
        else:
            self.local_player.find_local_player()
        if not self.local_player.is_found():
            self.local_player.not_found_warning()

        self.chkHideWatched.setChecked(
            self.settings.value(SettingsKeys.HIDE_WATCHED, False, type=bool)
        )
        is_advanced = self.settings.value(
            SettingsKeys.ADVANCED, False, type=bool
        )
        if is_advanced:
            self.btnAdvanced.click()
        self.update_player_info()

    def closeEvent(self, event):
        if self.local_player.is_found():
            self.settings.setValue(
                SettingsKeys.PLAYER_PATH, str(self.local_player.player_path)
            )
        self.settings.setValue(
            SettingsKeys.HIDE_WATCHED, self.chkHideWatched.isChecked()
        )
        self.settings.setValue(
            SettingsKeys.ADVANCED, self.btnAdvanced.isChecked()
        )
        return super().closeEvent(event)

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
        # Create menu and insert some actions
        menu = QMenu("Options")
        font = menu.font()
        font.setPointSize(10)
        menu.setFont(font)
        menu_item = self.lstFiles.itemAt(position)
        menu_media = self.lstFiles.itemWidget(menu_item)

        mark_watched = QAction(
            QIcon(resource_path("assets/icons/visibility.svg")),
            "Mark watched",
            self,
        )
        mark_watched.triggered.connect(
            lambda: self.set_media_watch_status(True)
        )

        mark_unwatched = QAction(
            QIcon(resource_path("assets/icons/visibility_off.svg")),
            "Mark unwatched",
            self,
        )
        mark_unwatched.triggered.connect(
            lambda: self.set_media_watch_status(False)
        )

        delete = QAction(
            QIcon(resource_path("assets/icons/delete_forever.svg")),
            "Delete from filesystem",
            self,
        )
        delete.triggered.connect(self.delete_media_from_filesystem)

        reveal_on_filesystem = QAction(
            QIcon(resource_path("assets/icons/folder.svg")),
            "Reveal on filesystem",
            self,
        )
        reveal_on_filesystem.triggered.connect(self.reveal_on_filesystem)

        play = QAction(
            QIcon(resource_path("assets/icons/play_circle.svg")), "Play", self
        )
        play.triggered.connect(lambda: self.play_selected_item(menu_media))

        copy_path = QAction(
            QIcon(resource_path("assets/icons/copy.svg")), "Copy path", self
        )
        copy_path.triggered.connect(lambda: self.copy_item_path(menu_media))

        menu.addSection(f"Selected: {len(self.lstFiles.selectedItems())}")
        menu.addAction(play)
        menu.addAction(mark_watched)
        menu.addAction(mark_unwatched)
        menu.addAction(reveal_on_filesystem)
        menu.addAction(copy_path)
        menu.addAction(delete)
        menu.exec_(self.lstFiles.mapToGlobal(position))

    def select_new_player(self):
        if self.player_open_dialog.exec_() == QDialog.Accepted:
            files = self.player_open_dialog.selectedFiles()
            if len(files) > 0:
                file_path = files[0]
                file_info = QFileInfo(file_path)
                if not file_info or not file_info.isExecutable():
                    message_box(
                        title="Invalid file",
                        text="File must be an executable binary",
                        icon=QMessageBox.Warning,
                        buttons=QMessageBox.Ok,
                    )
                else:
                    self.local_player.set_player(file_path)
                    self.update_player_info()

    def set_media_watch_status(self, set_watched: bool):
        for item in self.lstFiles.selectedItems():
            media: MediaItem = self.lstFiles.itemWidget(item)
            if set_watched:
                media.set_watched()
            else:
                media.set_unwatched()
        self.filter_medias()

    def delete_media_from_filesystem(self):
        medias = self.lstFiles.selectedItems()
        lines = []
        for i, item in enumerate(medias, 1):
            m = self.lstFiles.itemWidget(item)
            lines.append(f"  {i}. {m.get_title()}")
        msg = "\n".join(lines)
        status = message_box(
            title="Confirm deletion",
            text=f"You are about to delete {len(medias)} files\n\n{msg}",
            icon=QMessageBox.Warning,
            buttons=QMessageBox.Ok | QMessageBox.Cancel,
        )
        if status == QMessageBox.Ok:
            for item in medias:
                media: MediaItem = self.lstFiles.itemWidget(item)
                try:
                    media.path.unlink()
                except OSError:
                    logger.error(f"Unable to delete file {media.path}")
                self.lstFiles.takeItem(self.lstFiles.row(item))

            self.filter_medias()

    def reveal_on_filesystem(self):
        medias = self.lstFiles.selectedItems()
        for item in medias:
            media: MediaItem = self.lstFiles.itemWidget(item)
            click.launch(str(media.path), locate=True)

    def play_selected_item(self, media: MediaItem):
        self.play_media(media)

    def copy_item_path(self, media: MediaItem):
        cb = QApplication.clipboard()
        cb.setText(str(media.path))

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
        self.grp_current_media.setTitle(FINISHED)
        self.lbl_movie_info.setText(NOT_AVAILABLE)
        self.lbl_finishes.setText(NOT_AVAILABLE)

        total = self.lstFiles.count()
        watched = 0
        for i in range(total):
            item = self.lstFiles.item(i)
            media: MediaItem = self.lstFiles.itemWidget(item)
            if media.is_watched():
                watched += 1
            elif len(self.lstFiles.selectedItems()) == 0:
                item.setSelected(True)
                media.parse_media_info()
                self.lbl_movie_info.setText(media.get_short_info())
                self.grp_current_media.setTitle(media.get_title()[:30])
                if media.duration is not None:
                    now = datetime.datetime.now()
                    finishes = now + datetime.timedelta(seconds=media.duration)
                    finishes = finishes.strftime("%H:%M:%S")
                else:
                    finishes = "N/A"
                self.lbl_finishes.setText(finishes)

                self.lstFiles.scrollToItem(
                    item, QAbstractItemView.PositionAtCenter
                )
        self.progressBar.setMaximum(total)
        self.progressBar.setValue(watched)
        self.progressBar.setToolTip(f"{total - watched} left to watch")
        self.lstFiles.setFocus()

    def playback_started(self):
        for w in self.basic_view_widgets + self.advanced_view_widgets:
            w.setDisabled(True)

    def playback_finished(self):
        for w in self.basic_view_widgets + self.advanced_view_widgets:
            w.setEnabled(True)
        self.local_player.media.set_watched()
        self.filter_medias()

    def get_first_unwatched(self):
        total = self.lstFiles.count()
        for i in range(total):
            item = self.lstFiles.item(i)
            media: MediaItem = self.lstFiles.itemWidget(item)
            if not media.is_watched():
                return media
        return None

    def play_media(self, media: MediaItem):
        if self.local_player.is_found():
            self.local_player.set_media(media)
            self.local_player.start()
        else:
            self.local_player.not_found_warning()

    def play_button_pressed(self):
        media = self.get_first_unwatched()
        if not media:
            return
        self.play_media(media)

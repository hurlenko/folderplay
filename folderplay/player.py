import datetime
import logging
import re

import click
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import (
    QListWidgetItem,
    QMenu,
    QDialog,
    QMessageBox,
    QAction,
    QApplication,
    QAbstractItemView,
)

from folderplay.constants import (
    EXTENSIONS_MEDIA,
    SettingsKeys,
    NOT_AVAILABLE,
    FINISHED,
)
from folderplay.gui.icons import IconSet
from folderplay.gui.mainwindow import MainWindow
from folderplay.localplayer import LocalPlayer
from folderplay.media import MediaItem
from folderplay.utils import message_box, normpath, format_duration, format_size

logger = logging.getLogger(__name__)


class Player(MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.local_player = LocalPlayer()

        self.local_player.started.connect(self.playback_started)
        self.local_player.finished.connect(self.playback_finished)

        self.filters = [self.hide_regex_not_match, self.hide_watched]

        self.basic_view_widget.btn_play.pressed.connect(
            self.play_button_pressed
        )
        self.settings_widget.btn_change_player.pressed.connect(
            self.select_new_player
        )
        self.settings_widget.chk_hide_watched.stateChanged.connect(
            self.filter_media
        )
        self.settings_widget.chk_regex.stateChanged.connect(self.filter_media)
        self.settings_widget.txt_search_box.textEdited.connect(
            self.filter_media
        )
        self.basic_view_widget.btn_refresh.pressed.connect(self.load_media)
        self.lst_media.customContextMenuRequested.connect(
            self.media_context_menu
        )
        self.lst_media.doubleClicked.connect(self.play_selected_item)

        self.act_mark_watched = None
        self.act_mark_watched_next = None
        self.act_mark_unwatched = None
        self.act_mark_unwatched_previous = None
        self.act_delete = None
        self.act_reveal_on_filesystem = None
        self.act_play = None
        self.act_copy_path = None
        self.act_refresh = None

    def init(self):
        self.setup_actions()
        self.load_media()
        self.read_settings()

    def setup_actions(self):
        # Mark watched action
        self.act_mark_watched = QAction(
            IconSet.current.visibility, "Mark watched", self
        )
        self.act_mark_watched.triggered.connect(
            lambda: self.set_media_watch_status(True)
        )
        self.act_mark_watched.setShortcut("Space")
        self.act_mark_watched.setShortcutVisibleInContextMenu(True)
        self.addAction(self.act_mark_watched)

        # Mark Unwatched action
        self.act_mark_unwatched = QAction(
            IconSet.current.visibility_off, "Mark unwatched", self
        )
        self.act_mark_unwatched.triggered.connect(
            lambda: self.set_media_watch_status(False)
        )
        self.act_mark_unwatched.setShortcut("Shift+Space")
        self.act_mark_unwatched.setShortcutVisibleInContextMenu(True)
        self.addAction(self.act_mark_unwatched)

        self.act_delete = QAction(
            IconSet.current.delete_forever, "Delete from filesystem", self
        )
        self.act_delete.triggered.connect(self.delete_media_from_filesystem)
        self.act_delete.setShortcut("Del")
        self.act_delete.setShortcutVisibleInContextMenu(True)
        self.addAction(self.act_delete)

        self.act_reveal_on_filesystem = QAction(
            IconSet.current.folder, "Reveal on filesystem", self
        )
        self.act_reveal_on_filesystem.triggered.connect(
            self.reveal_on_filesystem
        )
        self.act_reveal_on_filesystem.setShortcut("O")
        self.act_reveal_on_filesystem.setShortcutVisibleInContextMenu(True)
        self.addAction(self.act_reveal_on_filesystem)

        self.act_play = QAction(IconSet.current.play_circle, "Play", self)
        self.act_play.triggered.connect(self.play_selected_item)
        self.act_play.setShortcut("Return")
        self.act_play.setShortcutVisibleInContextMenu(True)
        self.addAction(self.act_play)

        self.act_copy_path = QAction(IconSet.current.copy, "Copy path", self)
        self.act_copy_path.triggered.connect(self.copy_item_path)
        self.act_copy_path.setShortcut("Ctrl+C")
        self.act_copy_path.setShortcutVisibleInContextMenu(True)

        self.act_refresh = QAction(IconSet.current.refresh, "Refresh", self)
        self.act_refresh.triggered.connect(self.load_media)
        self.act_refresh.setShortcut("R")
        self.act_refresh.setShortcutVisibleInContextMenu(True)
        self.addAction(self.act_refresh)

        self.act_mark_unwatched_previous = QAction(
            IconSet.current.visibility, "Mark unwatched previous", self
        )
        self.act_mark_unwatched_previous.triggered.connect(
            self.mark_unwatched_previous
        )
        self.act_mark_unwatched_previous.setShortcut("Ctrl+Z")
        self.addAction(self.act_mark_unwatched_previous)

        self.act_mark_watched_next = QAction(
            IconSet.current.visibility_off, "Mark watched next", self
        )
        self.act_mark_watched_next.triggered.connect(self.mark_watched_next)
        self.act_mark_watched_next.setShortcut("Ctrl+Shift+Z")
        self.act_mark_watched_next.setShortcutVisibleInContextMenu(True)
        self.addAction(self.act_mark_watched_next)

    def read_settings(self):
        logger.info("Loading settings")
        local_player_path = self.settings.value(SettingsKeys.PLAYER_PATH)
        if not self.local_player.is_found() and local_player_path:
            self.local_player.set_player(local_player_path)
            logger.info(
                "Using player from config: {}".format(local_player_path)
            )
        else:
            logger.info("Searching for player")
            self.local_player.find_local_player()

        if not self.local_player.is_found():
            logger.warning("Host player not found")
            self.local_player.not_found_warning()

        self.settings_widget.chk_hide_watched.setChecked(
            self.settings.value(SettingsKeys.HIDE_WATCHED, False, type=bool)
        )
        is_advanced = self.settings.value(
            SettingsKeys.ADVANCED, False, type=bool
        )
        if is_advanced:
            logger.info("Switching to advanced view")
            self.basic_view_widget.btn_advanced.click()
        else:
            self.reset()
        self.update_player_info()

    def closeEvent(self, event):
        if self.local_player.is_found():
            logger.info(
                "Saving player info: {}".format(self.local_player.player_path)
            )
            self.settings.setValue(
                SettingsKeys.PLAYER_PATH, str(self.local_player.player_path)
            )
        self.settings.setValue(
            SettingsKeys.HIDE_WATCHED,
            self.settings_widget.chk_hide_watched.isChecked(),
        )
        self.settings.setValue(
            SettingsKeys.ADVANCED,
            self.basic_view_widget.btn_advanced.isChecked(),
        )
        return super().closeEvent(event)

    def update_player_info(self):
        self.settings_widget.lbl_player_name.setText(self.local_player.name())

    def filter_media(self):
        total = self.lst_media.count()
        items_hidden = 0
        logger.info("Filtering {} medias".format(total))

        for i in range(total):
            item = self.lst_media.item(i)

            media = self.lst_media.itemWidget(item)
            is_hidden = False
            for f in self.filters:
                if f(media) is True:
                    is_hidden = True
                    items_hidden += 1
                    break
            item.setHidden(is_hidden)
        logger.info("{} items were hidden".format(items_hidden))
        self.init_unwatched()

    def hide_watched(self, media: MediaItem) -> bool:
        return (
            self.settings_widget.chk_hide_watched.isChecked()
            and media.is_watched()
        )

    def hide_regex_not_match(self, media: MediaItem) -> bool:
        pattern = self.settings_widget.txt_search_box.text()
        if not self.settings_widget.chk_regex.isChecked():
            pattern = re.escape(pattern)
        try:
            pattern = re.compile(pattern, re.IGNORECASE)
        except re.error:
            # Failed pattern should not hide the whole list of medias
            return False

        found = bool(pattern.search(media.get_title()))
        return not found

    def media_context_menu(self, position):
        # Create menu and insert some actions
        menu = QMenu("Options")
        logger.info("Creating context menu")
        menu.addSection(
            "Selected: {}".format(len(self.lst_media.selectedItems()))
        )
        menu.addAction(self.act_play)
        menu.addAction(self.act_mark_watched)
        menu.addAction(self.act_mark_unwatched)
        menu.addAction(self.act_refresh)
        menu.addAction(self.act_reveal_on_filesystem)
        menu.addAction(self.act_copy_path)
        menu.addAction(self.act_delete)
        menu.exec_(self.lst_media.mapToGlobal(position))

    def select_new_player(self):
        logger.info("Selecting new player")
        if self.settings_widget.dlg_select_player.exec_() == QDialog.Accepted:
            files = self.settings_widget.dlg_select_player.selectedFiles()
            if len(files) > 0:
                file_path = files[0]
                file_info = QFileInfo(file_path)
                if not file_info or not file_info.isExecutable():
                    logger.error("Bad file selected: {}".format(file_path))
                    message_box(
                        title="Invalid file",
                        text="File must be an executable binary",
                        icon=QMessageBox.Warning,
                        buttons=QMessageBox.Ok,
                    )
                else:
                    logger.info("Selected file: {}".format(file_path))
                    self.local_player.set_player(file_path)
                    self.update_player_info()

    def set_media_watch_status(self, set_watched: bool):
        logger.info("Updating media status to {}".format(set_watched))

        for item in self.lst_media.selectedItems():
            media = self.lst_media.itemWidget(item)
            if set_watched:
                media.set_watched()
            else:
                media.set_unwatched()
        self.filter_media()

    def mark_unwatched_previous(self):
        logger.info("Unwatching last watched")
        total = self.lst_media.count()

        for i in reversed(range(total)):
            item = self.lst_media.item(i)
            media = self.lst_media.itemWidget(item)
            if not item.isHidden() and media.is_watched():
                media.set_unwatched()
                break
        self.filter_media()

    def mark_watched_next(self):
        logger.info("Marking next media as watched")
        total = self.lst_media.count()
        for i in range(total):
            item = self.lst_media.item(i)
            media = self.lst_media.itemWidget(item)
            if not item.isHidden() and not media.is_watched():
                media.set_watched()
                break
        self.filter_media()

    def delete_media_from_filesystem(self):
        logger.info("Deleting medias")
        medias = self.lst_media.selectedItems()
        if not medias:
            return
        lines = []
        if len(medias) < 11:
            for i, item in enumerate(medias, 1):
                m = self.lst_media.itemWidget(item)
                lines.append("  {}. {}".format(i, m.get_title()))
        msg = "\n".join(lines)
        status = message_box(
            title="Confirm deletion",
            text="You are about to delete {} files\n\n{}".format(
                len(medias), msg
            ),
            icon=QMessageBox.Warning,
            buttons=QMessageBox.Ok | QMessageBox.Cancel,
        )
        logger.info("{} files to be deleted".format(len(medias)))
        if status == QMessageBox.Ok:
            for item in medias:
                media = self.lst_media.itemWidget(item)
                try:
                    media.path.unlink()
                except OSError:
                    logger.error("Unable to delete file {}".format(media.path))
                self.lst_media.takeItem(self.lst_media.row(item))

            self.filter_media()

    def reveal_on_filesystem(self):
        medias = self.lst_media.selectedItems()
        logger.info("Opening file location for {} files".format(medias))
        for item in medias:
            media = self.lst_media.itemWidget(item)
            click.launch(str(media.path), locate=True)

    def copy_item_path(self):
        logger.info("Getting media path")
        medias = self.lst_media.selectedItems()
        if medias:
            media = self.lst_media.itemWidget(medias[0])
            cb = QApplication.clipboard()
            cb.setText(str(media.path))
            logger.info("{} copied to the clipboard".format(media))

    def load_media(self):
        # https://stackoverflow.com/a/25188862/8014793
        self.lst_media.clear()
        medias = []
        logger.info("Loading media from filesystem: {}".format(self.media_dir))
        for f in self.media_dir.rglob("*"):
            f = normpath(f)
            if f.suffix.lower() in EXTENSIONS_MEDIA:
                medias.append(MediaItem(f))
        medias.sort()
        logger.info("{} medias found ".format(len(medias)))
        for m in medias:
            item = QListWidgetItem(self.lst_media)
            # Set size hint
            item.setSizeHint(m.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.lst_media.addItem(item)
            self.lst_media.setItemWidget(item, m)
        self.filter_media()
        self.highlight_first_unwatched()

    def highlight_first_unwatched(self):
        self.lst_media.clearSelection()

        total = self.lst_media.count()
        for i in range(total):
            item = self.lst_media.item(i)
            media = self.lst_media.itemWidget(item)
            if not media.is_watched():
                item.setSelected(True)
                self.lst_media.scrollToItem(
                    item, QAbstractItemView.PositionAtCenter
                )
                return

    def init_unwatched(self):
        self.basic_view_widget.grp_current_media.setTitle(FINISHED)
        self.basic_view_widget.lbl_movie_info_time.setText(NOT_AVAILABLE)
        self.basic_view_widget.lbl_movie_info_size.setText(NOT_AVAILABLE)
        self.basic_view_widget.lbl_movie_info_res.setText(NOT_AVAILABLE)

        total = self.lst_media.count()
        logger.info("Initializing {} media".format(total))
        watched = 0
        unwatched_initialized = False
        for i in range(total):
            item = self.lst_media.item(i)
            media = self.lst_media.itemWidget(item)
            if media.is_watched():
                watched += 1
            elif not unwatched_initialized:
                unwatched_initialized = True
                media.parse_media_info()
                logger.info("Setting current media to {}".format(media))
                if media.duration is not None:
                    now = datetime.datetime.now()
                    finishes = now + datetime.timedelta(seconds=media.duration)
                    self.basic_view_widget.lbl_movie_info_time.setText(
                        "{}/{}".format(
                            format_duration(media.duration),
                            finishes.strftime("%H:%M"),
                        )
                    )
                if media.size is not None:
                    self.basic_view_widget.lbl_movie_info_size.setText(
                        format_size(media.size)
                    )

                if all((media.width, media.height)):
                    self.basic_view_widget.lbl_movie_info_res.setText(
                        "{}x{}".format(media.width, media.height)
                    )
                self.basic_view_widget.grp_current_media.setTitle(
                    media.get_title()
                )

        logger.info("Medias watched {}".format(watched))
        self.basic_view_widget.pbr_watched.setMaximum(total)
        self.basic_view_widget.pbr_watched.setValue(watched)
        self.basic_view_widget.pbr_watched.setToolTip(
            "{} left to watch".format(total - watched)
        )

    def playback_started(self):
        logger.info("Disabling widgets")
        self.setDisabled(True)

    def playback_finished(self):
        logger.info("Enabling widgets")
        self.setEnabled(True)
        self.local_player.media.set_watched()
        self.filter_media()
        self.highlight_first_unwatched()

    def get_first_unwatched(self) -> MediaItem:
        logger.info("Getting first unwatched media")
        total = self.lst_media.count()
        for i in range(total):
            item = self.lst_media.item(i)
            media = self.lst_media.itemWidget(item)
            if not media.is_watched():
                logger.info("Found: {}".format(media))
                return media
        logger.warning("No unwatched media found")
        return None

    def play_selected_item(self):
        logger.info("Getting media")
        medias = self.lst_media.selectedItems()
        if medias:
            media = self.lst_media.itemWidget(medias[0])
            logger.info("Playing media {}".format(media))
            self.play_media(media)

    def play_media(self, media: MediaItem):
        if self.local_player.is_found():
            logger.warning("Player found, playing {}".format(media))
            self.local_player.set_media(media)
            self.local_player.start()
        else:
            logger.warning("Player not found")
            self.local_player.not_found_warning()

    def play_button_pressed(self):
        media = self.get_first_unwatched()
        if not media:
            return
        self.play_media(media)

import os
import sys

# from PyQt5 import Qt
import vlc
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from player import Player


def player_test():
    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new("extra/Nextcloud.mp4")
    # Media.get_mrl()
    player.set_media(Media)
    player.play()

    # player = vlc.MediaPlayer()
    # x = player.play()
    while True:
        pass


def main():
    QApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    # app.setStyle("Fusion")
    player = Player(os.getcwd())
    player.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
    # player_test()

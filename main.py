import os

from PyQt5.QtWidgets import QApplication

from player import Player

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    player = Player(os.getcwd())
    player.show()
    sys.exit(app.exec_())

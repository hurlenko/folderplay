from PyQt5.QtWidgets import QApplication

from gui.mainwindow import MainWindow

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())

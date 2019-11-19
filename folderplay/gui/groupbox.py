from PyQt5.QtWidgets import QGroupBox


class NoTitleGroupBox(QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("QGroupBox{ padding-top: 0; margin-top: 0 }")

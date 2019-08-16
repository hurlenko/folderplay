from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QProgressBar,
    QVBoxLayout,
    QSizePolicy,
    QApplication,
    QHBoxLayout,
    QStyle,
    QLineEdit,
    QCheckBox,
    QWidget,
    QAbstractItemView,
    QListWidget,
)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Play button
        self.btnPlay = QPushButton()
        self.setup_play_button()

        # Advanced view button
        self.btnAdvanced = QPushButton()
        self.setup_advanced_button()

        self.btnReload = QPushButton()
        self.setup_reload_button()

        # Progressbar
        self.progressBar = QProgressBar()
        self.setup_progress_bar()

        # File names list view
        self.lstFiles = QListWidget()
        self.setup_files_list()

        # Search box
        self.searchBox = QLineEdit()
        self.setup_search_line_edit()

        self.chkShowWatched = QCheckBox()
        self.setup_show_watched_checkbox()

        self.chkRegex = QCheckBox()
        self.setup_regex_checkbox()

        self.advanced_view_size = QSize(1600, 400)
        self.basic_view_size = QSize(600, 250)

        self.basic_view_widgets = [
            self.btnPlay,
            self.btnAdvanced,
            self.btnReload,
            self.progressBar,
        ]

        self.advanced_view_widgets = [
            self.lstFiles,
            self.searchBox,
            self.chkShowWatched,
            self.chkShowWatched,
            self.chkRegex,
        ]

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main window
        self.setup_main_window()

    def basic_view_layout(self):
        vlayout = QVBoxLayout()
        vlayout_reload_advanced = QVBoxLayout()

        hlayout = QHBoxLayout()

        widgets = [self.btnAdvanced, self.btnReload]

        for w in widgets:
            vlayout_reload_advanced.addWidget(w)

        hlayout.addWidget(self.progressBar, 3)
        hlayout.addLayout(vlayout_reload_advanced)

        # Button is two times bigger than progressbar
        vlayout.addLayout(hlayout, 1)
        vlayout.addWidget(self.btnPlay, 2)
        return vlayout

    def advanced_view_layout(self):
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout_checkboxes = QHBoxLayout()

        basic_layout = self.basic_view_layout()

        checkboxes = [self.chkShowWatched, self.chkRegex]

        for w in checkboxes:
            hlayout_checkboxes.addWidget(w)

        vlayout.addLayout(basic_layout)
        vlayout.addLayout(hlayout_checkboxes)

        vlayout.addWidget(self.searchBox)

        hlayout.addLayout(vlayout, 1)
        hlayout.addWidget(self.lstFiles, 2)

        return hlayout

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos()
        )
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def toggle_advanced_view(self):
        if self.size() == self.basic_view_size:
            for w in self.advanced_view_widgets:
                w.show()
            self.setFixedSize(self.advanced_view_size)
        else:
            for w in self.advanced_view_widgets:
                w.hide()
            self.setFixedSize(self.advanced_view_size)
            self.setFixedSize(self.basic_view_size)
        self.center()

    # region Widget setup routine
    def setup_main_window(self):
        self.central_widget.setLayout(self.advanced_view_layout())
        self.setFixedSize(self.advanced_view_size)
        self.toggle_advanced_view()
        self.center()

        self.setWindowTitle("FolderPlay by Hurlenko")

    def setup_play_button(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.btnPlay.setSizePolicy(sizePolicy)
        self.btnPlay.setText("Play")

    def setup_advanced_button(self):
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.btnAdvanced.setSizePolicy(sizePolicy)
        self.btnAdvanced.setToolTip("Advanced options")
        # Icons
        # https://joekuan.files.wordpress.com/2015/09/screen3.png
        self.btnAdvanced.setIcon(
            self.style().standardIcon(QStyle.SP_ArrowRight)
        )
        self.btnAdvanced.clicked.connect(self.toggle_advanced_view)

    def setup_reload_button(self):
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.btnReload.setSizePolicy(sizePolicy)
        self.btnReload.setToolTip("Reload")
        # Icons
        # https://joekuan.files.wordpress.com/2015/09/screen3.png
        self.btnReload.setIcon(
            self.style().standardIcon(QStyle.SP_BrowserReload)
        )

    def setup_progress_bar(self):
        self.progressBar.setValue(24)
        # Allow progressbar to expand to take up all space in layout
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.progressBar.setSizePolicy(sizePolicy)

        self.progressBar.setFormat("%v / %m")
        self.progressBar.setToolTip("This is %m a tooltip message.")

    def setup_files_list(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lstFiles.setSizePolicy(sizePolicy)
        self.lstFiles.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.lstFiles.setSortingEnabled(True)

        # # Add dummy items
        # model = QStandardItemModel(self.lstFiles)
        #
        # foods = [
        #     "Cookie dough" * 20,  # Must be store-bought
        #     "Hummus",  # Must be homemade
        #     "Spaghetti",  # Must be saucy
        #     "Dal makhani",  # Must be spicy
        #     "Chocolate whipped cream",  # Must be plentiful
        # ]
        #
        # for food in foods * 10:
        #     # Create an item with a caption
        #     item = QStandardItem(
        #         self.style().standardIcon(QStyle.SP_DialogNoButton), food
        #     )
        #
        #     # Add the item to the model
        #     model.appendRow(item)
        # self.lstFiles.setModel(model)

    def setup_search_line_edit(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.searchBox.setSizePolicy(sizePolicy)
        self.searchBox.setPlaceholderText("Search...")

    def setup_regex_checkbox(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.chkRegex.setSizePolicy(sizePolicy)
        self.chkRegex.setText("Regex")

    def setup_show_watched_checkbox(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.chkShowWatched.setSizePolicy(sizePolicy)
        self.chkShowWatched.setText("Show Watched")

    # endregion Widget setup routine

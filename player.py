from pathlib import Path

import vlc

from constants import EXTENSIONS_MEDIA
from gui import MainWindow


class Player(MainWindow):
    def __init__(self, media_dir: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.media_dir = Path(media_dir)
        # Create a basic vlc instance
        self.instance = vlc.Instance()

        # Create an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        self.load_media()

    def load_media(self):
        # https://stackoverflow.com/a/25188862/8014793
        for f in self.media_dir.rglob("*"):
            if f.suffix in EXTENSIONS_MEDIA:
                self.lstFiles.addItem(str(f))

        # # medias.sort()
        # for m in medias:
        #     self.lstFiles

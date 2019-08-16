import logging
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

        self.load_media()

    def load_media(self):
        # https://stackoverflow.com/a/25188862/8014793
        for f in self.media_dir.rglob("*"):
            if f.suffix in EXTENSIONS_MEDIA:
                self.lstFiles.addItem(str(f))

    def play(self):
        x = self.lstFiles.item(1)
        media = self.instance.media_new(x.text())
        self.mediaplayer.set_media(media)
        # media.parse()
        self.mediaplayer.play()

        # player = vlc.MediaPlayer(x.text())
        # player.play()


    # @vlc.callbackmethod
    # def SongFinished(self, event, status):
    #     # print ('item finish : ', self.filelist[self.indicator].name)
    #     self.indicator += 1
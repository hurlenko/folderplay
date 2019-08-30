import inspect
import os
from abc import ABCMeta, abstractmethod
from pathlib import Path
from xml.etree import ElementTree as et

from PyQt5.QtCore import Qt, QPoint, QRect, QRectF
from PyQt5.QtGui import (
    QIcon,
    QColor,
    QIconEngine,
    QImage,
    qRgba,
    QPixmap,
    QPainter,
)
from PyQt5.QtSvg import QSvgRenderer

from folderplay.utils import resource_path


class SvgEngine(QIconEngine):
    def __init__(self, svg_content):
        super().__init__()
        self.data = svg_content

    def paint(self, painter, rect, mode, state):
        """ paint(self, QPainter, QRect, QIcon.Mode, QIcon.State) """
        renderer = QSvgRenderer(self.data)
        renderer.render(painter, QRectF(rect))

    def pixmap(self, size, mode, state):
        img = QImage(size, QImage.Format_ARGB32)
        img.fill(qRgba(0, 0, 0, 0))
        pix = QPixmap.fromImage(img, Qt.NoFormatConversion)
        painter = QPainter(pix)
        r = QRect(QPoint(0.0, 0.0), size)
        self.paint(painter, r, mode, state)
        return pix

    def clone(self):
        return SvgEngine(self.data)


class QIconMeta(type(QIcon), ABCMeta):
    # https://stackoverflow.com/a/28727066/8014793
    pass


class ColorfulSvgIcon(QIcon, metaclass=QIconMeta):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.path = Path(filename)

    @abstractmethod
    def setColor(self, color: QColor):
        pass


class MaterialIcon(ColorfulSvgIcon):
    def setColor(self, color: QColor):
        # Possible ways to change colors:
        # https://stackoverflow.com/a/33540671/8014793
        # https://stackoverflow.com/a/44757951/8014793

        tree = et.parse(self.path)
        root = tree.getroot()
        xmlns = root.tag.split("}")[0] + "}"
        for path in root.findall("{}path".format(xmlns)):
            if not path.get("fill"):
                path.set("fill", color.name())

        new_icon = QIcon(SvgEngine(et.tostring(root)))
        self.swap(new_icon)

        # fd, filename = tempfile.mkstemp()
        # os.close(fd)
        # try:
        #     tree.write(filename)
        #     icon = QIcon(filename)
        #     self.swap(icon)
        # finally:
        #     os.remove(filename)

        # with tempfile.NamedTemporaryFile() as fp:
        #     tree.write(fp)
        #     fp.close()
        #     icon = QIcon(fp.name)
        #     print(fp.name)
        #     print(fp.name)
        # self.swap(icon)


def icon(name):
    return property(lambda self: self.load_icon(name))


class GenericIconSet:
    def __init__(self, loader, directory):
        self.loader = loader
        self.directory = directory
        self.cache = {}

    def iter_icon_names(self):
        for (name, value) in inspect.getmembers(
            self.__class__, lambda v: isinstance(v, property)
        ):
            yield name

    def set_color(self, color: QColor):
        for icn in self.iter_icon_names():
            getattr(self, icn).setColor(color)

    def swap(self, other: "GenericIconSet"):
        for icn in self.iter_icon_names():
            this_icon = getattr(self, icn)
            other_icon = getattr(other, icn)
            this_icon.swap(other_icon)

    def load_icon(self, name):
        cached = self.cache.get(name)
        if cached:
            return cached
        new_icon = self.loader(
            resource_path(os.path.join("icons", self.directory, name))
        )
        self.cache[name] = new_icon
        return new_icon

    check_box = icon("check_box.svg")
    check_box_blank = icon("check_box_blank.svg")
    copy = icon("copy.svg")
    delete_forever = icon("delete_forever.svg")
    folder = icon("folder.svg")
    folder_open = icon("folder_open.svg")
    play = icon("play.svg")
    play_circle = icon("play_circle.svg")
    refresh = icon("refresh.svg")
    settings = icon("settings.svg")
    visibility = icon("visibility.svg")
    visibility_off = icon("visibility_off.svg")


class IconSets:
    MaterialIconSet = GenericIconSet(MaterialIcon, "material")
    __current = MaterialIconSet

    @classmethod
    def set_current(cls, iconset):
        if not isinstance(iconset, GenericIconSet):
            raise TypeError("Icon set must be of type GenericIconSet")
        cls.__current = iconset

    @classmethod
    def current(cls) -> "GenericIconSet":
        return cls.__current

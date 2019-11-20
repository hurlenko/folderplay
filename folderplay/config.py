import inspect
import json
import os
from pathlib import Path

from folderplay import __version__ as about
from gui.icons import IconSet
from gui.styles import Style


class Param:
    def __init__(self, name, default=None, type_=None):
        self.name = name
        self.default = default
        self.type = type_ or (lambda x: x)

    def __get__(self, instance: "Config", owner: "Config"):
        value = instance._overrides.get(self.name, self.default)
        return self.type(value)

    def __set__(self, instance: "Config", value):
        # Raises an exception if value is not json serializable
        json.dumps(value)
        instance._overrides[self.name] = value

    def __repr__(self):
        return "%s(%r)" % (self.name, self.default)


class Config:
    # cascade of option values:
    #
    #     default option values, overridden by
    #     config file options, overridden by
    #     environment variables, overridden by
    #     command-line options.
    def __init__(self, search_dir: str, cli_overrides: dict):
        self._path = Path(search_dir, about.__title__).with_suffix(".json")
        self._overrides = {}
        self._keys = {
            obj.name
            for _, obj in inspect.getmembers(
                self.__class__, lambda v: isinstance(v, Param)
            )
        }
        self._load_file()
        self._overrides.update(
            {k: v for k, v in cli_overrides.items() if k in self._keys and v}
        )

    def _load_file(self):
        if self._path.is_file():
            params = json.loads(self._path.read_text("utf-8"))
            if not isinstance(params, dict):
                raise ValueError("Invalid config file")
            unknown = params.keys() - self._keys
            if unknown:
                raise ValueError("Unknown keys: {}".format(", ".join(unknown)))
            self._overrides.update(params)

    def save(self):
        config = {}
        for member_name, member_object in inspect.getmembers(
            self.__class__, lambda v: isinstance(v, Param)
        ):
            config[member_object.name] = getattr(self, member_name)
        self._path.write_text(
            json.dumps(config, indent=4, sort_keys=True, ensure_ascii=False)
        )

    player = Param("player_path")
    hide_watched = Param("hide_watched", False)
    advanced = Param("advanced", False)
    style = Param("style", Style.light.name)
    iconset = Param("iconset", IconSet.material.name)
    workdir = Param("workdir", os.getcwd())

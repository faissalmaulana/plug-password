from pathlib import Path

from platformdirs import user_config_dir
from tomlkit import dumps, parse, table
from tomlkit.toml_document import TOMLDocument


class _ConfigApplication:
    def __init__(self, path_dir: Path):
        self.config_dir = path_dir
        self.config_file: Path | None = None
        self.__doc: TOMLDocument | None = None

    def setup_config_dir(self):
        """
        Create config directory and config file if missing.
        Does NOT write content.
        """
        if self.config_file is not None:
            raise FileExistsError

        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.config_file = self.config_dir / "config.toml"
        self.config_file.touch(exist_ok=True)

    def __write_defaults(self):
        """
        Write default TOML config (only for empty file).
        """

        doc = parse(
            """[sqlite_directory]\nlocation_path = "" # Path where the root directory of db located"""
        )

        if self.config_file is not None:
            self.config_file.write_text(dumps(doc), encoding="utf-8")

    def _ensure_loaded(self):
        """
        Ensure config exists, has content, and is loaded.
        """
        try:
            self.setup_config_dir()
        except FileExistsError:
            pass

        if self.config_file is not None:
            if self.config_file.stat().st_size == 0:
                self.__write_defaults()

            if self.__doc is None:
                self.__doc = parse(self.config_file.read_text(encoding="utf-8"))

    def __save(self):
        """
        Write TOML value To the config file.
        """
        if self.config_file is not None and self.__doc is not None:
            self.config_file.write_text(dumps(self.__doc), encoding="utf-8")

    def get_location(self) -> str:
        """
        Get path where the config is stored.
        """
        try:
            self.setup_config_dir()
        except FileExistsError:
            pass

        return str(self.config_dir)

    def get_value(self, key, table_name=None, default=None):
        """
        Get TOML value in the config else default.
        """
        self._ensure_loaded()

        if table_name:
            if self.__doc is not None:
                return self.__doc.get(table_name, {}).get(key, default)

        if self.__doc is not None:
            return self.__doc.get(key, default)

    def set_key_value(self, key, value, table_name=None):
        """
        Set a TOML value in the config.

        - key: config key
        - value: value to set (replaces existing or creates new)
        - table_name: optional TOML table name
        """

        self._ensure_loaded()

        if key == "" or table_name == "":
            raise Exception("key and table_name can't empty string")

        if self.__doc is None:
            raise RuntimeError("Document not loaded")

        if table_name:
            if table_name not in self.__doc:
                self.__doc[table_name] = table()

            self.__doc[table_name][key] = value  # type: ignore[index]
        else:
            self.__doc[key] = value

        self.__save()


config_app = _ConfigApplication(
    Path(user_config_dir("plug-password", "Faissal Maulana"))
)

__all__ = ["config_app"]

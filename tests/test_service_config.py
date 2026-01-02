import os
import unittest
from pathlib import Path

from internal.services.config.config import _ConfigApplication


class TestSetUpConfigCreateDir(unittest.TestCase):
    def setUp(self) -> None:
        tmpPath = Path("tests/.tmp")
        tmpPath.mkdir(parents=True, exist_ok=True)

        self.fakeHomeDirPath = tmpPath

    def test_success_setup_home_dir(self):
        """
        Success setup config dir.
        """
        configApp = _ConfigApplication(self.fakeHomeDirPath)
        expected = "tests/.tmp/config.toml"

        configApp.setup_config_dir()
        result = str(configApp.config_file)

        self.assertEqual(expected, result)

    def test_fail_setup_home_file_already_exists(self):
        """
        Fail setup config because the config file already exists.
        """

        configApp = _ConfigApplication(self.fakeHomeDirPath)

        configApp.setup_config_dir()

        with self.assertRaises(FileExistsError):
            configApp.setup_config_dir()

    def tearDown(self) -> None:
        # The directory must be empty first
        os.remove("tests/.tmp/config.toml")

        self.fakeHomeDirPath.rmdir()


class TestGetLocationConfig(unittest.TestCase):
    def setUp(self) -> None:
        tmpPath = Path("tests/.tmp")
        tmpPath.mkdir(parents=True, exist_ok=True)

        self.fakeHomeDirPath = tmpPath

    def test_success_get_home_config_path(self):
        """
        Success get path where the config file is stored.
        """

        configApp = _ConfigApplication(self.fakeHomeDirPath)
        expected = "tests/.tmp"

        result = configApp.get_location()
        self.assertEqual(expected, result)

    def tearDown(self) -> None:
        # The directory must be empty first
        os.remove("tests/.tmp/config.toml")

        self.fakeHomeDirPath.rmdir()


class TestGetTomlValue(unittest.TestCase):
    def setUp(self) -> None:
        tmpPath = Path("tests/.tmp")
        tmpPath.mkdir(parents=True, exist_ok=True)

        self.fakeHomeDirPath = tmpPath

    def test_success_get_value(self):
        """
        Success get TOML value.
        """
        configApp = _ConfigApplication(self.fakeHomeDirPath)
        # from default config
        expected = ""

        result = configApp.get_value("location_path", table_name="sqlite_directory")
        self.assertEqual(expected, result)

    def test_fail_get_value_not_found_key(self):
        """
        Fail get TOML value because key is not exists.
        """
        configApp = _ConfigApplication(self.fakeHomeDirPath)

        self.assertIsNone(configApp.get_value("something", default=None))

    def tearDown(self) -> None:
        # The directory must be empty first
        os.remove("tests/.tmp/config.toml")

        self.fakeHomeDirPath.rmdir()


class TestSettingTomlValue(unittest.TestCase):
    def setUp(self) -> None:
        tmpPath = Path("tests/.tmp")
        tmpPath.mkdir(parents=True, exist_ok=True)

        self.fakeHomeDirPath = tmpPath

    def test_success_set_key_value(self):
        """
        Success set TOML key-value.
        """
        configApp = _ConfigApplication(self.fakeHomeDirPath)
        expected = "Lizzy McAlpine"

        configApp.set_key_value("singer", "Lizzy McAlpine")

        self.assertEqual(expected, configApp.get_value("singer"))

    def test_success_set_key_value_with_table(self):
        """
        Success set TOML key-value to a table.
        """
        configApp = _ConfigApplication(self.fakeHomeDirPath)
        expected = "plug-password"

        configApp.set_key_value("name", "plug-password", "project")

        self.assertEqual(expected, configApp.get_value("name", "project"))

    def test_success_set_value_replace_existing(self):
        """
        Success set TOML key-value to existing key.
        """
        configApp = _ConfigApplication(self.fakeHomeDirPath)
        expected = ".tmp"

        configApp.set_key_value("location_path", ".tmp", "sqlite_directory")

        self.assertEqual(
            expected, configApp.get_value("location_path", "sqlite_directory")
        )

    def test_success_set_value_to_and_create_new_table(self):
        """
        Success set TOML key-value and create new table because the given table not exists.
        """
        configApp = _ConfigApplication(self.fakeHomeDirPath)
        expected = ".tmp"

        configApp.set_key_value("location_path", ".tmp", "server")

        self.assertEqual(expected, configApp.get_value("location_path", "server"))

    def test_fail_set_value_key_is_empty(self):
        """
        Fail set TOML key-value because the given key is empty string.
        """
        configApp = _ConfigApplication(self.fakeHomeDirPath)

        with self.assertRaises(Exception):
            configApp.set_key_value("", "")

    def test_fail_set_value_key_and_table_is_empty(self):
        """
        Fail set TOML key-value because the given key or table is empty string.
        """
        configApp = _ConfigApplication(self.fakeHomeDirPath)

        with self.assertRaises(Exception):
            configApp.set_key_value("", "", "")

    def tearDown(self) -> None:
        # The directory must be empty first
        os.remove("tests/.tmp/config.toml")

        self.fakeHomeDirPath.rmdir()


if __name__ == "__main__":
    unittest.main()

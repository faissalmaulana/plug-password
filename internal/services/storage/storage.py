from pathlib import Path

from internal.constants.constants import KEY_STORE_DIRECTORY, TABLE_STORE_DIRECTORY
from internal.repositories.sqlite.store import SqliteStore
from internal.repositories.store import Store
from internal.services.config.config import config_app


class Storage:
    def __init__(self, store: Store) -> None:
        self.__store = store

    def create(self):
        try:
            self.__store.create()
        except Exception as err:
            raise err

    def get_current_store(self) -> str:
        try:
            return self.__store.get_current_table()
        except Exception as err:
            raise err

    def get_all_snapshots(self) -> list[str]:
        try:
            return self.__store.get_all_tables()
        except Exception as err:
            raise err

    def switch_snapshot(self, snapshot_name: str):
        if snapshot_name == "":
            raise ValueError("snapshot name is required")

        try:
            self.__store.switch_table(snapshot_name)
        except Exception as err:
            raise err


storage_dir: str | None = config_app.get_value(
    KEY_STORE_DIRECTORY, table_name=TABLE_STORE_DIRECTORY
)

if storage_dir is None:
    storage_dir = ""

sqliteRepository = SqliteStore(Path(storage_dir))
store = Storage(sqliteRepository)

__all__ = ["store"]

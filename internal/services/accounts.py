import secrets
import sqlite3
import uuid

from internal.constants.constants import KEY_STORE_DIRECTORY, TABLE_STORE_DIRECTORY
from internal.services.config.config import config_app
from internal.services.storage.storage import sqlite_repository


class Account:
    def __init__(self) -> None:
        self.__storage: str = self.__get_store_path()

    def add_new_account(self, platform: str):
        name = self.__generate_account_name()

        try:
            sqlite_repository.backup_current_table(f"{name}_accounts")

            with sqlite3.connect(self.__storage + "/passwords.sqlite") as conn:
                cur = conn.cursor()
                account_id = str(uuid.uuid4())
                cur.execute(
                    "INSERT INTO accounts(id, platform) VALUES(?, ?)",
                    (account_id, platform),
                )

                conn.commit()
        except Exception as err:
            print(err)
            raise

    def __generate_account_name(self) -> str:
        return f"{secrets.token_hex(4)}"

    def __get_store_path(self) -> str:
        storage_dir: str | None = config_app.get_value(
            KEY_STORE_DIRECTORY, table_name=TABLE_STORE_DIRECTORY
        )

        if storage_dir is None:
            return ""

        return storage_dir

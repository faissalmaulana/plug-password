import sqlite3
from pathlib import Path

from internal.constants.constants import DEFAULT_STORAGE_NAME
from internal.repositories.store import Store


class SqliteStore(Store):
    def __init__(self, workdir_path: Path) -> None:
        self.__db_path = workdir_path / DEFAULT_STORAGE_NAME

    def create(self) -> bool:
        """
        Initialize new database and set default tables.

        - If DB exists AND both tables exist -> FileExistsError
        - If DB exists but tables are missing -> create missing tables
        - If DB does not exist -> create DB and tables
        """

        try:
            with sqlite3.connect(str(self.__db_path)) as conn:
                accounts_exists = self.__table_exists(conn, "accounts")
                active_exists = self.__table_exists(conn, "active_table")

                # DB file exists and both tables exist
                if self.__db_path.is_file() and accounts_exists and active_exists:
                    raise FileExistsError("Database and required tables already exist")

                # Create missing tables
                if not accounts_exists:
                    self.__create_account_table(conn)

                if not active_exists:
                    default_table = "accounts"
                    self.__create_and_insert_active_table(default_table, conn)

                return True

        except sqlite3.Error as err:
            raise err

    def get_current_table(self) -> str:
        try:
            with sqlite3.connect(str(self.__db_path)) as conn:
                cur = conn.cursor()
                cur.execute("SELECT table_name FROM active_table WHERE id = 1;")

                row = cur.fetchone()
                if row is None:
                    return ""
                return row[0]
        except sqlite3.Error as err:
            raise err

    def backup_current_table(self, table_name):
        try:
            with sqlite3.connect(str(self.__db_path)) as conn:
                cursor = conn.cursor()
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                cursor.execute(
                    f"CREATE TABLE {table_name} AS SELECT * FROM accounts WHERE 0"
                )
                cursor.execute(f"INSERT INTO {table_name} SELECT * FROM accounts")

                conn.commit()
        except sqlite3.Error as err:
            raise err

    def switch_table(self, table_name: str) -> None:
        """
        Switch active table to an existing table name.
        """

        try:
            with sqlite3.connect(str(self.__db_path)) as conn:
                cur = conn.cursor()

                # Check table exists
                cur.execute(
                    "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?;",
                    (table_name,),
                )

                if cur.fetchone() is None:
                    raise ValueError(f"Table '{table_name}' does not exist")

                self.__update_active_table(table_name, conn)

        except sqlite3.Error:
            raise

    def get_all_tables(self) -> list[str]:
        try:
            with sqlite3.connect(self.__db_path) as conn:
                cur = conn.cursor()
                cur.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table'
                AND name LIKE '%_accounts'
            """)

                return [row[0] for row in cur.fetchall()]

        except sqlite3.Error as err:
            raise err

    def __create_and_insert_active_table(
        self, def_table: str, conn: sqlite3.Connection
    ):
        try:
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS active_table (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    table_name TEXT NOT NULL
                );
            """)

            cur.execute(
                """
                INSERT INTO active_table (id, table_name)
                VALUES (1, ?)
                ON CONFLICT(id)
                DO UPDATE SET table_name = excluded.table_name;
            """,
                (def_table,),
            )

            conn.commit()

        except sqlite3.Error:
            raise

    def __update_active_table(
        self,
        table_name: str,
        conn: sqlite3.Connection,
    ):
        try:
            cur = conn.cursor()

            cur.execute(
                "UPDATE active_table SET table_name = ? WHERE id = 1;",
                (table_name),
            )

        except sqlite3.Error as err:
            raise err

    def __create_account_table(self, conn: sqlite3.Connection):
        try:
            with sqlite3.connect(str(self.__db_path)) as conn:
                cur = conn.cursor()
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS accounts(id TEXT NOT NULL PRIMARY KEY,platform TEXT NOT NULL);"
                )

        except sqlite3.Error as err:
            raise err

    def __table_exists(self, conn: sqlite3.Connection, table_name: str) -> bool:
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
            (table_name,),
        )
        return cursor.fetchone() is not None

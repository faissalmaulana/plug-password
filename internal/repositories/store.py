from abc import ABC, abstractmethod
from pathlib import Path


class Store(ABC):
    """Interface Store."""

    def __init__(self, workdir_path: Path) -> None:
        pass

    @abstractmethod
    def create(self) -> bool:
        """
        Initialize new database/storage and set default tables.

        Returns:
            bool: True if successful

        Raises:
            FileExistsError: If storage already exists with required tables
        """
        pass

    @abstractmethod
    def get_current_table(self) -> str:
        """
        Get the name of the currently active table.

        Returns:
            str: Current table name, empty string if not found
        """
        pass

    @abstractmethod
    def backup_current_table(self, table_name: str) -> None:
        """
        Backup the current accounts table to a new table with given name.

        Args:
            table_name: Name for the backup table
        """
        pass

    @abstractmethod
    def switch_table(self, table_name: str) -> None:
        """
        Switch active table to an existing table name.

        Args:
            table_name: Name of table to switch to

        Raises:
            ValueError: If table does not exist
        """
        pass

    @abstractmethod
    def get_all_tables(self) -> list[str]:
        """
        Get all tables.

        Returns:
            list[str]: List of table names
        """
        pass

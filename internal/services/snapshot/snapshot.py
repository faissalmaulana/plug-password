from datetime import datetime


class Snapshot:
    def __init__(self, prefix: str, date: datetime | None = None) -> None:
        self.__name_prefix = prefix
        self.__date_created = date

    def get_snapshot_formatted(self) -> str:
        """
        Get formatted snapshot version.
        It will joined the prefix and date created
        if date is None only formatted with prefix.
        """

        prefix = self.__name_prefix.strip().lower()

        if self.__date_created is None:
            return f"{prefix}.sqlite"

        formatted_date = self.__date_created.strftime("%m-%d-%Y_%H-%M")
        return f"{prefix}_{formatted_date}.sqlite"

from pathlib import Path
from typing import cast

from internal.constants.constants import DEFAULT_STORAGE_NAME
from internal.services.snapshot.snapshot import Snapshot


class Storage:
    def __init__(self) -> None:
        self.storage_dir: Path = cast(Path, None)
        self._active_storage: Path = cast(Path, None)

    def create_storage_workdir(self, storage_dir_path: Path):
        """
        Initialize storage workdir for the first time.
        """

        self.storage_dir = storage_dir_path
        self.active_storage = storage_dir_path / DEFAULT_STORAGE_NAME

        # Check if the root is exist
        if not self.storage_dir.is_dir():
            raise FileNotFoundError

        if self.is_workdir_initialized():
            raise Exception("storage workdir already exist")

        for subdir in (".tmp", "snapshots"):
            path = self.storage_dir / subdir
            path.mkdir(exist_ok=True)

    def is_workdir_initialized(self) -> bool:
        """
        Check whether storage workdir has been set up.
        """

        tmp_dir = self.storage_dir / ".tmp"
        snapshots_dir = self.storage_dir / "snapshots"

        return tmp_dir.is_dir() and snapshots_dir.is_dir()

    def get_active_storage(self) -> Path:
        return self.active_storage

    # Todo: create new snapshot to snapshots directory
    def save_snapshot(self, snapshot: Snapshot):
        pass


storage_app = Storage()

__all__ = ["storage_app"]

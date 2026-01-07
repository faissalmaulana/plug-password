import os
from pathlib import Path
from typing import Annotated

import typer

from internal.constants.constants import (
    KEY_STORE_DIRECTORY,
    TABLE_STORE_DIRECTORY,
)
from internal.services.config.config import config_app
from internal.services.storage import storage

app = typer.Typer(no_args_is_help=True, help="Manage Store of plug password")


def validate_set_path(path: str):
    if path == "":
        raise typer.BadParameter("path can't be empty string")
    return path


def set_path_directory(path: str):
    directory = Path(path).expanduser().resolve()

    # Create directory if it doesn't exist
    if not directory.exists():
        typer.confirm(f"Directory '{directory}' does not exist. Create it?", abort=True)
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

    if not directory.is_dir():
        raise typer.BadParameter(f"'{path}' exists but is not a directory")

    # Check if directory is writable
    if not os.access(directory, os.W_OK):
        raise typer.BadParameter(f"Directory '{directory}' is not writable")

    try:
        config_app.set_key_value(
            KEY_STORE_DIRECTORY, str(directory), TABLE_STORE_DIRECTORY
        )
        print(f"Successfully set store directory to: {directory}")
    except Exception as err:
        raise typer.BadParameter(str(err))


@app.command()
def set(path: Annotated[str, typer.Argument(callback=validate_set_path)]):
    """
    Set path where the storage want to stored.

    Examples:
        store set /home/user/data
        store set ~/Documents/myapp
        store set /mnt/usb/backup
    """

    try:
        set_path_directory(path)
    except (Exception, FileNotFoundError) as err:
        print("ERROR:", err)
        raise typer.Abort()


@app.command()
def init():
    """
    Initialize empty storage and create accounts table
    """

    storage_dir: str | None = config_app.get_value(
        KEY_STORE_DIRECTORY, table_name=TABLE_STORE_DIRECTORY
    )

    if storage_dir is None:
        while True:
            path: Path = typer.prompt(
                "Set path where the storage needs to be stored", type=Path
            )

            try:
                set_path_directory(str(path))
                # Update with the new set value
                storage_dir = config_app.get_value(
                    KEY_STORE_DIRECTORY, table_name=TABLE_STORE_DIRECTORY
                )

                break
            except (Exception, FileNotFoundError) as err:
                print("ERROR:", err)
                raise typer.Abort()

    try:
        if storage_dir is not None:
            storage.store.create()
            print("Initialized storage...")

    except (FileNotFoundError, FileExistsError, Exception) as err:
        if isinstance(err, FileNotFoundError):
            print("Storage directory is not found")
        elif isinstance(err, FileExistsError) or isinstance(err, Exception):
            print("Storage already initialized")


@app.command()
def status():
    """
    Display information about what is my current store
    """
    try:
        current_store = storage.store.get_current_store()
        print(f"On store {current_store}")
    except Exception as err:
        print(err)


@app.command()
def list():
    """
    Display all stores's snapshots
    """
    try:
        stores = storage.store.get_all_snapshots()
        current_store = storage.store.get_current_store()

        display = "Snapshots:\n"

        if len(stores) > 0:
            for store in stores:
                if store == current_store:
                    display += f"*{store}\n"
                    continue

                display += f"{store}\n"
        else:
            display += "There's no snapshot yet."

        print(display)
    except Exception as err:
        print(err)


@app.command()
def switch(
    snapshot: Annotated[str, typer.Argument()],
):
    """
    Switch current storage to available snapshot
    """

    try:
        storage.store.switch_snapshot(snapshot)
        print(f"Swich to {snapshot}")
    except Exception as err:
        print(err)
        raise


if __name__ == "__main__":
    app()

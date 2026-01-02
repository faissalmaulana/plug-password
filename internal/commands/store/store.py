import os
from pathlib import Path
from typing import Annotated

import typer

from internal.constants.constants import KEY_STORE_DIRECTORY, TABLE_STORE_DIRECTORY
from internal.services.config.config import config_app

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


if __name__ == "__main__":
    app()

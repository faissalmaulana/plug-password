from typing import Annotated

import typer

from internal.services.config.config import config_app

app = typer.Typer(no_args_is_help=True, help="Manage Plug Password configuration")


def validate_set_key_command(key: str):
    if key == "":
        raise typer.BadParameter("key can't be empty string")
    return key


def validate_set_value_command(value: str):
    if value == "":
        raise typer.BadParameter("value can't be empty string")

    return value


@app.command()
def set(
    key: Annotated[str, typer.Argument(callback=validate_set_key_command)],
    value: Annotated[str, typer.Argument(callback=validate_set_value_command)],
    table: Annotated[str, typer.Argument()] = "",
):
    """
    Set value to config file
    """

    try:
        config_app.set_key_value(key, value, table)
        print("success setting value to config file")
    except Exception as err:
        raise typer.BadParameter(str(err))


@app.command()
def get(
    key: Annotated[str, typer.Argument(callback=validate_set_key_command)],
    table: Annotated[str, typer.Argument()] = "",
):
    """
    Get value from config file
    """

    value = config_app.get_value(key, table_name=table)
    if value is None:
        print(f"value with key: {key.upper()} is not found or could be inside tables")
        raise typer.Exit()

    print(value)


@app.command()
def location():
    """
    Get the location where the config file is stored
    """

    value = config_app.get_location()
    if value == "":
        print("config location not found")
        raise typer.Exit()

    print(value)


if __name__ == "__main__":
    app()

from typing import Annotated

import typer

from internal.services.accounts import Account

app = typer.Typer(no_args_is_help=True, help="Manage Account password")


@app.command()
def add(
    platform: Annotated[str, typer.Argument()],
):
    """
    Add new account to storage
    """
    try:
        account = Account()
        account.add_new_account(platform)
        print("Succesfully add new account")
    except Exception as err:
        print(err)
        raise


if __name__ == "__main__":
    app()

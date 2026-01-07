import typer

from internal.commands import accounts
from internal.commands.config import config
from internal.commands.store import store

app = typer.Typer(
    no_args_is_help=True,
    help="Plug Password\n\n\nA tool for managing backup passwords securely with SQLite",
)

app.add_typer(config.app, name="config")
app.add_typer(store.app, name="store")
app.add_typer(accounts.app, name="account")


if __name__ == "__main__":
    app()

import typer

from internal.commands.config import config

app = typer.Typer(
    no_args_is_help=True,
    help="Plug Password\n\n\nA tool for managing backup passwords securely with SQLite",
)

app.add_typer(config.app, name="config")


if __name__ == "__main__":
    app()

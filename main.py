import typer

app = typer.Typer(
    no_args_is_help=True,
    help="Plug Password\n\n\nA tool for managing backup passwords securely with SQLite",
)


if __name__ == "__main__":
    app()

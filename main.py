import typer

app = typer.Typer(no_args_is_help=True)


@app.callback(invoke_without_command=True)
def callback():
    """
    Plug Password

    A tool for managing backup passwords securely using SQLite.
    """

    raise typer.Exit()


if __name__ == "__main__":
    app()

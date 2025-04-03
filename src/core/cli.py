import typer

app = typer.Typer()


@app.command()
def hello(name: str = "Luk") -> str:
    """Print a greeting with the provided name."""
    print(f"Hello {name}")  # noqa: T201
    return f"Hello {name}"

from pathlib import Path

import typer

from core.taxonomy_loader import load_taxonomy

app = typer.Typer()


@app.command("load-taxonomy")
def load_taxonomy_cli(
    path: Path = Path("data/taxonomy.json"), language: str = "en", *, show: bool = False
) -> None:
    """Load and display taxonomy terms in the selected language."""
    terms = load_taxonomy(path, language)
    typer.echo(f"✅ Loaded {len(terms)} terms from {path}")

    if show:
        typer.echo("🔎 First few terms:")
        for t in terms[:10]:
            typer.echo(f"- {t['id']}: {t['name']}")

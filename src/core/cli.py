from pathlib import Path

import typer

from core.embedder import Embedder
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


@app.command("match-taxonomy")
def match_taxonomy_cli(  # noqa: PLR0913
    text: str = typer.Option(..., help="Input text to match against taxonomy"),
    path: Path = Path("data/taxonomy.json"),
    language: str = "en",
    top_k: int = 5,
    domain: str = typer.Option(
        None,
        help="Optional taxonomy domain to filter on (e.g. 'theme', 'eventtype', ...)",
    ),
    *,
    with_prompt: bool = typer.Option(
        False,  # noqa: FBT003
        "--with-prompt",
        help="Include the suggested LLM prompt as output",
    ),
) -> None:
    """Match input text to the most similar taxonomy terms using embeddings."""
    terms = load_taxonomy(path, language)

    if domain:
        terms = [t for t in terms if t["domain"] == domain]
        typer.echo(f"🔍 Matching only within domain: '{domain}'")

    embedder = Embedder()
    matches = embedder.most_similar(text, terms, top_k=top_k)

    typer.echo(f"🔍 Input: {text}")
    typer.echo(f"🔝 Top {top_k} matches:\n")
    for match in matches:
        typer.echo(f"  - {match['name']} ({match['id']}) — score: {match['score']:.3f}")

    # LLM prompt
    # TODO(LukV):  # noqa: FIX002, TD003
    # Remove this when we have a proper LLM integration
    if with_prompt:
        llm_prompt = "You are a cultural data expert.\n\n"
        llm_prompt += f'Given this description:\n"{text}"\n\n'
        llm_prompt += "Match the most appropriate categories from the following taxonomy terms:\n\n"  # noqa: E501
        for match in matches:
            llm_prompt += f"- {match['id']}: {match['name']}\n"

        llm_prompt += (
            "\nReturn a list of the most relevant IDs, optionally explain your choices."
        )

        typer.echo("\n🧠 Suggested LLM Prompt:\n")
        typer.echo(llm_prompt)

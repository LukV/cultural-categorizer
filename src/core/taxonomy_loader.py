import json
from pathlib import Path
from typing import Any

from core.normalizer import normalize


def load_taxonomy(path: Path, language: str = "en") -> list[dict[str, Any]]:
    """Load taxonomy terms and flatten them to a list of {id, name}
    dicts in a given language.
    """
    with Path.open(path, encoding="utf-8") as f:
        raw = json.load(f)

    terms = []
    for term in raw.get("terms", []):
        try:
            name = term["name"][language]
            domain = term["domain"]
            label = f"{domain.capitalize()}: {name}"
            embedding_text = normalize(label)
            terms.append(
                {
                    "id": term["id"],
                    "domain": domain,
                    "name": name,
                    "embedding_text": embedding_text,
                }
            )
        except KeyError:
            continue

    return terms

import json
from pathlib import Path
from typing import Any


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
            terms.append({"id": term["id"], "name": name})
        except KeyError:
            continue  # skip if no translation in the given language

    return terms

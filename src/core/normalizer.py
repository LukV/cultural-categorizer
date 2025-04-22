import re
import unicodedata


def normalize(text: str) -> str:
    """Normalize text for embedding: lowercase, remove punctuation,
    strip accents (e.g. é → e), collapse whitespace.
    """
    if not text:
        return ""

    # Lowercase
    text = text.lower()

    # Strip accents
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")

    # Remove punctuation (except useful symbols if needed)
    text = re.sub(r"[^\w\s]", "", text)

    # Collapse multiple spaces
    return re.sub(r"\s+", " ", text).strip()

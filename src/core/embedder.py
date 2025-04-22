import numpy as np
from numpy.typing import NDArray
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from core.normalizer import normalize


class Embedder:
    """A class for embedding text using a pre-trained SentenceTransformer model.
    Provides methods to encode text into dense vectors and compute similarity
    between input text and candidate terms.
    """

    def __init__(self, model_name: str = "distiluse-base-multilingual-cased-v1"):  # noqa: ANN204, D107
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> NDArray[np.float32]:
        """Encode a list of texts into dense vectors."""
        return self.model.encode(texts, convert_to_numpy=True)

    def most_similar(
        self, input_text: str, candidates: list[dict[str, str]], top_k: int = 5
    ) -> list[dict[str, float | str]]:
        """Compute similarity between input and candidate taxonomy terms."""
        input_text_clean = normalize(input_text)
        candidate_texts = [c["embedding_text"] for c in candidates]
        candidate_ids = [c["id"] for c in candidates]
        candidate_names = [c["name"] for c in candidates]

        input_vec = self.encode([input_text_clean])
        candidate_vecs = self.encode(candidate_texts)

        scores = cosine_similarity(input_vec, candidate_vecs)[0]
        top_indices = np.argsort(scores)[::-1][:top_k]

        return [
            {
                "id": candidate_ids[i],
                "name": candidate_names[i],
                "score": float(scores[i]),
            }
            for i in top_indices
        ]

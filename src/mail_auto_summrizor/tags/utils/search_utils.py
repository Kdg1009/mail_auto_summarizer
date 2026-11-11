from sentence_transformers import SentenceTransformer
from pathlib import Path
import json
import numpy as np


class TagEmbeddingSearch:

    def __init__(
        self,
        embedding_files: list[str],
        model: SentenceTransformer | None = None,
    ):
        self.base_dir = Path(__file__).parent.parent

        self.model_name = None
        self.model = model

        self.tag_ids = []
        self.tag_subjects = []
        self.tag_embeddings = None

        self._load_embeddings(embedding_files)

        # Reuse an externally supplied model if available.
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)

    def _load_embeddings(self, embedding_files: list[str]):

        embedding_chunks = []

        for filename in embedding_files:

            path = self.base_dir / filename

            if not path.is_file():
                raise FileNotFoundError(path)

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Check model consistency
            current_model = data["model"]

            if self.model_name is None:
                self.model_name = current_model

            elif self.model_name != current_model:
                raise ValueError(
                    "Different embedding models detected."
                )

            dimension = data["dimension"]
            tags = data.get("tags", [])

            if not tags:
                continue

            # Convert one taxonomy to a single matrix
            vectors = np.asarray(
                [tag["embedding"] for tag in tags],
                dtype=np.float32,
            )

            if vectors.shape != (len(tags), dimension):
                raise ValueError(
                    f"Invalid embedding shape: {filename}"
                )

            embedding_chunks.append(vectors)

            # Keep metadata in the same row order
            self.tag_ids.extend(
                tag["id"] for tag in tags
            )

            self.tag_subjects.extend(
                [data["taxonomy"]] * len(tags)
            )

        if not embedding_chunks:
            raise ValueError("No tag embeddings loaded.")

        # Combine all taxonomy matrices
        self.tag_embeddings = np.concatenate(
            embedding_chunks,
            axis=0,
        )

        # Validate metadata alignment
        if not (
            len(self.tag_ids)
            == len(self.tag_subjects)
            == self.tag_embeddings.shape[0]
        ):
            raise ValueError("Metadata and embedding size mismatch.")

        # Validate embedding dimension
        if self.model is not None:
            expected_dim = self.model.get_sentence_embedding_dimension()

            if self.tag_embeddings.shape[1] != expected_dim:
                raise ValueError("Model and embedding dimensions differ.")

    def search(
        self,
        context: str,
        threshold: float = 0.7,
        top_k: int | None = None,
        subject: list[str] | None = None,
    ) -> dict[str,list[dict]]:

        if not context.strip():
            return {}

        if not -1.0 <= threshold <= 1.0:
            raise ValueError("Threshold must be between -1 and 1.")

        if top_k is not None and top_k <= 0:
            return {}

        # Encode query
        context_emb = self.model.encode(
            f"query: {context}",
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        ).astype(np.float32, copy=False)

        # Calculate cosine similarity (all taxonomies)
        similarities = self.tag_embeddings @ context_emb

        # Optional taxonomy filtering
        if subject:
            subject_set = set(subject)

            mask = np.asarray(
                [s in subject_set for s in self.tag_subjects],
                dtype=bool,
            )
        else:
            mask = np.ones(len(self.tag_ids), dtype=bool)

        # Apply threshold
        valid_indices = np.flatnonzero(
            (similarities >= threshold) & mask
        )

        if len(valid_indices) == 0:
            return {}

        # Group candidates by taxonomy
        grouped_results = {}

        for index in valid_indices:
            taxonomy = self.tag_subjects[index]

            grouped_results.setdefault(taxonomy, []).append(
                {
                    "id": self.tag_ids[index],
                    "taxonomy": taxonomy,
                    "similarity": float(similarities[index]),
                }
            )

        # ================================================
        # 5. Sort and apply top_k per taxonomy
        # ================================================

        for taxonomy, candidates in grouped_results.items():

            candidates.sort(
                key=lambda x: x["similarity"],
                reverse=True,
            )

            if top_k is not None:
                grouped_results[taxonomy] = candidates[:top_k]

        return grouped_results
# Create reference dict [{"id":"embeddings"}] file.
# Always synchronize reference file with tags taxonomy file.

from sentence_transformers import SentenceTransformer
from pathlib import Path
import json
import hashlib

MODEL_NAME = "intfloat/multilingual-e5-small"
BATCHSIZE = 32

def parse_taxonomy(taxonomy:dict) -> dict:
    
    return {
        'version' : taxonomy['version'],
        'subject' : taxonomy['taxonomy'],
        'description' : taxonomy['description'],
        'source_scope' : taxonomy['source_scope'],
        'tags' : taxonomy['tags'],
    }

def make_embedding_text(tag: dict) -> str:
    """
    Build a descriptive text for one taxonomy tag.
    E5 models use the passage: prefix for indexed documents.
    """

    tag_id = tag.get("id", "")
    label = tag.get("label", "")
    description = tag.get("description", "")
    aliases = tag.get("aliases", [])
    examples = tag.get("examples", [])
    excluded_examples = tag.get("excluded_examples", [])
    parent_id = tag.get("parent_id", "")

    parts = [
        f"ID: {tag_id}",
        f"Label: {label}",
        f"Description: {description}",
    ]

    if aliases:
        parts.append(f"Aliases: {', '.join(aliases)}")

    if examples:
        parts.append(f"Examples: {', '.join(examples)}")

    if excluded_examples:
        parts.append(
            f"Excluded examples: {', '.join(excluded_examples)}"
        )

    if parent_id:
        parts.append(f"Parent category: {parent_id}")

    return "passage: " + ". ".join(parts)

def get_taxonomy_hash(taxonomy: dict) -> str:
    """
    Generate hash from taxonomy content.
    """

    content = json.dumps(
        taxonomy,
        ensure_ascii=False,
        sort_keys=True,
    )

    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()

def build_embedding_dict(filename:str, force:bool=False):
    base_dir = Path(__file__).parent.parent
    taxonomy_path = base_dir / filename

    if not taxonomy_path.exists():
        raise FileNotFoundError(f"[ERROR] Could not find file: {taxonomy_path}")

    # Load taxonomy
    with open(taxonomy_path, 'r', encoding='utf-8') as f:
        taxonomy_raw = json.load(f)

    taxonomy = parse_taxonomy(taxonomy_raw)

    # Output path
    embedding_path = base_dir/"embs"/f"{taxonomy_path.stem}.embeddings.json"

    # Check taxonomy changes
    taxonomy_hash = get_taxonomy_hash(taxonomy_raw)

    if embedding_path.exists() and not force:
        with open(embedding_path, 'w', encoding='utf-8') as f:
            existing = json.load(f)

        if existing.get("taxonomy_hash") == taxonomy_hash:
            print("[INFO] Embeddings are already synchronized.")
            return embedding_path

    # Load model
    model = SentenceTransformer(MODEL_NAME)

    # Filter inactive tags
    active_tags = [tag for tag in taxonomy['tags'] if tag.get('active',True)]

    # Prepare batch input
    embedding_texts = [make_embedding_text(tag) for tag in active_tags]

    # Batch encoding
    vectors = model.encode(
        embedding_texts,
        batch_size=BATCHSIZE,
        normalize_embeddings=True,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    # Build reference dictionary
    embedding_tags = []

    for tag, text, vector in zip(active_tags, embedding_texts, vectors):
        embedding_tags.append({
            "id":tag['id'],
            "label":tag['label'],
            "embedding_text":text,
            "embedding":vector.tolist(),
        })

    result = {
        "version":taxonomy["version"],
        "taxonomy":taxonomy["subject"],
        "model":MODEL_NAME,
        "dimension":int(vectors.shape[1]),
        "taxonomy_hash":taxonomy_hash,
        "tags":embedding_tags
    }

    # Save JSON
    with open(embedding_path, "w", encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f"[INFO] Embeddings saved: {embedding_path}")
    return embedding_path

if __name__ == "__main__":
    build_embedding_dict("task_areas.tags.json")

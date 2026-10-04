from sentence_transformers import SentenceTransformer

from llm_memory.models import Memory

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed(memory: Memory) -> list[float]:
    return model.encode(memory.text, normalize_embeddings=True).tolist()

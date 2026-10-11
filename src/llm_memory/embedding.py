from opentelemetry import trace
from sentence_transformers import SentenceTransformer

from llm_memory.models import Memory

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)
tracer: trace.Tracer = trace.get_tracer(__name__)


def embed(memory: Memory) -> list[float]:
    with tracer.start_as_current_span("embed") as span:
        span.set_attribute("embedding.model", MODEL_NAME)
        span.set_attribute("embedding.input_chars", len(memory.text))
        return model.encode(memory.text, normalize_embeddings=True).tolist()

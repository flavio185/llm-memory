# Service that will connect to Vector DB and make calls
import datetime

from llm_memory import embedding
from llm_memory.models import Memory
from llm_memory.qdrant_store import QdrantStore


class MemoryNotFoundError(Exception):
    pass


class AmbiguousMemoryError(Exception):
    pass


class MemoryService:
    def __init__(self):
        self.db_instance = QdrantStore()

    def create_memory(self, memory: Memory):
        now = datetime.datetime.now(tz=datetime.UTC)
        memory.timestamp = now.strftime("%Y%m%d%H%M%S")
        memory.embeddings = embedding.embed(memory)
        self.vector_id = self.db_instance.create_memory(memory)
        return self.vector_id

    def search_memory(
        self, memory: Memory, limit: int = 3, score_threshold: float = 0.4
    ) -> list[dict]:
        memory.embeddings = embedding.embed(memory)
        return self.db_instance.search_memory(memory, limit, score_threshold)

    def get_memory_by_id(self, memory_id: str) -> Memory | None:
        return self.db_instance.get_memory_by_id(memory_id)

    def delete_memory(self, memory: Memory) -> Memory:
        memory.embeddings = embedding.embed(memory)
        results = self.search_memory(memory)
        if not results:
            raise MemoryNotFoundError("No memory similar enough to this text.")
        # Validate that the best match is not too close to the second best.
        if len(results) > 1 and results[0]["score"] - results[1]["score"] <= 0.1:
            raise AmbiguousMemoryError("Not sure about this memory, be more specific.")
        memory_id = results[0]["id"]
        deleted_memory = self.get_memory_by_id(memory_id)
        if deleted_memory is None:
            raise MemoryNotFoundError("Memory no longer exists.")
        self.db_instance.delete_memory(memory_id)
        return deleted_memory

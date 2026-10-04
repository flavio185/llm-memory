# Qdrant helper
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointIdsList, PointStruct, VectorParams

from llm_memory.models import Memory


class QdrantStore:
    def __init__(
        self, db_url: str = "http://localhost:42983", collection: str = "memories"
    ):
        self.collection = collection
        self.client = QdrantClient(url=db_url)
        if not self.client.collection_exists(collection):
            self.client.create_collection(
                collection,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )

    def create_memory(self, memory: Memory) -> str:
        if memory.embeddings is None:
            raise ValueError("memory.embeddings is required to search")
        vector_id = str(uuid.uuid4())
        self.client.upsert(
            self.collection,
            points=[
                PointStruct(
                    id=vector_id,
                    vector=memory.embeddings,
                    payload={"text": memory.text, "timestamp": memory.timestamp},
                )
            ],
        )
        return vector_id

    def delete_memory(self, memory_id: str):
        self.client.delete(
            collection_name=self.collection,
            points_selector=PointIdsList(points=[memory_id]),
        )

    def search_memory(
        self, memory: Memory, limit: int = 3, score_threshold: float = 0.4
    ) -> list[dict]:
        if memory.embeddings is None:
            raise ValueError("memory.embeddings is required to search")
        result = self.client.query_points(
            self.collection,
            query=memory.embeddings,
            limit=limit,
            score_threshold=score_threshold,
        )
        return [
            {"id": str(p.id), "score": p.score, **(p.payload or {})}
            for p in result.points
        ]

    def get_memory_by_id(self, memory_id: str) -> Memory | None:
        points = self.client.retrieve(
            self.collection,
            ids=[memory_id],
            with_payload=True,
            with_vectors=True,
        )
        if not points:
            return None
        point = points[0]
        payload = point.payload or {}
        return Memory(
            id=str(point.id),
            text=payload["text"],
            embeddings=point.vector if isinstance(point.vector, list) else None,  # type: ignore
            timestamp=payload.get("timestamp"),
        )

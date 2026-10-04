from pydantic import BaseModel, StrictFloat


class Memory(BaseModel):
    id: str | None
    text: str
    embeddings: list[StrictFloat] | None
    timestamp: str | None

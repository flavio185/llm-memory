from fastapi import FastAPI, HTTPException

from llm_memory.memory_service import (
    AmbiguousMemoryError,
    MemoryNotFoundError,
    MemoryService,
)
from llm_memory.models import Memory

app = FastAPI()


# 2. Use the model as a function argument
@app.post("/memory/create")
def create_memory(memory: Memory):
    service = MemoryService()
    service.create_memory(memory)
    return {"memory": memory}


@app.post("/memory/delete")
def delete_memory(memory: Memory):
    # Delete memory
    service = MemoryService()
    try:
        deleted_memory = service.delete_memory(memory)
    except MemoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AmbiguousMemoryError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return {
        "message": f"{deleted_memory.text} deleted",
        "data da memoria": deleted_memory.timestamp,
    }


@app.post("/memory/search")
def search_memory(memory: Memory):
    service = MemoryService()
    results = service.search_memory(memory)
    if not results:
        return {"message": "I don't know what you're talking about", "results": []}
    return {"results": results}

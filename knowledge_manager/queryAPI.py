from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from database.db_search import search_v2, query_v2, get_by_ids_v2

app = FastAPI()

class QueryRequest(BaseModel):
    context: str
    user: str | None = None
    type: str | None = None
    source: str | None = None

class EntityRequest(BaseModel):
    ids: List[str]
    user: str

@app.post("/KM/search")
#Search based on embedding similarity.
def similarity_search(request : QueryRequest):
    output = search_v2(
        search_str=request.context,
        user=request.user,
        type=request.type, #Valid types: msg,tbl,doc,json
        source=request.source
    )
    print("Embedding search yield:", output)
    return {"result": output}

@app.get("/KM/query")
#Query search based on metadata filters.
def filtered_search(
    user: str, 
    type: str | None = None, 
    source: str | None = None):

    output = query_v2(
        user=user,
        type=type, #Valid types: msg,tbl,doc,json
        source=source
    )
    print("Filtered search yield:", output)
    return {"result": output}

@app.post("/KM/entity")
#Fetch entities by exact ID.
def search_by_id(request : EntityRequest):
    output = get_by_ids_v2(
        ids=request.ids,
        user=request.user
    )
    print("ID search yield:", output)
    return {"result": output}

#For manual testing
"""
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
"""

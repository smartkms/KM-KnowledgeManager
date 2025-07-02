from fastapi import FastAPI
from pydantic import BaseModel
from database.db_service import query

app = FastAPI()

class QueryRequest(BaseModel):
    # TODO add filters for searching by metadata (if filters are provided by RAG)
    text: str

@app.post("/KM/query")
#Sends query to MilvusDB and returns search results
def query_request(request : QueryRequest):
    output = query(request.text)
    return {"results": output}

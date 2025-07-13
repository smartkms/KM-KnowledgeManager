from fastapi import FastAPI
from pydantic import BaseModel
from database.db_search import isci_zapise

app = FastAPI()

class QueryRequest(BaseModel):
    # TODO add filters for searching by metadata (if filters are provided by RAG)
    text: str

@app.post("/KM/query")
#Sends query to MilvusDB and returns search results
def query_request(request : QueryRequest):
    output = isci_zapise(request.text)
    
    # why not just return output?
    return {"results": output}

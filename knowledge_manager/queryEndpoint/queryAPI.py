from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/KM/query")
def query(data : QueryRequest):
    output = data.query
    return {"response": "SENT: " + output}

def searchMilvus(query): #placeholder
    output = "temp"
    return output

def response(query): #placeholder
    output = "temp"
    return output

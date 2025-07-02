from fastapi import FastAPI
from pydantic import BaseModel
from database.db_service import isci_zapise

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/KM/query")
def query(data : QueryRequest):
    output = isci_zapise(data.query)
    return {
        "res" : output
    }

def searchMilvus(query): #placeholder
    output = "temp"
    return output

def response(query): #placeholder
    output = "temp"
    return output

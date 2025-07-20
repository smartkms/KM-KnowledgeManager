from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from redis import Redis
from rq import Queue
from datetime import datetime
import os
import collectionEndpoint.bouncer as bouncer

app = FastAPI()

redisHost = os.getenv('REDIS_HOST', 'localhost')
redisHostPort = os.getenv('REDIS_HOST_PORT', 6379)
redisConnect = Redis(host=redisHost, port=redisHostPort)
taskQueue = Queue('processing', connection=redisConnect)

class User(BaseModel):
    id: str
    displayName: str

class Message(BaseModel):
    createdDateTime: datetime
    user: User
    body: str

class ChannelMessages(BaseModel):
    channelId: str
    messages: list[Message]

class File(BaseModel) : 
    # TODO minIO will pass a different format for files
    fileName: str
    fileLocation: HttpUrl

class PushRequest(BaseModel):
    typefield: str
    platform: str
    id: str
    timestamp: datetime
    content: dict

@app.post("/KM/push")
#Sends data for encoding and storing in Milvus DB
#Data sent is template sensitive
def push_data(data : PushRequest):
    taskQueue.enqueue(bouncer.processData, data.dict())
    return {"status": "successfully queued", "id": data.id}
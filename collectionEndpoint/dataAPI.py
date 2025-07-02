from fastapi import FastAPI
from pydantic import BaseModel
from redis import Redis
from rq import Queue
import os
import bouncer

app = FastAPI()

redisHost = os.getenv('REDIS_HOST', 'localhost')
redisConnect = Redis(host=redisHost, port=6379)
taskQueue = Queue('processing', connection=redisConnect)

class User(BaseModel):
    id: str
    displayName: str

class Message(BaseModel):
    createdDateTime: str
    user: User
    body: str

class ChannelMessages(BaseModel):
    channelId: str
    messages: list[Message]

class File(BaseModel) : 
    # TODO minIO will pass a different format for files
    fileName: str
    fileLocation: str

class PushRequest(BaseModel):
    typefield: str
    platform: str
    id: str
    timestamp: str
    content: dict

@app.post("/KM/push")
#Sends data for encoding and storing in Milvus DB
#Data sent is template sensitive
def push_data(data : PushRequest):
    taskQueue.enqueue(bouncer.processData, data.dict())
    return {"status": "successfully queued", "id": data.id}
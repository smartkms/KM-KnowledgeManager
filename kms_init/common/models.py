from pydantic import BaseModel

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

class File(BaseModel) : #minIO needs different one
    fileName: str
    fileLocation: str

class PushRequest(BaseModel):
    typefield: str
    platform: str
    id: str
    timestamp: str
    content: dict

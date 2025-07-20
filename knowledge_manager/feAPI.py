import os
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from datetime import datetime
from io import BytesIO
from database.db_store import store_file_v2
from database.models import StoreFunctionType

app = FastAPI()

class Message(BaseModel):
    createTime: datetime
    messageId: str
    role: str
    content: str

class ChatRequest(BaseModel):
    title: str
    createTime: datetime
    updateTime: datetime | None = None
    conversationId: str
    messages: list[Message]

@app.post("/KM/saveChat")
#Send chats to Milvus for vectorization
def send_chat(chat : ChatRequest):
    output = chat.messages
    print(f"Encoding {len(output)} messages from {chat.conversationId}...")
    
    #TODO fix this by not sending each message but the whole convo
    for message in output:
        metadata = {
                "create_time": message.createTime,
                "message_id": message.messageId,
                "role": message.role,
                "message_content": message.content,
            }
        txt_file = BytesIO(message.content.encode())
        store_file_v2(txt_file, metadata, StoreFunctionType.PLAIN_TEXT)

@app.post("/KM/saveFile")
#Send files to Milvus for vectorization
#Use a multipart/form-data POST request
async def send_file(
    file: UploadFile = File(...), # <-- the actual file
    fileId: str = Form(...),
    fileName: str = Form(...),
    createTime: datetime = Form(...),
    updateTime: datetime | None = Form(None)):

    print(f"Processing file {fileName}...")

    file_content = await file.read()
    file_stream = BytesIO(file_content)
    fileType = os.path.splitext(fileName)[1].lower()
    metadata = {
            "file_id": fileId,
            "file_name": fileName,
            "posted_date_time": createTime
        }

    if fileType in [".docx", ".xlsx", ".pptx"]:
        store_file_v2(file_stream,metadata,StoreFunctionType.MS_OFFICE)
    elif fileType in [".pdf"]:
        store_file_v2(file_stream,metadata,StoreFunctionType.PDF)
    else:
        print("Error, unsupported file type.")


#Uncomment this part and run feAPI.py for manual testing:
"""
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
"""

#Example of chat JSON:
"""
{
  "title": "Michelangelo biography summary",
  "createTime": "2025-07-20T14:30:00",
  "updateTime": "2025-07-20T14:30:05",
  "conversationId": "784326478",
  "messages": [
    {
      "createTime": "2025-07-20T14:30:00",
      "messageId": "msg1",
      "role": "user",
      "content": "Tell me about Michelangelo."
    },
    {
      "createTime": "2025-07-20T14:30:05",
      "messageId": "msg2",
      "role": "assistant",
      "content": "Michelangelo was an Italian sculptor, painter, architect and poet of the High Renaissance..."
    }
  ]
}
"""

#Example use of "/KM/saveFile" in python:
"""
with open("document.pdf", "rb") as f:
        response = requests.post(
            "http://localhost:8000/KM/saveFile",
            files={"file": ("document.pdf", f, "application/pdf")},
            data={
                "fileId": "32847832",
                "fileName": "document.pdf",
                "createTime": datetime.now().isoformat(),
            }
        )
"""
import os
import requests
from io import BytesIO
from database.db_store import store_file_v2
from database.models import StoreFunctionType

def file_download(link: str):
    file = requests.get(link)
    file.raise_for_status()
    return BytesIO(file.content)

def processData(data: dict):
    print(f"[Bouncer] Received: {data['id']}")

    if data["typefield"] == "messages":
        output = data["content"]["messages"]
        print(f"Encoding {len(output)} messages from {data['content']['channelId']}...")
        
        #Do we add all messages up or put each one through the store function?
        for message in output:
            metadata = {
                #Maybe add channel and channel ID?
                "user_id": message["user"]["id"],
                "username": message["user"]["displayName"],
                "created_date_time": message["createdDateTime"],
            }
            txt_file = BytesIO(message["body"].encode())
            store_file_v2(txt_file,metadata,StoreFunctionType.PLAIN_TEXT)

    elif data["typefield"] == "file":
        print(f"Processing file {data['content']['fileName']}...")

        file = file_download(data["content"]["fileLocation"])
        fileType = os.path.splitext(data["content"]["fileName"])[1].lower()
        metadata = {
            "file_id": data["id"],
            "file_name": data["content"]["fileName"],
            "posted_date_time": data["timestamp"]
        }

        if fileType in [".docx", ".xlsx", ".pptx"]:
            store_file_v2(file,metadata,StoreFunctionType.MS_OFFICE)
        elif fileType in [".pdf"]:
            store_file_v2(file,metadata,StoreFunctionType.PDF)
        else:
            print("Error, unsupported file type.")
        

    print(f"[Bouncer] Done processing: {data['id']}")

import os
import requests
from knowledge_manager.database.db_service import store_text, store_pdf_files, store_msoffice_files

def file_download(link: str):
    file = requests.get(link)
    file.raise_for_status()
    return BytesIO(file.content)

def processData(data: dict):
    print(f"[Bouncer] Received: {data['id']}")

    if data["typefield"] == "messages":
        output = data["content"]["messages"]
        print(f"Encoding {len(output)} messages from {data['content']['channelId']}...")
        
        for message in output:
            metadata = {
                #maybe add channel in channel ID?
                "user_id": message["user"]["id"],
                "username": message["user"]["displayName"],
                "created_date_time": message["createdDateTime"],
            }
            store_text(message["body"],metadata)

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
            store_msoffice_files(file,metadata)
        elif fileType in [".pdf"]:
            store_pdf_files(file,metadata)
        else:
            print("Error, unsupported file type.")
        

    print(f"[Bouncer] Done processing: {data['id']}")

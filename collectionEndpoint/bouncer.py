import time
import random
from knowledge_manager.database.db_service import store_text, store_pdf_files, store_msoffice_files

def processData(data: dict):
    print(f"[Bouncer] Received: {data['id']}")

    if data["typefield"] == "messages":
        output = data["content"]["messages"]
        print(f"Encoding {len(output)} messages from {data['content']['channelId']}...")
        for message in output:
            metadata = {
                #maybe add channel ID?
                "user_id": message["user"]["id"],
                "username": message["user"]["displayName"],
                "date_time": message["createdDateTime"],
            }
            store_text(message["body"],metadata)

    elif data["typefield"] == "file":
        # TODO we need to add proper file passing to the database (waiting on collector for minIO)
        output = data["content"]["fileLocation"]
        print(f"Processing file {data['content']['fileName']}...")
        time.sleep(random.randint(1,5)) #simulating

    print(f"[Bouncer] Done processing: {data['id']}")

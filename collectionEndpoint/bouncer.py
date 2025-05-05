import time
import random

def processData(data: dict):
    print(f"[Bouncer] Received: {data['id']}")

    if data["typefield"] == "messages":
        output = data["content"]["messages"]
        print(f"Encoding {len(output)} messages from {data['content']['channelId']}...")
        time.sleep(random.randint(1,5)) #simulating

    elif data["typefield"] == "file":
        output = data["content"]["fileLocation"]
        print(f"Processing file {data['fileName']}...")
        time.sleep(random.randint(1,5)) #simulating

    print(f"[Bouncer] Done processing: {data['id']}")
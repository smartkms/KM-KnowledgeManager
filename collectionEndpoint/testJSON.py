import requests
import json
import os

url = 'http://localhost:8000/KM/push'

def send_post_request(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)

    response = requests.post(url, json=data)
    
json_files = [f for f in os.listdir() if f.startswith('example') and f.endswith('.json')]

for json_file in json_files:
    send_post_request(json_file)
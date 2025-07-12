# KM-KnowledgeManager
Clone repo
``` bash
git clone https://github.com/smartkms/KM-Knowledge-Manager
```
## Initialization
### .env file
In root directory create `.env` file. Declare the following variables:
```ini
OPENAI_API_KEY=my-secret-key
VECTOR_DB_URI=http://localhost:19530
VECTOR_DB_TOKEN=root:Milvus
VECTOR_DB_NAME=km
```
### Local docker instance of milvus
From root of project:
```bash
cd docker
docker compose up -d
```
Milvus should be running on `localhost:19530`. User interface is on `localhost:9091/webui`.

### Initialize and populate database
In `kms_ini` folder rename `milvus_init.yaml.example` to `milvus_init.yaml`.
From project root:
```bash
cd kms_init
pip install -r requirements.txt
python3 init_db.py
```

## Query API for RAG
Sends queries to the Milvus database.
From project root:
```bash
cd knowledge_manager
pip install -r requirements.txt
uvicorn --reload queryAPI:app
```
A SwaggerUI is established on `http://127.0.0.1:8000/docs`
where you can test the API or just make a post request at `http://localhost:8000/KM/query` in your code.

## Data API with RedisQueue
Make sure you have Docker installed.

**1.** Move to */KM-KnowledgeManager/knowledge_manager/collectionEndpoint* and run these commands to clear containers and establish the docker:
``` bash
  docker-compose up redis -d
  ```
**2.** Run the dataAPI:
```bash
 cd ..
 python3 -m venv collectionEndpoint/.venvDataApi
 source collectionEndpoint/.venvDataApi/bin/activate
 pip install -r collectionEndpoint/requirements.txt
 uvicorn dataAPI:app

```

**3.** Tests
- 1st test: You can test the api on *http://127.0.0.1:8000/docs*
- 2nd test: Open a new terminal in the *KM-Knowledge-Manager/knowledge_manager/collectionEndpoint/Tests* directory and run testJSON.py to test sending JSON data.
  ``` bash
  python testJSON.py
  ```
  If the test is successfull this line should appear on the first terminal:
  *INFO:     127.0.0.1:56180 - "POST /KM/push HTTP/1.1" 200 OK*
  
  You can add your own JSON files that folow the same format and   name (exampleX.json), currently there are only 3 provided from   the Collector.

## Usage
### Database package
The only methods for external use from database package are those defined and documented in db_service. All the other are for **internal use** only.

Check `demo.py` to see examples of usage.

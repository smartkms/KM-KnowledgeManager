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
```
### Local docker instance of milvus
From root of project:
```bash
cd docker
docker compose up -d
```
Milvus should be running on `localhost:19530`. User interface is on `localhost:9091`.

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

To test it, install uvicorn 
``` bash
pip install uvicorn
```
and run this command in */KM-KnowledgeManager/knowledge_manager/api* directory
``` bash
uvicorn queryAPI:app -reload
```
A SwaggerUI is established on `http://127.0.0.1:8000/docs`
where you can test the API or just make a post request at `http://localhost:8000/KM/query` in your code.

## Data API with RedisQueue
Make sure you have Docker installed.

**1.** Move to */KM-KnowledgeManager/collectionEndpoint* and run these commands to clear containers and establish the docker:

  **On Windows**
  ``` bash
  docker-compose up --build
  ```
  **On Linux**
  ``` bash
  sudo docker-compose up --build
  ```
  If the queue sets up correctly you should see:
  
  *rqworker    | 12:52:34 *** Listening on processing...*
  
  The terminal will display RedisQueue jobs and handling

**2.** Open a new terminal in the same directory and run testJSON.py to test sending JSON data.
  ``` bash
  python testJSON.py
  ```
  Successfull transfers are displayed on the 1st terminal and end with:
  
  *rqworker    | [Bouncer] Done processing: 'id'*
  
  You can add your own JSON files that folow the same format and   name (exampleX.json), currently there are only 3 provided from   the Collector.
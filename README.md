# KM-KnowledgeManager
Clone repo
``` bash
git clone https://github.com/smartkms/KM-Knowledge-Manager
```
## Query API
For now its a simple API that only returns back the query.

To test it, install uvicorn in */KM-KnowledgeManager/queryEndpoint* directory:
``` bash
pip install uvicorn
```
and run this command:
``` bash
uvicorn queryAPI:app -reload
```
A SwaggerUI is established on *http://127.0.0.1:8000/docs*
where you can test teh API.
## Data API with RedisQueue
Make sure you have Docker installed.

**1.** Move to */KM-KnowledgeManager/collectionEndpoint* and run these commands to clear containers and establish the docker:

  **On Windows**
  ``` bash
  docker-compose up --build
  ```
  **On Linux**
  ``` bash
  sudo docker rm -f $(sudo docker ps -aq)
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

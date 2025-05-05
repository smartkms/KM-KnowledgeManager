# KM-Knowledge-Manager
Clone the repo
``` bash
git clone https://github.com/smartkms/KM-Knowledge-Manager
```
## Data API with RedisQueue
Make sure you have Docker installed.

1. Move to */collectionEndpoint* and run these commands to clear containers and establish the docker:

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

2. Open a new terminal in the same directory and run testJSON.py to test sending JSON data.
``` bash
python3 testJSON.py
```
Successfull transfers are displayed on the 1st terminal and end with:

*rqworker    | [Bouncer] Done processing: 'id'*

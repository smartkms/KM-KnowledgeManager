import json
import os
from pymilvus import MilvusClient, MilvusException
from common.logger import getLogger


logger = getLogger("populate-db")

JSON_PATH = "./resources/json"

def populate_milvus_db(config) :
    try:
        uri = config["milvus"]["uri"]
        populate = config["populate"]
        logger.info("Starting")
        for name, client in populate["clients"].items():
            try:
                milvus_client = MilvusClient(uri=uri, token=client["token"], db_name=client["db"])
                for folder_name, metadata in client["folders"].items():
                    try:
                        with open(os.path.join(JSON_PATH, f"{folder_name}.json"), 'r', encoding='utf-8') as f:
                            entities = json.load(f)
                        insert_res = milvus_client.insert(collection_name=metadata["collection"], data=entities) # has also field 'ids'
                        logger.info("Inserted %d entities from %s.json into collection %s", insert_res["insert_count"], folder_name, metadata["collection"])
                    except FileNotFoundError as e:# json deserialization | open file
                        logger.fatal("Could not open file %s/%s.json\n\t%s", os.path.abspath(JSON_PATH), folder_name, e)
                    except json.JSONDecodeError as e:
                        logger.fatal("Could not decode file %s.json",  folder_name)
                    except MilvusException as e:
                        logger.fatal("Could not insert entities into collection %s.", metadata["collection"])
            except MilvusException as e:
                logger.fatal("Could not create client %s.", name)
            finally:
                milvus_client.close()
    except FileNotFoundError as e:
        logger.fatal("Could not open folder %s.", JSON_PATH)
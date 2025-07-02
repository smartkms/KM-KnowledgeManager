# transform raw documenta data into json data to import into database
import yaml
import json
import os
from common.logger import getLogger
from common.embedding_openai import embed_text
from utils.md_splitter import splitfile

logger = getLogger("transform-docs")
# TODO move macros to __init__.py
RESOURCE_PATH = "./resources/"
JSON_PATH = "./resources/json"


def transform_doc_to_json(populate):
    try:
        clients = populate["clients"]
        for name, client in clients.items():
            logger.info("Converting documents for client %s.", name)
            for folder_name, metadata in client["folders"].items():
                if metadata["skip_transform"]:
                    logger.info("Skipping transformation of %s.", folder_name)
                    continue
                path = f"{RESOURCE_PATH}{folder_name}"
                # TODO add metadata as dictionary, as they are, later
                datatype = metadata["type"]
                user = metadata["user"]
                entities = []
                try:
                    files = os.listdir(path=path)
                    for file_name in files:
                        try:
                            with open(os.path.join(path, file_name), 'rb') as file:
                                chunks = splitfile(file, file_name)
                                for chunk in chunks:
                                    vector = embed_text(chunk)
                                    entity = {
                                        "text" : chunk,
                                        "embedding" : vector,
                                        "type" : datatype,
                                        "user" : user
                                    }
                                    entities.append(entity)
                        except FileNotFoundError as e:
                            logger.fatal("File %s in folder %s not found.", file_name, folder_name)
                    json_name = folder_name + ".json"
                    try:
                        with open(os.path.join(JSON_PATH, json_name), "w") as json_file:
                            json.dump(entities, json_file)
                    except Exception as e:
                        logger.fatal("Could not create file %s: %s", json_name, e)
                except FileNotFoundError as e:
                    logger.fatal("Folder %s not found.", folder_name)
                

    except FileNotFoundError:
        logger.fatal("Error: %s not found.", config_file)
    except yaml.YAMLError as e:
        logger.fatal("Error: Invalid YAML format - %s", e)
    except KeyError as e:
        logger.fatal("Error: Missing key in configuration - %s", e)



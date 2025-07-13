from .embedding_openai import embed_text
from dotenv import load_dotenv
import os
from pymilvus import MilvusClient
from typing import List
from .models import FileMetadata, BaseEntity
from . import MILVUS_PUBLIC_USER

use_local_db = False
load_dotenv()

# TODO preverit kako se najboljse poda skupek sporocil ai modelu

URI = os.getenv("VECTOR_DB_URI", "http://localhost:19530")
TOKEN = os.getenv("VECTOR_DB_TOKEN", "root:Milvus")
DB_NAME = os.getenv("VECTOR_DB_NAME", "km")

DEFAULT_COLLECTION_NAME="data"
# TODO import various collections from yaml config file
COLLECTION_NAME = "data"

# TODO not use same client for read and write
milvus_client = MilvusClient(uri=URI, token=TOKEN, db_name=DB_NAME)

# Important
# TODO v2 apis for calling database

# Features to implement (not urgent):
# TODO preveri tipe iskanja, dodaj iskanje preko metapodatkov kot dodatnih filtrov, validate filter expressions
# TODO preveri, ali je vredno zapis shraniti (check insert funkcija), in kaj zbrisati
# TODO razsiri na vec zapisov z istimi metapodatki hkrati List(str) | str
# TODO select outputfields to return, avoid vectors
# TODO use source LIKE {source} for searching for grater flexibility
# TODO rethink position

# V2 APIs
def store_data_v2(chunks : List[str], metadata : FileMetadata) -> List[str]:
    entities=[]
    for chunk in chunks:
        embedding=embed_text(chunk)
        entity = metadata.model_copy(
            update={
                "text" : chunk,
                "embedding" : embedding
            },
            deep=True
        )
        entities.append(entity.model_dump())
    res = milvus_client.insert(collection_name=COLLECTION_NAME, data=entities)
    return res["ids"]

# TODO add offset and limit
# TODO can erturn similarity to query vector, can implement something about it
# adds user to filtering, user should be specified and validated in resource class
def search_data_v2(query : str, type : str | None = None, source : str | None = None, user : str = MILVUS_PUBLIC_USER) -> List[BaseEntity]:
    filter_expression_list = ["user == {user} "]
    filter_params = {
        "user" : user
    }
    if type != None:
        filter_expression_list.append(" AND type == {type}")
        filter_params["type"] = type
    if source != None:
        filter_expression_list.append(" AND source == {source}")
        filter_params["source"] = source
    filter_expression = ' '.join(filter_expression_list)
    embedding = embed_text(query)
    res = milvus_client.search(collection_name=COLLECTION_NAME, data=[embedding], output_fields=["*"], filter=filter_expression, filter_params=filter_params)
    return list(map(lambda entity : BaseEntity.model_validate(entity["entity"]), res[0]))

# searches only by scalar
# TODO validate parameters (should not contain spaces)
def query_data_v2(type : str | None = None, source : str | None = None, user : str = MILVUS_PUBLIC_USER) -> List[BaseEntity]:
    filter_expression_list = ["user == {user} "]
    filter_params = {
        "user" : user
    }
    if type != None:
        filter_expression_list.append(" AND type == {type}")
        filter_params["type"] = type
    if source != None:
        filter_expression_list.append(" AND source == {source}")
        filter_params["source"] = source
    filter_expression = ' '.join(filter_expression_list)
    res = milvus_client.query(collection_name=COLLECTION_NAME, output_fields=["*"], filter=filter_expression, filter_params=filter_params)
    return list(map(lambda entity : BaseEntity.model_validate(entity), res))

# not using milvus get function to enable searching by user
def query_data_by_id_v2(ids : List[str], user : str = MILVUS_PUBLIC_USER) -> List[BaseEntity]:
    filter_expression = "user == {user} AND id IN {ids}"
    filter_params = {
        "user" : user,
        "ids" : ids
    }
    res = milvus_client.query(collection_name=COLLECTION_NAME, output_fields=["*"], filter=filter_expression, filter_params=filter_params)
    return list(map(lambda entity : BaseEntity.model_validate(entity), res))

# V1 apis, will be replaced by API's using Models as parameters and having additional parameters
@DeprecationWarning
def shrani_podatke(tekst: str, metapodatki: dict[str, any]):

    vektor = embed_text(tekst)
    is_new = True # TODO add function to check this attribute
    metapodatki["text"]=tekst
    metapodatki["embedding"]=vektor
    if is_new:
        res = milvus_client.insert(collection_name=COLLECTION_NAME, data=metapodatki)
        
    return res["ids"][0]
    # Example return object:
    # {'insert_count': 1, 'ids': ['459296023779213584']}

@DeprecationWarning
def isci_zapise(tekst: str):
    vector = embed_text(tekst)
    print("Vector size: " + str(vector.__len__()))
    res = milvus_client.search(collection_name=COLLECTION_NAME, data=[vector], limit=2, output_fields=["text", "id", "$meta", "user", "type"], filter="user == \"test\"")
    return list(map(lambda entity : entity["entity"], res))
    # Example return (is list of list, $meta dynamic field will be split to its components):
    # [[
    #     {
    #         'id': '459296023779213584', 
    #         'distance': 0.5804224610328674, 
    #         'entity': {
    #             'other': 'tralala', 
    #             'user': 'test', 
    #             'type': 'document', 
    #             'text': 'Database dela dobro', 
    #             'id': '459296023779213584'}
    #             }
    #     }
    # ]]
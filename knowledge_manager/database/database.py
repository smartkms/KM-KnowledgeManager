from .embedding_openai import embed_text
from dotenv import load_dotenv
import os
from pymilvus import MilvusClient

use_local_db = False
load_dotenv()

# TODO preverit kako se najboljse poda skupek sporocikl ai modelu
# TODO RBAC

URI = os.getenv("VECTOR_DB_URI", "http://localhost:19530")
TOKEN = os.getenv("VECTOR_DB_TOKEN", "root:Milvus")
DB_NAME = os.getenv("VECTOR_DB_NAME", "db")

DEFAULT_COLLECTION_NAME="data"
# TODO import various collections from yaml config file
COLLECTION_NAME = "data"

milvus_client = MilvusClient(uri=URI, token=TOKEN, db_name=DB_NAME)

# Important
# TODO v2 apis for calling database, change existing to use pymilvus

# Features to implement (not urgent):
# TODO preveri tipe iskanja, dodaj iskanje preko metapodatkov kot dodatnih filtrov, validate filter expressions
# TODO preveri, ali je vredno zapis shraniti (check insert funkcija), in kaj zbrisati
# TODO razsiri na vec zapisov z istimi metapodatki hkrati List(str) | str

# V2 APIs


# V1 apis, will be replaced by API's using Models as parameters and having additional parameters
@DeprecationWarning
def shrani_podatke(tekst: str, metapodatki: dict[str, any]):

    vektor = embed_text(tekst)
    is_new = True # TODO add function to check this attribute
    metapodatki["text"]=tekst
    metapodatki["embedding"]=vektor
    if is_new:
        res = milvus_client.insert(collection_name=COLLECTION_NAME, data=metapodatki)
        
    return res
    # Example return object:
    # {'insert_count': 1, 'ids': ['459296023779213584']}

@DeprecationWarning
def isci_zapise(tekst: str):
    vector = embed_text(tekst)
    print("Vector size: " + str(vector.__len__()))
    res = milvus_client.search(collection_name=COLLECTION_NAME, data=[vector], limit=2, output_fields=["text", "id", "$meta", "user", "type"], filter="user == \"test\"")
    return res
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

from langchain_milvus import BM25BuiltInFunction, Milvus
from embedding_openai import embeddings, embed_text
# from kms_db import use_local_db
from dotenv import load_dotenv
import os

use_local_db = True
load_dotenv()
# TODO preverit kako se najboljse poda skupek sporocikl ai modelu
# TODO RBAC

if use_local_db:
    LocalDBURI = "./milvus_local.db"
    vectorstore = Milvus(
        embedding_function=embeddings,
        connection_args={"uri": LocalDBURI},
        index_params={"index_type": "FLAT", "metric_type": "L2"},
        collection_name="vectorstore_demo",
        drop_old=False,
        auto_id=True,
        primary_field="pk"
    )
else:
    URI = os.getenv("VECTOR_DB_URI")
    vectorstore = Milvus(
        embedding_function=embeddings,
        connection_args={"uri": URI, "token": "root:Milvus", "db_name": "milvus_demo"},
        index_params={"index_type": "FLAT", "metric_type": "L2"},
        consistency_level="Strong",
        drop_old=False,  # set to True if seeking to drop the collection with that name if it exists
        collection_name="vectorstore_demo",
        auto_id=True,
        primary_field="pk"
    )
# print("db_init ok")

# def func():
#     txt="Database dela dobro"
#     vektor = embed_text(txt)
#     slovar= dict(avtor="Peter", leto=2025)
#     print(slovar)
#     vectorstore_local.add_embeddings(texts=[txt], embeddings=[vektor], metadatas=[slovar])
#     res = vectorstore.add_embeddings(texts=[txt], embeddings=[vektor], metadatas=[slovar])
#     print(res)

# TODO implemetiraj en search in en create metodo
# TODO hrani embeddinge in podatke v lokalnem datoteki, da jih lahko loadas

# TODO razsiri na vec zapisov z istimi metapodatki hkrati
def shrani_podatke(tekst: str, metapodatki: dict[str, any]):
    # TODO preveri, ali je vredno zapis shraniti (check insert funkcija), in kaj zbrisati
    # TODO spremeni VectorMetadata v slovar
    vektor = embed_text(tekst)
    # print("embed ok")
    return vectorstore.add_embeddings(texts=[tekst], embeddings=[vektor], metadatas=[metapodatki])

def isci_zapise(tekst: str):
    # TODO preveri tipe iskanja, dodaj iskanje preko metapodatkov kot dodatnih filtrov
    res = vectorstore.similarity_search(tekst)
    return res

# def func_test():
#     txt="Database dela dobro"
#     vektor = [0.60, 0.23, 0.08]
#     slovar= dict(avtor="Peter", leto=2023)
#     print(slovar)
#     res = vectorstore.add_embeddings(texts=[txt], embeddings=[vektor], metadatas=[slovar])
#     print(res)

# def search_test():
#     res = vectorstore.similarity_search_by_vector(embedding=[0.6, 0.6, 1.0], k=1)
#     print (res)

# func_test()
# search_test()
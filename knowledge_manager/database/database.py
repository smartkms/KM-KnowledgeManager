from .embedding_openai import embeddings, embed_text
from dotenv import load_dotenv
import os
from pymilvus import MilvusClient

use_local_db = False
load_dotenv()
# TODO preverit kako se najboljse poda skupek sporocikl ai modelu
# TODO RBAC

URI = os.getenv("VECTOR_DB_URI")
milvus_client = MilvusClient(uri=URI, token="root:Milvus", db_name="km")
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
# def shrani_podatke(tekst: str, metapodatki: dict[str, any]):
#     # TODO preveri, ali je vredno zapis shraniti (check insert funkcija), in kaj zbrisati
#     # TODO spremeni VectorMetadata v slovar
#     vektor = embed_text(tekst)
#     # print("embed ok")
#     return vectorstore.add_embeddings(texts=[tekst], embeddings=[vektor], metadatas=[metapodatki])

def isci_zapise(tekst: str):
    # TODO preveri tipe iskanja, dodaj iskanje preko metapodatkov kot dodatnih filtrov
    vector = embed_text(tekst)
    print("Vector size: " + str(vector.__len__()))
    res = milvus_client.search(collection_name="data", data=[vector], limit=2, output_fields=["text"], filter="user == \"test\"")
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
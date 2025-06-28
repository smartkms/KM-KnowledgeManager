# Tukaj se bodo nahajale funkcije, ki imajo opravka y embeddingi in parametri za enmbedding
# Sprva bo tukaj naòeloma funkcija embed (text) in API_kljuc ya dostop do Google Vertexai iz .env
# Moznost dodat se funkcijo, ki vrne embeddings model

# Trenutna tezava: potrebuje vertexai account, da deluje. Kar pomeni, da trenutno uporabljamo OpenAI embeddinge
# Embeddinge delamo posebej, da lahko preden damo embeddin v bazo preverimo, ali moramo kaj posodobiti ipd

from dotenv import load_dotenv
import os
from langchain_google_vertexai import VertexAIEmbeddings

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    print("GOOGLE_API_KEY env variable is missing.")


# Initialize the a specific Embeddings Model version
embeddings = VertexAIEmbeddings(model_name="text-embedding-004")

vektor =  embeddings.embed(["I like pizza."])
print(vektor)
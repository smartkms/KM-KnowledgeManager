# Obstaja več tipov embeddingov, async, text, document
# V Zacetni fazi bo implementiran samo sinhron za tekst
# TODO raziskat kako OpeAI razdeli vecje dokumente v chunke

from dotenv import load_dotenv
from typing import List
import os
from langchain_openai import OpenAIEmbeddings

load_dotenv()
if "OPENAI_API_KEY" not in os.environ:
    print("OPENAI_API_KEY variable is missing in .env file.")

# TODO bolje definirati parametre embedinga, trenutno je izbran samo tip (najcenejsi)
# param check_embedding_ctx_length: bool = True
# Whether to check the token length of inputs and automatically split inputs longer than embedding_ctx_length.
# param dimensions: int | None = None
# The number of dimensions the resulting output embeddings should have.
# Only supported in text-embedding-3 and later models.
# param embedding_ctx_length: int = 8191
# The maximum number of tokens to embed at once.
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    # With the `text-embedding-3` class
    # of models, you can specify the size
    # of the embeddings you want returned.
    dimensions=1024
)

# Features
# TODO dodati check tokenov, òe je text predolg, se sprozi exeption
def embed_text(txt : str) :
    return embeddings.embed_query(txt)

def embed_chunks(chunks: List[str]) -> List[List[str]]:
    # set proper chunk size
    return embeddings.embed_documents(texts=chunks)
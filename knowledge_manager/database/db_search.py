from .database import isci_zapise, search_data_v2, query_data_v2, query_data_by_id_v2
from .models import BaseEntity
from .validation import *
from . import MILVUS_PUBLIC_USER
from typing import List


@DeprecationWarning
def query(text: str):
    return isci_zapise(text)

# using Milvus nomenclature for methods for v2 - search is with embedding, query is with scalar fields
# TODO add number of entities returned
def search_v2(
    search_str : str, 
    user : str = MILVUS_PUBLIC_USER, 
    type : str | None = None, 
    source :str | None = None) -> List[BaseEntity]:

    """
    Searches for entity based on similarity to search_str embedding,
    filtering result based on user, type, source.
    """
    validate_user(user)
    validate_type(type)
    validate_source(source)
    return search_data_v2(query=search_str, type=type, source=source, user=user)

# TODO add pagination
def query_v2(
    user : str = MILVUS_PUBLIC_USER,
    type : str | None = None,
    source :str | None = None) -> List[BaseEntity]:

    """
    Searches for entity based on user, type, source fields.
    """
    validate_user(user)
    validate_type(type)
    validate_source(source)
    return query_data_v2(type=type, source=source, user=user)

# TODO add pagination
def get_by_ids_v2(
    ids : List[str], 
    user : str = MILVUS_PUBLIC_USER ) -> List[BaseEntity]:

    """
    Searches for entity based on id, only entities belonging to user can be accessed.
    """
    validate_user(user)
    for id in ids:
        validate_id(id)
    return query_data_by_id_v2(ids=ids, user=user)
from typing import BinaryIO
from .database import isci_zapise

def query(text: str):
    return isci_zapise(text)
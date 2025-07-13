from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Final
from enum import Enum
from numpy import float16

# Optional: create enum file for storing enums and import them here if they are many
class FileType:
    MESSAGES : Final[str]="msg"
    TEXT_DOCUMENT : Final[str]="txt"
    TABLE : Final[str]="tbl"
    DOCUMENT : Final[str]="doc"
    JSON : Final[str]="json"

    def list_types(self) -> List[str]:
        return [self.MESSAGES, self.DOCUMENT, self.TABLE, self.TEXT_DOCUMENT, self.JSON]

class FileMetadata (BaseModel):
    model_config = ConfigDict(extra="allow") #allows extra fields (will be added to dynamic field in db schema)

    user: str = "public"
    type: str = FileType.TEXT_DOCUMENT
    # TODO add to schema as static field
    source: str = "unknown" # used to identify the source of the file for update and delete operation
    # should be in form platform|partition|filename
    # | is used as separator as is not allowed in filename and urls
    # add constraints to form of path like allowed characters: A-Za-z0-9/-_@#?:
    # like drive|folder|subfolder|my_doc.docx
    # or discord|my_channel (messages are numerated to distinguish them)

# result of reading from database (this are not)
class BaseEntity(FileMetadata):
    id: Optional[str] # excludes id when creating entity
    embedding: Optional[List[float]] = Field(exclude=True)
    text: str
    # TODO add static field to schema
    position: int = -1 # consecutive number of the chunk, can be used for ordering

# TODO are fields that are unique to each data type, and inherit base entity
# considering the use of dynamic fileds inheritance is not strictly required but can be used to ensure uniform structure
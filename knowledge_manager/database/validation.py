import re
from .models import FileType

class FieldValidationException (Exception):
    def __init__(self, field : str):
        self.field = field
        super().__init__(f"Validation failed on field: {field}")

def validate_user(user : str) -> bool:
    match = re.fullmatch(r"^[A-Za-z0-9_-]+", user)
    if not match:
        raise FieldValidationException("user")
        

def validate_source(source : str) -> bool:
    match = re.fullmatch(r"^([A-Za-z0-9_/:-]+\|){0,2}[A-Za-z0-9_-]+", source)
    if not match:
        raise FieldValidationException("source")

def validate_id(id : str) -> bool:
    match = re.fullmatch(r"^[A-Za-z0-9_-]+", id) # TODO check what form have milvus ids and restrict regex
    if not match:
        raise FieldValidationException("id")

def validate_type(type : str) :
    if type not in FileType.list_types():
        raise FieldValidationException("type")
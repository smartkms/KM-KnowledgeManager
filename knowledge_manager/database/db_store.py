from typing import BinaryIO, List
from fileProcessing.ms_reader import convert_ms
from fileProcessing.pdf_reader import convert_pdf
from fileProcessing.md_splitter import split_onlength
from .database import shrani_podatke, store_data_v2
from .models import FileMetadata, StoreFunctionType

# V2 methods, returns list of created entities ids
def store_file_v2(file : BinaryIO, metadata : FileMetadata, storeFunctionType : StoreFunctionType) -> List[str]:
    match storeFunctionType:
        case StoreFunctionType.PDF:
            plaintext=convert_pdf(file)
        case StoreFunctionType.MS_OFFICE:
            plaintext=convert_ms(file)
        case StoreFunctionType.PLAIN_TEXT:
            plaintext=file.read().decode()
    chunks = split_onlength(plaintext)
    res = store_data_v2(chunks=chunks, metadata=metadata)
    return res


### Funkcija pretvori PDF format v Markdown
### File mora biti odprt v binarni obliki open(path, "rb")
### Deluje na PDF-jih
def store_pdf_files(file: BinaryIO, metadata:  dict[str, str]):
    md = convert_pdf(filestream=file)
    chunks = split_onlength(md)
    keys = []
    for txt in chunks:
        id = shrani_podatke(txt, metadata)
        keys.append(id)
    return keys

### Funkcija pretvori MS Office formate v Markdown
### File mora biti odprt v binarni obliki open(path, "rb")
### Testirani formati: .docx, .xlsx, .pptx
### Lahko interpretira pdf ampak za to raje uporabi pdf_reader funkcije, ker je md bolj kakovosten
@DeprecationWarning
def store_msoffice_files(file: BinaryIO, metadata:  dict[str, str]):
    md = convert_ms(filestream=file)
    chunks = split_onlength(md)
    keys = []
    for txt in chunks:
        id = shrani_podatke(txt, metadata)
        keys.append(id)
    return keys

@DeprecationWarning
def store_text(text: str, metadata : dict[str, str]):
    chunks = split_onlength(text=text)
    keys = []
    for txt in chunks:
        id = shrani_podatke(txt, metadata)
        keys.append(id)
    return keys

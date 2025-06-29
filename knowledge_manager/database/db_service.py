from typing import BinaryIO
from ms_reader import convert_ms
from pdf_reader import convert_pdf
from md_splitter import split_onlength
from database import shrani_podatke, isci_zapise

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
def store_msoffice_files(file: BinaryIO, metadata:  dict[str, str]):
    md = convert_ms(filestream=file)
    chunks = split_onlength(md)
    keys = []
    for txt in chunks:
        id = shrani_podatke(txt, metadata)
        keys.append(id)
    return keys

def store_text(text: str, metadata : dict[str, str]):
    return shrani_podatke(text, metadata)

def query(text: str):
    return isci_zapise(text)
import pymupdf4llm as mupdf
from pymupdf import Document
from typing import BinaryIO


### Funkcija pretvori PDF format v Markdown
### File mora biti odprt v binarni obliki open(path, "rb")
### Deluje na PDF-jih
def convert_pdf(file: BinaryIO) -> str:
    pymupdf_document= Document(stream=file)
    return mupdf.to_markdown(file)


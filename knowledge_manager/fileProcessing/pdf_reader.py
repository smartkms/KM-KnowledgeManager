import pymupdf4llm as mupdf
from typing import BinaryIO


### Funkcija pretvori PDF format v Markdown
### File mora biti odprt v binarni obliki open(path, "rb")
### Deluje na PDF-jih
def convert_pdf(file: BinaryIO) -> str:
    return mupdf.to_markdown(file)


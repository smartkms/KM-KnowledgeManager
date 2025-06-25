import pymupdf4llm as mupdf
from typing import BinaryIO


### Funkcija pretvori PDF format v Markdown
### File mora biti odprt v binarni obliki open(path, "rb")
### Deluje na PDF-jih
def convert_pdf(file: BinaryIO) -> str:
    return mupdf.to_markdown(file)


# dwnpath = "C:\\Users\\peter\\Downloads\\"

### TODO Ustavrit MuPDF document iz BinaryIO

# pdfile = open("c.pdf", mode="rb")
# md = mupdf.to_markdown(pdfile)

# print(md)

# from langchain_pymu
# pdf4llm import PyMuPDF4LLMLoader

# path = "./a.pdf"
# loader = PyMuPDF4LLMLoader(path, mode="single")
# doc = loader.load()

# print(doc[0].page_content)

# from langchain_community.document_loaders import PDFMinerLoader

# path = "./a.pdf"
# loader = PDFMinerLoader(path, mode="single")
# doc = loader.load()

# print(doc[0].page_content[0:100])


from langchain_text_splitters import MarkdownTextSplitter, MarkdownHeaderTextSplitter
from langchain_core import documents

splitter = MarkdownTextSplitter()
splitterh = MarkdownHeaderTextSplitter(headers_to_split_on=[
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
    ("####", "Header 4"),
    ("#####", "Header 5"),
    ("######", "Header 6"),
])

def split_onlength(text: str) -> list[str] :
    return splitter.split_text(text=text)

def split_onheaders(text: str) -> list[documents.Document]:
    return splitterh.split_text(text=text)
    # returns Document, documents should be converted to str
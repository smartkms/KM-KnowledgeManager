from markitdown import MarkItDown
from typing import BinaryIO

### Funkcija pretvori MS Office formate v Markdown
### File mora biti odprt v binarni obliki open(path, "rb")
### Testirani formati: .docx, .xlsx, .pptx
### Lahko interpretira pdf ampak za to raje uporabi pdf_reader funkcije, ker je md bolj kakovosten
md = MarkItDown(enable_plugins=False) # Set to True to enable plugins
def convert_ms(filestream : BinaryIO) -> str:
    return md.convert(filestream)

# file = open("b.docx", mode="rb")
# md = MarkItDown(enable_plugins=False) # Set to True to enable plugins
# result = md.convert(file)
# print(result.text_content)


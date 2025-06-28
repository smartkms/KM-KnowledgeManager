# kms-db-service
Program deluje na Windowsih samo v okrnjeni obliki: MilvusLite ni na razpolago in tudi markitdown. Raje zaženite program na WSL-ju.
## Potrbni uporabški računi
Da embeddingi delujejo, je potrebno imeti odprt plačniški račun pri podjetju OpenAI. 
## .env file
Primer podatkov v datoteki. Podatki veyani na googlove storitve so potrebni, če uporabljaš Gemini LLM model ali VertexAI embeddinge.
```
GOOGLE_API_KEY=asdfghjkl
GOOGLE_APPLICATION_CREDENTIALS=C:\Path\to\gcloud\application_default_credentials.json
OPENAI_API_KEY=sk-proj-asdfghjkl
VECTOR_DB_URI=http://localhost:19530
```
## Uporaba
Vse potrebne funkcije so v **db_service**. *query* in *store_text* sprejmejo vsebino, ki se bo shranila v podatkovno bazo kot navadne nize. *store_pdf_files* in *store_msoffice_files* sprejmejo kot vsebino, ki bo hranjena v podatkovni bazi datatoke odprte kot tok bajtov, npr. z uporabo funkcije:
```
open("path/to/something.pdf", "rb")
```
**Važno je, da so dokumenti odprti v binarni obliki in NE v tekstovni.**
Metapodatki so podani kot slovar(niz, niz) npr.:
```
metadata = dict(avtor="Peter", leto="2025", type="pdf document")
```

## Database
Možna sta dva načina uporabe vektorske podatkovne baze: lokalno s shranjevanjem trajnega stanja kar direktno v .db datoteko, ali s povezavo na vsebnik z Milvus/Zillis sliko.
### Lokalna vektorska podatkovna baza
Če ne spreminjaš že napisane kode se bo zagnala lokalna podatkovna baza - MilvusLite.
Potrebno je imeti Linux ali Mac računalnik, drugače program ne bo deloval. Podatki se bodo shranili v *milvus_local.db* datoteko. Ne vse napredne funkcionalnosti so omogočene. Če se ima potrebo le po neki osnovni implementaciji podatkovne baze je ta implementacija zadostna.
### Hostana podatkovna baza
V primeru, da želiš uporabljati vse napredne funkcionalnosti vektorske podatkovne baze, lahko zaženeš *milvus-standalone-docker-compose.yaml* in se bo v lokalnem dockerju zagnala slika Milvus DB. V .env pravilno nastavi *VECTOR_DB_URI*.
### Embeddings
Če se za ponudnika embeddingov želi uporabljati VertexAI, je dovolj, da se med importi nadomesti:
```
from embedding_openai import embeddings
```
z:
```
from embedding_vertexai import embeddings
```
Da to deluje je potrebno imeti billing account pri Googlu in pravilno nastavljene *GOOGLE_API_KEY* in *GOOGLE_APPLICATION_CREDENTIALS* okoljske spremenljivke.

## Ostale komponente
### Bralci dokumentov
Trenutno so bralci dokumentov tako nastavljeni, da dobijo že odprto datoteko v načinu "rb" (read binary) in berejo tok bajtov. Za pdf se uporablja ločeno knjižnico, ker je bolj performantna. Za MS office formate se uporablja knjižnico, ki jih lahko vse obravnava. Dokumenti so pretvorjeni v Markdown.
### Splitterji
Trenutno se uporablja splitter, ki deli Markdown tekst v kose na podlagi števila znakov. Kmalu bo na voljo splitter, ki loči po headerjih.

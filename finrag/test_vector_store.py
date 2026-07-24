from finrag.loader import load_document
from finrag.splitter import split_text
from finrag.embedding import embedding_model
from finrag.vector_store import create_vector_store

text = load_document("docs/vat_law.txt")

chunks = split_text(text)

vector_store = create_vector_store(
    chunks,
    embedding_model
)

print(vector_store)
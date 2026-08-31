from finrag.loader import load_document
from finrag.splitter import split_text
from finrag.embedding import embedding_model
from finrag.vector_store import create_vector_store
from finrag.retriever import create_retriever

text = load_document("docs/vat_law.txt")

chunks = split_text(text)

vector_store = create_vector_store(
    chunks,
    embedding_model
)

retriever = create_retriever(vector_store)

results = retriever.invoke(
    "Thuế giá trị gia tăng là gì?"
)

for i, doc in enumerate(results, start=1):
    print(f"\n===== Chunk {i} =====")
    print(doc.page_content)
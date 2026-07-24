from finrag.loader import load_documents

docs = load_documents("data/knowledge")

print("=" * 60)
print(f"Total documents: {len(docs)}")
print("=" * 60)

print(docs[0].metadata)
print()
print(docs[0].page_content[:1000])
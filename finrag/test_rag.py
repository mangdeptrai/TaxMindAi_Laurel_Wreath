from finrag.splitter import split_documents
print("Splitting documents...")
chunks = split_documents(documents)

print(len(chunks))

chunks = chunks[:3]
from finrag.loader import load_documents
from finrag.splitter import split_documents


def main():

    docs = load_documents("data/knowledge")
    print("Số document:", len(docs))
    print("Độ dài page đầu tiên:", len(docs[0].page_content))
    print(repr(docs[0].page_content[:300]))
    chunks = split_documents(docs)

    print("=" * 60)
    print(f"Total pages : {len(docs)}")
    print(f"Total chunks: {len(chunks)}")
    print("=" * 60)

    print("\nMetadata:")
    print(chunks[0].metadata)

    print("\nContent:")
    print(chunks[0].page_content[:500])


if __name__ == "__main__":
    main()
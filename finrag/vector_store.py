from langchain_community.vectorstores import FAISS


def create_vector_store(chunks, embedding_model):
    """
    Tạo Vector Store từ danh sách Document.
    """

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    return vector_store
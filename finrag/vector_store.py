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

def load_vector_store(folder_path, embedding_model):
    """
    Tải Vector Store đã được lưu sẵn trên máy.
    """
    vector_store = FAISS.load_local(
        folder_path=folder_path, 
        embeddings=embedding_model, 
        allow_dangerous_deserialization=True
    )
    return vector_store
import os
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_retriever(vector_store=None, search_k=12, *args, **kwargs):
    if vector_store is None:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        db_path = os.path.join(BASE_DIR, "data")
        
        vector_store = FAISS.load_local(
            folder_path=db_path,
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )
        
    # SỬ DỤNG CHẾ ĐỘ TÌM KIẾM MMR ĐỂ ĐA DẠNG HÓA VĂN BẢN TRẢ VỀ
    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 12,
            "fetch_k": 30,      # Quét 30 chunks có điểm tương đồng cao nhất
            "lambda_mult": 0.5  # Cân bằng 50% độ liên quan và 50% tính đa dạng các file
        }
    )
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

# Import hàm đọc PDF
from finrag.ocr import ocr_pdf 

def build_vector_database():
    print("1. Đang quét và đọc TẤT CẢ tài liệu PDF trong thư mục data/knowledge...")
    
    knowledge_dir = "data/knowledge"
    documents = []

    if os.path.exists(knowledge_dir):
        # Dùng os.walk để quét toàn bộ thư mục con (laws, decrees, circulars, letters...)
        for root, dirs, files in os.walk(knowledge_dir):
            for file in files:
                if file.endswith(".pdf"):
                    file_path = os.path.join(root, file)
                    print(f" -> Đang đọc file: {file_path}")
                    try:
                        docs = ocr_pdf(file_path)
                        # Lưu thuộc tính source chuẩn hóa
                        for doc in docs:
                            doc.metadata["source"] = file_path
                        documents.extend(docs)
                    except Exception as e:
                        print(f"   [Lỗi] Không thể đọc file {file_path}: {e}")
    else:
        print(f"[Cảnh báo] Không tìm thấy thư mục {knowledge_dir}!")

    print(f"\nTổng số trang tài liệu đã nạp: {len(documents)}")

    if len(documents) == 0:
        print("❌ Không tìm thấy tài liệu PDF nào để build database!")
        return

    print("2. Đang chia nhỏ văn bản (chunking)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Tổng số chunks tạo ra: {len(chunks)}")

    print("3. Đang tạo Vector Database với Ollama Embeddings...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = FAISS.from_documents(chunks, embeddings)

    print("4. Đang lưu 2 file index vào thư mục 'data'...")
    output_dir = "data"
    vector_store.save_local(output_dir) 
    print(f"✅ Hoàn thành! Đã tạo xong index.faiss và index.pkl trong thư mục '{output_dir}'.")

if __name__ == "__main__":
    build_vector_database()
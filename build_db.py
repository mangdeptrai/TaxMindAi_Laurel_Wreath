from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

# Import file ocr.py từ trong thư mục finrag
from finrag.ocr import ocr_pdf 

def build_vector_database():
    print("1. Đang quét OCR và đọc tài liệu PDF...")
    
    # Thêm 'data/' vào trước tên file để trỏ đúng vào thư mục chứa tài liệu
    # Trỏ đường dẫn xuyên qua các thư mục con
    docs1 = ocr_pdf("data/knowledge/laws/law_vat.pdf") # File luật GTGT
    docs2 = ocr_pdf("data/knowledge/laws/law_cit.pdf") # File luật TNDN
    
    # Gộp nội dung 2 file
    documents = docs1 + docs2

    print("2. Đang chia nhỏ văn bản...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    print("3. Đang mã hóa và tạo FAISS Database...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = FAISS.from_documents(chunks, embeddings)

    print("4. Đang lưu Database xuống máy...")
    vector_store.save_local("db_thuemwg") 
    print("Hoàn thành! Đã tạo thư mục db_thuemwg.")

if __name__ == "__main__":
    build_vector_database()
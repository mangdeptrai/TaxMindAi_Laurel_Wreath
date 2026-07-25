import sys
import config
from finrag.retriever import create_retriever
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

# 1. Module Quyết định (Decision)
from decision import advisor
from decision import prompt_builder

# 2. Module RAG Tài chính (Finrag)
from finrag import rag_chain 

# 3. Module Dự báo (Forecasting)
from forecasting import forecast

# 4. Module Mô phỏng Montecarlo
from montecarlo import simulation as mc_simulation 

# 5. Module Kịch bản Mô phỏng (Simulation)
from simulation import scenario

# 6. Module Thuế (Taxtwin)
from taxtwin import calculator
from taxtwin import models

def init_system():
    """Khởi tạo hệ thống"""
    print("="*50)
    print(" ĐANG KHỞI ĐỘNG HỆ THỐNG TAXMINDAI LAUREL WREATH ")
    print("="*50)

def main():
    init_system()
    
    while True:
        print("\n--- CHỌN MODULE ĐỂ CHẠY ---")
        print("1. Cố vấn Quyết định (Decision Advisor)")
        print("2. Truy xuất tài liệu (FinRAG)")
        print("3. Dự báo tài chính (Forecasting)")
        print("4. Mô phỏng Montecarlo")
        print("5. Phân tích kịch bản Thuế (Taxtwin)")
        print("0. Thoát")
        
        choice = input("\nNhập lựa chọn của bạn (0-5): ")
        
        if choice == '1':
            print("\n[Đang chạy Module Decision...]")
            # TODO: Thay bằng hàm thực tế
            input("\n[Hoàn thành] Nhấn Enter để quay lại menu chính...")
            
        elif choice == '2':
            print("\n[Đang chạy Module FinRAG...]")
            user_question = input("Nhập câu hỏi về Thuế của bạn (hoặc gõ '0' để thoát): ")
            
            if user_question != '0':
                try:
                    # 1. Import các hàm cần thiết ngay tại đây
                    from langchain_community.embeddings import OllamaEmbeddings
                    from finrag.vector_store import load_vector_store
                    
                    # 2. Khởi tạo mô hình nhúng (Embeddings)
                    embeddings = OllamaEmbeddings(model="nomic-embed-text")
                    
                    # 3. Tải Database
                    # LƯU Ý: Thay "thu_muc_chua_faiss_index" bằng tên thư mục chứa file .faiss của bạn
                    vector_store = load_vector_store("vector_store", embeddings)
                    
                    # 4. Khởi tạo Retriever
                    my_retriever = create_retriever(vector_store) 
                    
                    print("\nĐang suy nghĩ và tra cứu tài liệu...")
                    result = rag_chain.ask_question(question=user_question, retriever=my_retriever)
                    
                    print("\n=== AI TƯ VẤN THUẾ ===")
                    print(result["answer"])
                    print("========================\n")
                    
                except Exception as e:
                    print(f"\n[Lỗi] Đã xảy ra vấn đề khi chạy FinRAG: {e}")

            input("\n[Hoàn thành] Nhấn Enter để quay lại menu chính...")

        elif choice == '3':
            print("\n[Đang chạy Module Forecasting...]")
            input("\n[Hoàn thành] Nhấn Enter để quay lại menu chính...")

        elif choice == '4':
            print("\n[Đang chạy Module Montecarlo...]")
            input("\n[Hoàn thành] Nhấn Enter để quay lại menu chính...")

        elif choice == '5':
            print("\n[Đang chạy Module Taxtwin...]")
            input("\n[Hoàn thành] Nhấn Enter để quay lại menu chính...")
            
        elif choice == '0':
            print("\nĐã thoát hệ thống. Tạm biệt!")
            sys.exit()
            
        else:
            print("\nLựa chọn không hợp lệ, vui lòng nhập số từ 0 đến 5.")
            input("\nNhấn Enter để thử lại...")

if __name__ == "__main__":
    main()
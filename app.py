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
                    vector_store = load_vector_store("db_thuemwg", embeddings)
                    
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
            print("\n[ĐANG CHẠY MODULE MONTE CARLO]")

            try:
                import csv
                from montecarlo.simulation import (
                    monte_carlo,
                    summarize_results,
                    calculate_percentiles
                )

                # Đọc danh sách doanh nghiệp
                companies = []

                with open(
                    "data/company/company.csv",
                    "r",
                    encoding="utf-8"
                ) as file:
                    reader = csv.DictReader(file)

                    for row in reader:
                        company = models.Company(
                            company_name=row["company_name"],
                            revenue=float(row["revenue"]),
                            cost=float(row["cost"]),
                            vat_input=float(row["vat_input"]),
                            vat_output=float(row["vat_output"])
                        )

                        companies.append(company)

                # Hiển thị doanh nghiệp
                print("\n--- CHỌN DOANH NGHIỆP ---")

                for i, company in enumerate(companies, 1):
                    print(f"{i}. {company.company_name}")

                company_choice = int(
                    input("\nChọn doanh nghiệp: ")
                )

                company = companies[company_choice - 1]

                # Nhập số lần mô phỏng
                num_simulations = int(
                    input("Nhập số lần mô phỏng: ")
                )

                print(
                    f"\nĐang thực hiện {num_simulations} "
                    f"lần mô phỏng cho {company.company_name}..."
                )

                # Chạy Monte Carlo
                results = monte_carlo(
                    company,
                    num_simulations
                )

                # Thống kê
                summary = summarize_results(results)
                percentiles = calculate_percentiles(results)

                print("\n========== KẾT QUẢ MONTE CARLO ==========")

                print(
                    f"Doanh nghiệp: {company.company_name}"
                )

                print(
                    f"Giá trị CIT trung bình: "
                    f"{summary['average_cit']:,.0f} VND"
                )

                print(
                    f"Độ lệch chuẩn CIT: "
                    f"{summary['std_cit']:,.0f} VND"
                )

                print(
                    f"CIT thấp nhất: "
                    f"{summary['min_cit']:,.0f} VND"
                )

                print(
                    f"CIT cao nhất: "
                    f"{summary['max_cit']:,.0f} VND"
                )

                print(
                    f"P5: "
                    f"{percentiles['p5']:,.0f} VND"
                )

                print(
                    f"Median (P50): "
                    f"{percentiles['p50']:,.0f} VND"
                )

                print(
                    f"P95: "
                    f"{percentiles['p95']:,.0f} VND"
                )

                print("==========================================")

            except Exception as e:
                print(
                    f"\n[Lỗi] Đã xảy ra vấn đề "
                    f"khi chạy Monte Carlo: {e}"
                )

            input(
                "\n[Hoàn thành] Nhấn Enter "
                "để quay lại menu chính..."
            )

        elif choice == '5':
            print("\n[ĐANG CHẠY MODULE TAXTWIN]")

            try:
                    import csv
                    from simulation.scenario import simulate_forecast

                    # Đọc danh sách doanh nghiệp
                    companies = []

                    with open(
                        "data/company/company.csv",
                        "r",
                        encoding="utf-8"
                    ) as file:
                        reader = csv.DictReader(file)

                        for row in reader:
                            company = models.Company(
                                company_name=row["company_name"],
                                revenue=float(row["revenue"]),
                                cost=float(row["cost"]),
                                vat_input=float(row["vat_input"]),
                                vat_output=float(row["vat_output"])
                            )

                            companies.append(company)

                    # Chọn doanh nghiệp
                    print("\n--- CHỌN DOANH NGHIỆP ---")

                    for i, company in enumerate(companies, 1):
                        print(f"{i}. {company.company_name}")

                    company_choice = int(
                        input("\nChọn doanh nghiệp: ")
                    )

                    company = companies[company_choice - 1]

                    # Thông tin hiện tại
                    current_profit = calculator.calculate_profit(company)
                    current_vat = calculator.calculate_vat(company)
                    current_cit = calculator.calculate_cit(company)

                    print("\n--- TÌNH TRẠNG HIỆN TẠI ---")

                    print(
                        f"Doanh thu: "
                        f"{company.revenue:,.0f} VND"
                    )

                    print(
                        f"Chi phí: "
                        f"{company.cost:,.0f} VND"
                    )

                    print(
                        f"Lợi nhuận: "
                        f"{current_profit:,.0f} VND"
                    )

                    print(
                        f"VAT: "
                        f"{current_vat:,.0f} VND"
                    )

                    print(
                        f"CIT: "
                        f"{current_cit:,.0f} VND"
                    )

                    # Nhập kịch bản
                    revenue_percent = float(
                        input(
                            "\nNhập % thay đổi doanh thu: "
                        )
                    )

                    cost_percent = float(
                        input(
                            "Nhập % thay đổi chi phí: "
                        )
                    )

                    print("\nĐang phân tích kịch bản...")

                    # Tạo doanh nghiệp sau kịch bản
                    future = simulate_forecast(
                        company,
                        revenue_percent,
                        cost_percent
                    )

                    future_profit = calculator.calculate_profit(
                        future
                    )

                    future_vat = calculator.calculate_vat(
                        future
                    )

                    future_cit = calculator.calculate_cit(
                        future
                    )

                    # Hiển thị kết quả
                    print("\n========== KẾT QUẢ TAXTWIN ==========")

                    print(f"\nDoanh nghiệp: {company.company_name}")

                    print("\n                 HIỆN TẠI          KỊCH BẢN")

                    print(
                        f"Doanh thu:       "
                        f"{company.revenue:>15,.0f}   "
                        f"{future.revenue:>15,.0f}"
                    )

                    print(
                        f"Chi phí:         "
                        f"{company.cost:>15,.0f}   "
                        f"{future.cost:>15,.0f}"
                    )

                    print(
                        f"Lợi nhuận:       "
                        f"{current_profit:>15,.0f}   "
                        f"{future_profit:>15,.0f}"
                    )

                    print(
                        f"VAT:             "
                        f"{current_vat:>15,.0f}   "
                        f"{future_vat:>15,.0f}"
                    )

                    print(
                        f"CIT:             "
                        f"{current_cit:>15,.0f}   "
                        f"{future_cit:>15,.0f}"
                    )

                    print("\n--- THAY ĐỔI ---")

                    print(
                        f"Lợi nhuận thay đổi: "
                        f"{future_profit - current_profit:,.0f} VND"
                    )

                    print(
                        f"CIT thay đổi: "
                        f"{future_cit - current_cit:,.0f} VND"
                    )

                    print("======================================")

            except Exception as e:
                    print(
                        f"\n[Lỗi] Đã xảy ra vấn đề "
                        f"khi chạy Taxtwin: {e}"
                    )

            input(
                    "\n[Hoàn thành] Nhấn Enter "
                    "để quay lại menu chính..."
                )
            
        elif choice == '0':
            print("\nĐã thoát hệ thống. Tạm biệt!")
            sys.exit()
            
        else:
            print("\nLựa chọn không hợp lệ, vui lòng nhập số từ 0 đến 5.")
            input("\nNhấn Enter để thử lại...")

if __name__ == "__main__":
    main()
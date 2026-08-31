import sys
import os
from datetime import date

import config
from finrag.retriever import create_retriever
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

# Xác định thư mục gốc chứa file app.py để tạo đường dẫn tương đối an toàn
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
    print("=" * 50)
    print(" ĐANG KHỞI ĐỘNG HỆ THỐNG TAXMINDAI LAUREL WREATH ")
    print("=" * 50)


VAN_BAN_INFO = {
    "data/knowledge/laws/law_vat.pdf": {
        "loai": "Luat",
        "ten": "Luật Thuế Giá trị gia tăng số 48/2024/QH15",
        "hieu_luc_tu": date(2025, 7, 1),
        "het_hieu_luc": None,
    },
    "data/knowledge/laws/law_cit.pdf": {
        "loai": "Luat",
        "ten": "Luật Thuế Thu nhập doanh nghiệp số 67/2025/QH15",
        "hieu_luc_tu": date(2025, 10, 1),
        "het_hieu_luc": None,
    },
    "data/knowledge/decrees/decree_70.pdf": {
        "loai": "Nghi dinh",
        "ten": "Nghị định số 68/2026/NĐ-CP (thuế hộ/cá nhân kinh doanh)",
        "hieu_luc_tu": date(2026, 3, 5),
        "het_hieu_luc": None,
    },
    "data/knowledge/circulars/circular_80.pdf": {
        "loai": "Thong tu",
        "ten": "Thông tư số 20/2026/TT-BTC (hướng dẫn Luật Thuế TNDN)",
        "hieu_luc_tu": date(2026, 3, 12),
        "het_hieu_luc": None,
    },
    "data/knowledge/letters/letter.pdf": {
        "loai": "Cong van",
        "ten": "Công văn số 4226/CT-NVT (hướng dẫn quyết toán thuế TNCN)",
        "hieu_luc_tu": date(2026, 5, 1),
        "het_hieu_luc": None,
    },
}

THU_TU_UU_TIEN = {"Luat": 1, "Nghi dinh": 2, "Thong tu": 3, "Cong van": 4}


def kiem_tra_hieu_luc(info):
    """Tra ve chuoi mo ta trang thai hieu luc dua tren ngay hien tai."""
    hom_nay = date.today()
    if info["hieu_luc_tu"] and hom_nay < info["hieu_luc_tu"]:
        return f"CHUA có hiệu lực (áp dụng từ {info['hieu_luc_tu'].strftime('%d/%m/%Y')})"
    if info["het_hieu_luc"] and hom_nay > info["het_hieu_luc"]:
        return f"ĐÃ HẾT hiệu lực (từ {info['het_hieu_luc'].strftime('%d/%m/%Y')})"
    return f"Còn hiệu lực (áp dụng từ {info['hieu_luc_tu'].strftime('%d/%m/%Y')})"


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
            try:
                from taxtwin.loader import load_company
                from montecarlo.simulation import (
                    monte_carlo,
                    summarize_results,
                    probability_over,
                    calculate_percentiles,
                )
                from decision.prompt_builder import build_prompt
                from finrag.llm import get_llm

                company_file = os.path.join(BASE_DIR, "data", "company", "company.csv")
                companies = load_company(company_file)
                print("\nCác doanh nghiệp có trong dữ liệu:")
                for i, c in enumerate(companies):
                    print(f"{i + 1}. {c.company_name}")

                idx = int(input("Chọn doanh nghiệp (nhập số thứ tự): ")) - 1
                company = companies[idx]

                print(f"\nĐang mô phỏng Monte Carlo cho '{company.company_name}'...")
                results = monte_carlo(company, 1000)
                summary = summarize_results(results)
                probability = probability_over(results, 900_000_000)
                percentiles = calculate_percentiles(results)

                prompt = build_prompt(summary, probability, percentiles)

                print("\nĐang nhờ AI viết báo cáo...")
                llm = get_llm()
                response = llm.invoke(prompt)

                print("\n=== BÁO CÁO CỐ VẤN THUẾ ===")
                print(response.content)
                print("========================\n")

            except Exception as e:
                print(f"\n[Lỗi] Đã xảy ra vấn đề khi chạy Decision Advisor: {e}")

            input("\n[Hoàn thành] Nhấn Enter để quay lại menu chính...")

        elif choice == '2':
            print("\n[Đang chạy Module FinRAG...]")
            user_question = input("Nhập câu hỏi về Thuế của bạn (hoặc gõ '0' để thoát): ")

            if user_question != '0':
                try:
                    from finrag.vector_store import load_vector_store

                    embeddings = OllamaEmbeddings(model="nomic-embed-text")

                    db_path = os.path.join(BASE_DIR, "db_thuemwg")
                    vector_store = load_vector_store(db_path, embeddings)

                    my_retriever = create_retriever(vector_store)

                    print("\nĐang suy nghĩ và tra cứu tài liệu...")
                    result = rag_chain.ask_question(question=user_question, retriever=my_retriever)

                    print("\n=== AI TƯ VẤN THUẾ ===")
                    print(result["answer"])
                    print("\n--- CĂN CỨ PHÁP LÝ (theo thứ bậc: Luật → Nghị định → Thông tư → Công văn) ---")

                    seen = set()
                    nguon_dung = []
                    for doc in result["documents"]:
                        src = doc.metadata.get("source", "")
                        page = doc.metadata.get("page", "?")
                        info = VAN_BAN_INFO.get(src)
                        if not info:
                            continue
                        key = (src, page)
                        if key in seen:
                            continue
                        seen.add(key)
                        nguon_dung.append((info, page))

                    nguon_dung.sort(key=lambda x: THU_TU_UU_TIEN.get(x[0]["loai"], 99))

                    for info, page in nguon_dung:
                        trang_thai = kiem_tra_hieu_luc(info)
                        print(f"- {info['ten']}, trang {page}")
                        print(f"    Tinh trang: {trang_thai}")

                    print("========================\n")

                except Exception as e:
                    print(f"\n[Lỗi] Đã xảy ra vấn đề khi chạy FinRAG: {e}")

            input("\n[Hoàn thành] Nhấn Enter để quay lại menu chính...")

        elif choice == '3':
            print("\n[Đang chạy Module Forecasting...]")
            try:
                from taxtwin.loader import load_company
                from taxtwin.calculator import calculate_vat, calculate_cit
                from forecasting.forecast import forecast_company

                company_file = os.path.join(BASE_DIR, "data", "company", "company.csv")
                companies = load_company(company_file)
                print("\nCác doanh nghiệp có trong dữ liệu:")
                for i, c in enumerate(companies):
                    print(f"{i + 1}. {c.company_name}")

                idx = int(input("Chọn doanh nghiệp (nhập số thứ tự): ")) - 1
                company = companies[idx]

                revenue_growth = float(input("Nhập % tăng trưởng doanh thu dự kiến (ví dụ 0.15 cho 15%): "))
                cost_growth = float(input("Nhập % tăng trưởng chi phí dự kiến (ví dụ 0.08 cho 8%): "))

                future = forecast_company(company, revenue_growth, cost_growth)

                print(f"\n===== DỰ BÁO CHO '{future.company_name}' =====")
                print(f"Doanh thu dự kiến : {future.revenue:,.0f}")
                print(f"Chi phí dự kiến   : {future.cost:,.0f}")
                print(f"VAT dự kiến       : {calculate_vat(future):,.0f}")
                print(f"CIT (TNDN) dự kiến: {calculate_cit(future):,.0f}")
                print("========================\n")

            except Exception as e:
                print(f"\n[Lỗi] Đã xảy ra vấn đề khi chạy Forecasting: {e}")

            input("\n[Hoàn thành] Nhấn Enter để quay lại menu chính...")

        elif choice == '4':
            print("\n[ĐANG CHẠY MODULE MONTE CARLO]")
            try:
                import csv
                from montecarlo.simulation import (
                    monte_carlo,
                    summarize_results,
                    calculate_percentiles,
                )

                companies = []
                company_file = os.path.join(BASE_DIR, "data", "company", "company.csv")

                with open(company_file, "r", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        company = models.Company(
                            company_name=row["company_name"],
                            revenue=float(row["revenue"]),
                            cost=float(row["cost"]),
                            vat_input=float(row["vat_input"]),
                            vat_output=float(row["vat_output"]),
                        )
                        companies.append(company)

                print("\n--- CHỌN DOANH NGHIỆP ---")
                for i, company in enumerate(companies, 1):
                    print(f"{i}. {company.company_name}")

                company_choice = int(input("\nChọn doanh nghiệp: "))
                company = companies[company_choice - 1]

                num_simulations = int(input("Nhập số lần mô phỏng: "))
                print(f"\nĐang thực hiện {num_simulations} lần mô phỏng cho {company.company_name}...")

                results = monte_carlo(company, num_simulations)
                summary = summarize_results(results)
                percentiles = calculate_percentiles(results)

                print("\n========== KẾT QUẢ MONTE CARLO ==========")
                print(f"Doanh nghiệp: {company.company_name}")
                print(f"Giá trị CIT trung bình: {summary['average_cit']:,.0f} VND")
                print(f"Độ lệch chuẩn CIT: {summary['std_cit']:,.0f} VND")
                print(f"CIT thấp nhất: {summary['min_cit']:,.0f} VND")
                print(f"CIT cao nhất: {summary['max_cit']:,.0f} VND")
                print(f"P5: {percentiles['p5']:,.0f} VND")
                print(f"Median (P50): {percentiles['p50']:,.0f} VND")
                print(f"P95: {percentiles['p95']:,.0f} VND")
                print("==========================================")

            except Exception as e:
                print(f"\n[Lỗi] Đã xảy ra vấn đề khi chạy Monte Carlo: {e}")

            input("\n[Hoàn thành] Nhấn Enter để quay lại menu chính...")

        elif choice == '5':
            print("\n[ĐANG CHẠY MODULE TAXTWIN]")

            try:
                import csv
                from simulation.scenario import simulate_forecast

                companies = []
                company_file = os.path.join(BASE_DIR, "data", "company", "company.csv")

                with open(company_file, "r", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        company = models.Company(
                            company_name=row["company_name"],
                            revenue=float(row["revenue"]),
                            cost=float(row["cost"]),
                            vat_input=float(row["vat_input"]),
                            vat_output=float(row["vat_output"]),
                        )
                        companies.append(company)

                print("\n--- CHỌN DOANH NGHIỆP ---")
                for i, company in enumerate(companies, 1):
                    print(f"{i}. {company.company_name}")

                company_choice = int(input("\nChọn doanh nghiệp: "))
                company = companies[company_choice - 1]

                current_profit = calculator.calculate_profit(company)
                current_vat = calculator.calculate_vat(company)
                current_cit = calculator.calculate_cit(company)

                print("\n--- TÌNH TRẠNG HIỆN TẠI ---")
                print(f"Doanh thu: {company.revenue:,.0f} VND")
                print(f"Chi phí: {company.cost:,.0f} VND")
                print(f"Lợi nhuận: {current_profit:,.0f} VND")
                print(f"VAT: {current_vat:,.0f} VND")
                print(f"CIT: {current_cit:,.0f} VND")

                revenue_percent = float(input("\nNhập % thay đổi doanh thu: "))
                cost_percent = float(input("Nhập % thay đổi chi phí: "))

                print("\nĐang phân tích kịch bản...")
                future = simulate_forecast(company, revenue_percent, cost_percent)

                future_profit = calculator.calculate_profit(future)
                future_vat = calculator.calculate_vat(future)
                future_cit = calculator.calculate_cit(future)

                print("\n========== KẾT QUẢ TAXTWIN ==========")
                print(f"\nDoanh nghiệp: {company.company_name}")
                print("\n                 HIỆN TẠI          KỊCH BẢN")
                print(f"Doanh thu:       {company.revenue:>15,.0f}   {future.revenue:>15,.0f}")
                print(f"Chi phí:         {company.cost:>15,.0f}   {future.cost:>15,.0f}")
                print(f"Lợi nhuận:       {current_profit:>15,.0f}   {future_profit:>15,.0f}")
                print(f"VAT:             {current_vat:>15,.0f}   {future_vat:>15,.0f}")
                print(f"CIT:             {current_cit:>15,.0f}   {future_cit:>15,.0f}")

                print("\n--- THAY ĐỔI ---")
                print(f"Lợi nhuận thay đổi: {future_profit - current_profit:,.0f} VND")
                print(f"CIT thay đổi: {future_cit - current_cit:,.0f} VND")
                print("======================================")

            except Exception as e:
                print(f"\n[Lỗi] Đã xảy ra vấn đề khi chạy Taxtwin: {e}")

            input("\n[Hoàn thành] Nhấn Enter để quay lại menu chính...")

        elif choice == '0':
            print("\nĐã thoát hệ thống. Tạm biệt!")
            sys.exit()

        else:
            print("\nLựa chọn không hợp lệ, vui lòng nhập số từ 0 đến 5.")
            input("\nNhấn Enter để thử lại...")


if __name__ == "__main__":
    main()
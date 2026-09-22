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

                company_file = os.path.join(BASE_DIR, "data", "company", "DuLieuMoPhong_ChuoiBanLe_FinRAG.xlsx")
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

                company_file = os.path.join(BASE_DIR, "data", "company", "DuLieuMoPhong_ChuoiBanLe_FinRAG.xlsx")
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
                company_file = os.path.join(BASE_DIR, "data", "company", "DuLieuMoPhong_ChuoiBanLe_FinRAG.xlsx")

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
                import pandas as pd

                from taxtwin.loader import load_company
                from taxtwin.calculator import calculate_profit, calculate_cit
                from simulation.scenario import (
                    simulate_revenue_increase,
                    simulate_operating_cost_reduction,
                    simulate_cogs_reduction
                )

                # ==========================================
                # ĐƯỜNG DẪN DỮ LIỆU
                # ==========================================

                company_file = os.path.join(
                    BASE_DIR,
                    "data",
                    "company",
                    "DuLieuMoPhong_ChuoiBanLe_FinRAG.xlsx"
                )

                # ==========================================
                # ĐỌC DỮ LIỆU KẾT QUẢ KINH DOANH
                # ==========================================

                companies = load_company(company_file)

                # ==========================================
                # ĐỌC DANH MỤC CỬA HÀNG
                # Header nằm ở dòng 4 của Excel
                # ==========================================

                store_df = pd.read_excel(
                    company_file,
                    sheet_name="DM_CuaHang",
                    header=3
                )

                # Tạo dictionary:
                # Mã cửa hàng -> Tên cửa hàng
                store_names = dict(
                    zip(
                        store_df["Mã CH"].astype(str),
                        store_df["Tên cửa hàng"].astype(str)
                    )
                )

                # ==========================================
                # LẤY DANH SÁCH CỬA HÀNG
                # ==========================================

                store_ids = sorted(
                    set(
                        company.store_id
                        for company in companies
                    )
                )

                print("\n--- DANH SÁCH CỬA HÀNG ---")

                for i, store_id in enumerate(store_ids, 1):

                    store_name = store_names.get(
                        store_id,
                        "Không có tên"
                    )

                    print(
                        f"{i}. {store_name} ({store_id})"
                    )

                print(
                    f"\nTổng số cửa hàng có dữ liệu: "
                    f"{len(store_ids)}"
                )

                # ==========================================
                # CHỌN CỬA HÀNG
                # ==========================================

                store_choice = int(
                    input(
                        f"\nChọn cửa hàng (1-{len(store_ids)}): "
                    )
                )

                if (
                    store_choice < 1
                    or store_choice > len(store_ids)
                ):
                    raise ValueError(
                        "Lựa chọn cửa hàng không hợp lệ."
                    )

                selected_store_id = store_ids[
                    store_choice - 1
                ]

                selected_store_name = store_names.get(
                    selected_store_id,
                    "Không có tên"
                )

                # ==========================================
                # LẤY DỮ LIỆU CỦA CỬA HÀNG ĐÃ CHỌN
                # ==========================================

                store_companies = [
                    company
                    for company in companies
                    if company.store_id == selected_store_id
                ]

                # ==========================================
                # CHỌN THÁNG
                # ==========================================

                print(
                    f"\n--- CÁC THÁNG CỦA "
                    f"{selected_store_name} ---"
                )

                for i, company in enumerate(
                    store_companies,
                    1
                ):
                    print(
                        f"{i}. {company.month}"
                    )

                month_choice = int(
                    input(
                        f"\nChọn tháng "
                        f"(1-{len(store_companies)}): "
                    )
                )

                if (
                    month_choice < 1
                    or month_choice > len(store_companies)
                ):
                    raise ValueError(
                        "Lựa chọn tháng không hợp lệ."
                    )

                company = store_companies[
                    month_choice - 1
                ]

                # ==========================================
                # TÍNH TOÁN HIỆN TẠI
                # ==========================================

                current_profit = calculate_profit(
                    company
                )

                current_cit = calculate_cit(
                    company
                )

                print(
                    "\n--- THÔNG TIN HIỆN TẠI ---"
                )

                print(
                    f"Tên cửa hàng:      "
                    f"{selected_store_name}"
                )

                print(
                    f"Mã cửa hàng:       "
                    f"{company.store_id}"
                )

                print(
                    f"Tháng:             "
                    f"{company.month}"
                )

                print(
                    f"Doanh thu:         "
                    f"{company.revenue:,.0f} VND"
                )

                print(
                    f"Giá vốn hàng bán:  "
                    f"{company.cogs:,.0f} VND"
                )

                print(
                    f"Chi phí vận hành:  "
                    f"{company.operating_cost:,.0f} VND"
                )

                print(
                    f"Lợi nhuận:         "
                    f"{current_profit:,.0f} VND"
                )

                print(
                    f"CIT:               "
                    f"{current_cit:,.0f} VND"
                )

                # ==========================================
                # CHỌN KỊCH BẢN
                # ==========================================

                print(
                    "\n--- CHỌN KỊCH BẢN ---"
                )

                print(
                    "1. Tăng doanh thu"
                )

                print(
                    "2. Giảm chi phí vận hành"
                )

                print(
                    "3. Giảm giá vốn hàng bán"
                )

                scenario_choice = input(
                    "\nChọn kịch bản (1-3): "
                )

                # ==========================================
                # KỊCH BẢN 1
                # ==========================================

                if scenario_choice == "1":

                    percent = float(
                        input(
                            "Nhập % tăng doanh thu "
                            "(ví dụ 10 cho 10%): "
                        )
                    )

                    future = simulate_revenue_increase(
                        company,
                        percent
                    )

                    scenario_name = (
                        f"Doanh thu tăng {percent}%"
                    )

                # ==========================================
                # KỊCH BẢN 2
                # ==========================================

                elif scenario_choice == "2":

                    percent = float(
                        input(
                            "Nhập % giảm chi phí vận hành "
                            "(ví dụ 5 cho 5%): "
                        )
                    )

                    future = simulate_operating_cost_reduction(
                        company,
                        percent
                    )

                    scenario_name = (
                        f"Chi phí vận hành giảm {percent}%"
                    )

                # ==========================================
                # KỊCH BẢN 3
                # ==========================================

                elif scenario_choice == "3":

                    percent = float(
                        input(
                            "Nhập % giảm giá vốn hàng bán "
                            "(ví dụ 5 cho 5%): "
                        )
                    )

                    future = simulate_cogs_reduction(
                        company,
                        percent
                    )

                    scenario_name = (
                        f"Giá vốn hàng bán giảm {percent}%"
                    )

                else:
                    raise ValueError(
                        "Kịch bản không hợp lệ."
                    )

                # ==========================================
                # TÍNH KẾT QUẢ SAU KỊCH BẢN
                # ==========================================

                future_profit = calculate_profit(
                    future
                )

                future_cit = calculate_cit(
                    future
                )

                # ==========================================
                # HIỂN THỊ KẾT QUẢ
                # ==========================================

                print(
                    "\n========== KẾT QUẢ TAXTWIN =========="
                )

                print(
                    f"\nCửa hàng: "
                    f"{selected_store_name}"
                )

                print(
                    f"Mã CH: {company.store_id}"
                )

                print(
                    f"Tháng: {company.month}"
                )

                print(
                    f"Kịch bản: {scenario_name}"
                )

                print(
                    "\n                    HIỆN TẠI          KỊCH BẢN"
                )

                print(
                    f"Doanh thu:          "
                    f"{company.revenue:>15,.0f}   "
                    f"{future.revenue:>15,.0f}"
                )

                print(
                    f"Giá vốn hàng bán:   "
                    f"{company.cogs:>15,.0f}   "
                    f"{future.cogs:>15,.0f}"
                )

                print(
                    f"Chi phí vận hành:   "
                    f"{company.operating_cost:>15,.0f}   "
                    f"{future.operating_cost:>15,.0f}"
                )

                print(
                    f"Lợi nhuận:          "
                    f"{current_profit:>15,.0f}   "
                    f"{future_profit:>15,.0f}"
                )

                print(
                    f"CIT:                "
                    f"{current_cit:>15,.0f}   "
                    f"{future_cit:>15,.0f}"
                )

                # ==========================================
                # THAY ĐỔI
                # ==========================================

                profit_change = (
                    future_profit
                    - current_profit
                )

                cit_change = (
                    future_cit
                    - current_cit
                )

                print("\n--- THAY ĐỔI ---")

                print(
                    f"Lợi nhuận thay đổi: "
                    f"{profit_change:,.0f} VND"
                )

                print(
                    f"CIT thay đổi:       "
                    f"{cit_change:,.0f} VND"
                )

                print(
                    "======================================"
                )

            except Exception as e:
                print(
                    f"\n[Lỗi] Đã xảy ra vấn đề "
                    f"khi chạy Taxtwin: {e}"
                )

            input(
                "\n[Hoàn thành] Nhấn Enter để quay lại menu chính..."
            )
        elif choice == '0':
            print("\nĐã thoát hệ thống. Tạm biệt!")
            sys.exit()

        else:
            print("\nLựa chọn không hợp lệ, vui lòng nhập số từ 0 đến 5.")
            input("\nNhấn Enter để thử lại...")


if __name__ == "__main__":
    main()
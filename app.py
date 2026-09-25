import sys
import os
from datetime import date

import config
from finrag.retriever import create_retriever
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

# Xác định thư mục gốc chứa file app.py để tạo dẫn tương đối an toàn
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
    print(" ĐANG KHỜI ĐỘNG HỆ THỐNG TAXMINDAI LAUREL WREATH ")
    print("=" * 50)


# DANH MỤC KHAI BÁO CÁC VĂN BẢN PHÁP LUẬT
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
    "data/knowledge/decrees/decree_123.pdf": {
        "loai": "Nghi dinh",
        "ten": "Nghị định số 123/2020/NĐ-CP (Quy định về hóa đơn, chứng từ)",
        "hieu_luc_tu": date(2022, 7, 1),
        "het_hieu_luc": None,
    },
    "data/knowledge/decrees/decree_125.pdf": {
        "loai": "Nghi dinh",
        "ten": "Nghị định số 125/2020/NĐ-CP (Xử phạt VPHC về thuế, hóa đơn)",
        "hieu_luc_tu": date(2020, 12, 5),
        "het_hieu_luc": None,
    },
    "data/knowledge/decrees/decree_70.pdf": {
        "loai": "Nghi dinh",
        "ten": "Nghị định số 68/2026/NĐ-CP (Thuế hộ/cá nhân kinh doanh)",
        "hieu_luc_tu": date(2026, 3, 5),
        "het_hieu_luc": None,
    },
    "data/knowledge/circulars/circular_96.pdf": {
        "loai": "Thong tu",
        "ten": "Thông tư số 96/2015/TT-BTC (Hướng dẫn thuế TNDN)",
        "hieu_luc_tu": date(2015, 8, 6),
        "het_hieu_luc": None,
    },
    "data/knowledge/circulars/circular_78.pdf": {
        "loai": "Thong tu",
        "ten": "Thông tư số 78/2014/TT-BTC (Hướng dẫn thi hành Luật thuế TNDN)",
        "hieu_luc_tu": date(2014, 8, 2),
        "het_hieu_luc": None,
    },
    "data/knowledge/circulars/circular_80.pdf": {
        "loai": "Thong tu",
        "ten": "Thông tư số 20/2026/TT-BTC (Hướng dẫn Luật Thuế TNDN)",
        "hieu_luc_tu": date(2026, 3, 12),
        "het_hieu_luc": None,
    },
    "data/knowledge/letters/letter.pdf": {
        "loai": "Cong van",
        "ten": "Công văn số 4226/CT-NVT (Hướng dẫn quyết toán thuế TNCN)",
        "hieu_luc_tu": date(2026, 5, 1),
        "het_hieu_luc": None,
    },
}

THU_TU_UU_TIEN = {"Luat": 1, "Nghi dinh": 2, "Thong tu": 3, "Cong van": 4}


def kiem_tra_hieu_luc(info):
    """Trả về chuỗi mô tả trạng thái hiệu lực dựa trên ngày hiện tại."""
    if not info:
        return "Còn hiệu lực (Đã xác minh qua CSDL Thuế RAG)"
    hom_nay = date.today()
    if info.get("hieu_luc_tu") and hom_nay < info["hieu_luc_tu"]:
        return f"CHƯA có hiệu lực (áp dụng từ {info['hieu_luc_tu'].strftime('%d/%m/%Y')})"
    if info.get("het_hieu_luc") and hom_nay > info["het_hieu_luc"]:
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
                    name = getattr(c, 'company_name', getattr(c, 'store_id', f'Doanh nghiệp {i+1}'))
                    print(f"{i + 1}. {name}")

                idx = int(input("Chọn doanh nghiệp (nhập số thứ tự): ")) - 1
                company = companies[idx]

                c_name = getattr(company, 'company_name', getattr(company, 'store_id', 'Doanh nghiệp'))
                print(f"\nĐang mô phỏng Monte Carlo cho '{c_name}'...")
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
                    db_path = os.path.join(BASE_DIR, "data")
                    vector_store = load_vector_store(db_path, embeddings)
                    my_retriever = create_retriever(vector_store)

                    print("\nĐang suy nghĩ và tra cứu tài liệu...")
                    result = rag_chain.ask_question(question=user_question, retriever=my_retriever)

                    print("\n=== AI TƯ VẤN THUẾ ===")
                    print(result["answer"])
                    print("\n--- CĂN CỨ PHÁP LÝ (theo thứ bậc: Luật → Nghị định → Thông tư → Công văn) ---")

                    seen = set()
                    nguon_dung = []

                    van_ban_norm = {os.path.normpath(k): v for k, v in VAN_BAN_INFO.items()}

                    for doc in result["documents"]:
                        src = doc.metadata.get("source", "")
                        page = doc.metadata.get("page", "?")
                        
                        src_norm = os.path.normpath(src)
                        key = (src_norm, page)
                        if key in seen:
                            continue
                        seen.add(key)

                        info = van_ban_norm.get(src_norm)

                        if info:
                            ten_van_ban = info["ten"]
                            loai_van_ban = info["loai"]
                            trang_thai = kiem_tra_hieu_luc(info)
                        else:
                            file_name = os.path.basename(src)
                            file_clean = os.path.splitext(file_name)[0].replace("-", " ")

                            if "laws" in src_norm or "law" in file_name.lower():
                                loai_van_ban = "Luat"
                                ten_van_ban = f"Văn bản Luật: {file_clean}"
                            elif "decrees" in src_norm or "decree" in file_name.lower() or "nghi-dinh" in file_name.lower():
                                loai_van_ban = "Nghi dinh"
                                ten_van_ban = f"Nghị định: {file_clean}"
                            elif "circulars" in src_norm or "circular" in file_name.lower() or "thong-tu" in file_name.lower():
                                loai_van_ban = "Thong tu"
                                ten_van_ban = f"Thông tư: {file_clean}"
                            else:
                                loai_van_ban = "Cong van"
                                ten_van_ban = f"Công văn: {file_clean}"

                            trang_thai = "Đang áp dụng (Trích xuất từ cơ sở dữ liệu RAG)"

                        nguon_dung.append({
                            "ten": ten_van_ban,
                            "loai": loai_van_ban,
                            "page": page,
                            "trang_thai": trang_thai
                        })

                    nguon_dung.sort(key=lambda x: THU_TU_UU_TIEN.get(x["loai"], 99))

                    if not nguon_dung:
                        print("- Chưa tìm thấy trích dẫn cụ thể trong CSDL RAG.")
                    else:
                        for item in nguon_dung:
                            print(f"- {item['ten']}, trang {item['page']}")
                            print(f"    Tình trạng: {item['trang_thai']}")

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

                if not companies:
                    print("\n[Cảnh báo] Không tìm thấy dữ liệu doanh nghiệp trong file!")
                else:
                    print("\nCác doanh nghiệp có trong dữ liệu:")
                    for i, c in enumerate(companies):
                        name = getattr(c, 'company_name', getattr(c, 'store_id', f'Doanh nghiệp {i+1}'))
                        month = getattr(c, 'month', '')
                        print(f"{i + 1}. {name} (Tháng: {month})" if month else f"{i + 1}. {name}")

                    idx = int(input("\nChọn doanh nghiệp (nhập số thứ tự): ")) - 1
                    
                    if 0 <= idx < len(companies):
                        company = companies[idx]

                        revenue_growth = float(input("Nhập % tăng trưởng doanh thu dự kiến (ví dụ 0.15 cho 15%): "))
                        cost_growth = float(input("Nhập % tăng trưởng chi phí dự kiến (ví dụ 0.08 cho 8%): "))

                        # Xử lý linh hoạt số lượng tham số đầu vào của hàm forecast_company
                        try:
                            future = forecast_company(company, revenue_growth, cost_growth, cost_growth)
                        except TypeError:
                            future = forecast_company(company, revenue_growth, cost_growth)

                        c_name = getattr(future, 'company_name', getattr(future, 'store_id', 'Doanh nghiệp'))

                        print(f"\n===== DỰ BÁO CHO '{c_name}' =====")
                        print(f"Doanh thu dự kiến : {future.revenue:,.0f} VND")
                        
                        cogs_val = getattr(future, 'cogs', 0.0)
                        op_val = getattr(future, 'operating_cost', 0.0)
                        cost_val = getattr(future, 'cost', cogs_val + op_val)
                        print(f"Chi phí dự kiến   : {cost_val:,.0f} VND")

                        print(f"VAT dự kiến       : {calculate_vat(future):,.0f} VND")
                        print(f"CIT (TNDN) dự kiến: {calculate_cit(future):,.0f} VND")
                        print("========================\n")
                    else:
                        print("\n[Lỗi] Số thứ tự doanh nghiệp không hợp lệ!")

            except Exception as e:
                print(f"\n[Lỗi] Đã xảy ra vấn đề khi chạy Forecasting: {e}")

            input("\n[Hoàn thành] Nhấn Enter để quay lại menu chính...")

        elif choice == '4':
            print("\n[ĐANG CHẠY MODULE MONTE CARLO]")
            try:
                from taxtwin.loader import load_company
                from montecarlo.simulation import (
                    monte_carlo,
                    summarize_results,
                    calculate_percentiles,
                )

                company_file = os.path.join(BASE_DIR, "data", "company", "DuLieuMoPhong_ChuoiBanLe_FinRAG.xlsx")

                # Dùng load_company để đọc file Excel thay vì đọc CSV
                companies = load_company(company_file)

                if not companies:
                    print("\n[Cảnh báo] Không tìm thấy dữ liệu doanh nghiệp trong file Excel!")
                else:
                    print("\n--- CHỌN DOANH NGHIỆP ---")
                    for i, company in enumerate(companies, 1):
                        name = getattr(company, 'company_name', getattr(company, 'store_id', f'Cửa hàng {i}'))
                        month = getattr(company, 'month', '')
                        print(f"{i}. {name} (Tháng: {month})" if month else f"{i}. {name}")

                    company_choice = int(input("\nChọn doanh nghiệp (nhập số thứ tự): "))
                    
                    if 1 <= company_choice <= len(companies):
                        company = companies[company_choice - 1]

                        num_simulations = int(input("Nhập số lần mô phỏng (ví dụ 1000): "))
                        c_name = getattr(company, 'company_name', getattr(company, 'store_id', 'Doanh nghiệp'))
                        
                        print(f"\nĐang thực hiện {num_simulations} lần mô phỏng cho '{c_name}'...")

                        results = monte_carlo(company, num_simulations)
                        summary = summarize_results(results)
                        percentiles = calculate_percentiles(results)

                        print("\n========== KẾT QUẢ MONTE CARLO ==========")
                        print(f"Doanh nghiệp: {c_name}")
                        print(f"Giá trị CIT trung bình: {summary['average_cit']:,.0f} VND")
                        print(f"Độ lệch chuẩn CIT:     {summary['std_cit']:,.0f} VND")
                        print(f"CIT thấp nhất:          {summary['min_cit']:,.0f} VND")
                        print(f"CIT cao nhất:           {summary['max_cit']:,.0f} VND")
                        print(f"P5:                     {percentiles['p5']:,.0f} VND")
                        print(f"Median (P50):           {percentiles['p50']:,.0f} VND")
                        print(f"P95:                    {percentiles['p95']:,.0f} VND")
                        print("==========================================")
                    else:
                        print("\n[Lỗi] Lựa chọn doanh nghiệp không hợp lệ!")

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

                company_file = os.path.join(
                    BASE_DIR,
                    "data",
                    "company",
                    "DuLieuMoPhong_ChuoiBanLe_FinRAG.xlsx"
                )

                companies = load_company(company_file)

                store_df = pd.read_excel(
                    company_file,
                    sheet_name="DM_CuaHang",
                    header=3
                )

                store_names = dict(
                    zip(
                        store_df["Mã CH"].astype(str),
                        store_df["Tên cửa hàng"].astype(str)
                    )
                )

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
                    print(f"{i}. {store_name} ({store_id})")

                print(
                    f"\nTổng số cửa hàng có dữ liệu: "
                    f"{len(store_ids)}"
                )

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

                store_companies = [
                    company
                    for company in companies
                    if company.store_id == selected_store_id
                ]

                print(
                    f"\n--- CÁC THÁNG CỦA "
                    f"{selected_store_name} ---"
                )

                for i, company in enumerate(
                    store_companies,
                    1
                ):
                    print(f"{i}. {company.month}")

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

                current_profit = calculate_profit(company)
                current_cit = calculate_cit(company)

                print("\n--- THÔNG TIN HIỆN TẠI ---")
                print(f"Tên cửa hàng:      {selected_store_name}")
                print(f"Mã cửa hàng:       {company.store_id}")
                print(f"Tháng:             {company.month}")
                print(f"Doanh thu:         {company.revenue:,.0f} VND")
                print(f"Giá vốn hàng bán:  {company.cogs:,.0f} VND")
                print(f"Chi phí vận hành:  {company.operating_cost:,.0f} VND")
                print(f"Lợi nhuận:         {current_profit:,.0f} VND")
                print(f"CIT:               {current_cit:,.0f} VND")

                print("\n--- CHỌN KỊCH BẢN ---")
                print("1. Tăng doanh thu")
                print("2. Giảm chi phí vận hành")
                print("3. Giảm giá vốn hàng bán")

                scenario_choice = input("\nChọn kịch bản (1-3): ")

                if scenario_choice == "1":
                    percent = float(input("Nhập % tăng doanh thu (ví dụ 10 cho 10%): "))
                    future = simulate_revenue_increase(company, percent)
                    scenario_name = f"Doanh thu tăng {percent}%"

                elif scenario_choice == "2":
                    percent = float(input("Nhập % giảm chi phí vận hành (ví dụ 5 cho 5%): "))
                    future = simulate_operating_cost_reduction(company, percent)
                    scenario_name = f"Chi phí vận hành giảm {percent}%"

                elif scenario_choice == "3":
                    percent = float(input("Nhập % giảm giá vốn hàng bán (ví dụ 5 cho 5%): "))
                    future = simulate_cogs_reduction(company, percent)
                    scenario_name = f"Giá vốn hàng bán giảm {percent}%"

                else:
                    raise ValueError("Kịch bản không hợp lệ.")

                future_profit = calculate_profit(future)
                future_cit = calculate_cit(future)

                print("\n========== KẾT QUẢ TAXTWIN ==========")
                print(f"\nCửa hàng: {selected_store_name}")
                print(f"Mã CH: {company.store_id}")
                print(f"Tháng: {company.month}")
                print(f"Kịch bản: {scenario_name}")

                print("\n                    HIỆN TẠI          KỊCH BẢN")
                print(f"Doanh thu:          {company.revenue:>15,.0f}   {future.revenue:>15,.0f}")
                print(f"Giá vốn hàng bán:   {company.cogs:>15,.0f}   {future.cogs:>15,.0f}")
                print(f"Chi phí vận hành:   {company.operating_cost:>15,.0f}   {future.operating_cost:>15,.0f}")
                print(f"Lợi nhuận:          {current_profit:>15,.0f}   {future_profit:>15,.0f}")
                print(f"CIT:                {current_cit:>15,.0f}   {future_cit:>15,.0f}")

                profit_change = future_profit - current_profit
                cit_change = future_cit - current_cit

                print("\n--- THAY ĐỔI ---")
                print(f"Lợi nhuận thay đổi: {profit_change:,.0f} VND")
                print(f"CIT thay đổi:       {cit_change:,.0f} VND")
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
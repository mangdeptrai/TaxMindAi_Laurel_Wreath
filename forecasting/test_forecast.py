from taxtwin.loader import load_company

from taxtwin.calculator import calculate_profit
from taxtwin.calculator import calculate_cit

from forecasting.forecast import forecast_company


# ==========================================
# LOAD DATA
# ==========================================

FILE_PATH = r"data/company/DuLieuMoPhong_ChuoiBanLe_FinRAG.xlsx"

companies = load_company(FILE_PATH)

print(f"Đã tải {len(companies)} bản ghi.")


# ==========================================
# CHỌN BẢN GHI ĐỂ DỰ BÁO
# ==========================================

company = companies[0]


# ==========================================
# DỰ BÁO
# ==========================================

future = forecast_company(
    company,
    revenue_growth=0.15,
    cogs_growth=0.08,
    operating_cost_growth=0.05
)


# ==========================================
# KẾT QUẢ
# ==========================================

print("\n===== DỰ BÁO =====")

print("Store:", future.store_id)

print("Month:", future.month)

print(
    "Revenue:",
    f"{future.revenue:,.0f} VNĐ"
)

print(
    "COGS:",
    f"{future.cogs:,.0f} VNĐ"
)

print(
    "Operating Cost:",
    f"{future.operating_cost:,.0f} VNĐ"
)

profit = calculate_profit(future)

cit = calculate_cit(future)

print(
    "Profit:",
    f"{profit:,.0f} VNĐ"
)

print(
    "CIT:",
    f"{cit:,.0f} VNĐ"
)
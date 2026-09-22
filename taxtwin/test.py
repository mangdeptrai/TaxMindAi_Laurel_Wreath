from taxtwin.loader import load_company

from taxtwin.calculator import (
    calculate_profit,
    calculate_cit,
    simulate_revenue_increase,
    simulate_operating_cost_reduction,
    simulate_cogs_reduction
)


# ==========================================
# ĐƯỜNG DẪN DỮ LIỆU
# ==========================================

FILE_PATH = r"data/company/DuLieuMoPhong_ChuoiBanLe_FinRAG.xlsx"


# ==========================================
# LOAD DATA
# ==========================================

companies = load_company(FILE_PATH)

print(f"Đã tải {len(companies)} bản ghi.")


# ==========================================
# KIỂM TRA TOÀN BỘ DỮ LIỆU
# ==========================================

mismatch_count = 0

for company in companies:

    calculated_profit = calculate_profit(company)

    if abs(
        calculated_profit - company.profit_before_tax
    ) > 1:

        mismatch_count += 1


print(
    f"Số bản ghi không khớp lợi nhuận: "
    f"{mismatch_count}"
)


# ==========================================
# LẤY BẢN GHI ĐẦU TIÊN
# ==========================================

company = companies[0]


print("\n--- BẢN GHI ĐẦU TIÊN ---")

print(company)


# ==========================================
# TÍNH TOÁN CƠ BẢN
# ==========================================

profit = calculate_profit(company)

cit = calculate_cit(company)


print("\n--- KẾT QUẢ TÍNH THUẾ ---")

print(f"Mã cửa hàng: {company.store_id}")

print(f"Tháng: {company.month}")

print(
    f"Doanh thu: "
    f"{company.revenue:,.0f} VNĐ"
)

print(
    f"Lợi nhuận: "
    f"{profit:,.0f} VNĐ"
)

print(
    f"CIT: "
    f"{cit:,.0f} VNĐ"
)


# ==========================================
# TEST SCENARIO
# ==========================================

print("\n==========================================")
print("             TEST SCENARIO")
print("==========================================")


# ------------------------------------------
# 1. DOANH THU TĂNG 10%
# ------------------------------------------

revenue_scenario = simulate_revenue_increase(
    company,
    10
)

revenue_profit = calculate_profit(
    revenue_scenario
)

revenue_cit = calculate_cit(
    revenue_scenario
)


print("\n[1] Doanh thu tăng 10%")

print(
    f"Doanh thu mới: "
    f"{revenue_scenario.revenue:,.0f} VNĐ"
)

print(
    f"Lợi nhuận mới: "
    f"{revenue_profit:,.0f} VNĐ"
)

print(
    f"CIT mới: "
    f"{revenue_cit:,.0f} VNĐ"
)


# ------------------------------------------
# 2. CHI PHÍ VẬN HÀNH GIẢM 5%
# ------------------------------------------

cost_scenario = simulate_operating_cost_reduction(
    company,
    5
)

cost_profit = calculate_profit(
    cost_scenario
)

cost_cit = calculate_cit(
    cost_scenario
)


print("\n[2] Chi phí vận hành giảm 5%")

print(
    f"Chi phí vận hành mới: "
    f"{cost_scenario.operating_cost:,.0f} VNĐ"
)

print(
    f"Lợi nhuận mới: "
    f"{cost_profit:,.0f} VNĐ"
)

print(
    f"CIT mới: "
    f"{cost_cit:,.0f} VNĐ"
)


# ------------------------------------------
# 3. GIÁ VỐN HÀNG BÁN GIẢM 5%
# ------------------------------------------

cogs_scenario = simulate_cogs_reduction(
    company,
    5
)

cogs_profit = calculate_profit(
    cogs_scenario
)

cogs_cit = calculate_cit(
    cogs_scenario
)


print("\n[3] Giá vốn hàng bán giảm 5%")

print(
    f"Giá vốn mới: "
    f"{cogs_scenario.cogs:,.0f} VNĐ"
)

print(
    f"Lợi nhuận mới: "
    f"{cogs_profit:,.0f} VNĐ"
)

print(
    f"CIT mới: "
    f"{cogs_cit:,.0f} VNĐ"
)
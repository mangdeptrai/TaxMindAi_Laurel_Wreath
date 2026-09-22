import pandas as pd

from taxtwin.models import Company


def load_company(file_path):
    df = pd.read_excel(
        file_path,
        sheet_name="DuLieuDoanhNghiepGiaLap",
        header=3
    )

    companies = []

    for _, row in df.iterrows():
        company = Company(
            store_id=str(row["Mã CH"]),
            month=str(row["Tháng"]),
            revenue=float(row["Doanh thu (VNĐ)"]),
            cogs=float(row["Giá vốn hàng bán (VNĐ)"]),
            operating_cost=float(row["Chi phí vận hành (VNĐ)"]),
            profit_before_tax=float(
                row["Lợi nhuận trước thuế (VNĐ)"]
            ),
            orders=int(row["Số đơn hàng"]),
            customers=int(row["Số lượt khách"]),
            conversion_rate=float(
                row["Tỷ lệ chuyển đổi (%)"]
            ),
            ending_inventory=int(
                row["Hàng tồn cuối kỳ (SP)"]
            )
        )

        companies.append(company)

    return companies
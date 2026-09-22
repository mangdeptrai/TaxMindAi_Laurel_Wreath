from copy import deepcopy

from taxtwin.models import Company


def forecast_company(
    company: Company,
    revenue_growth: float,
    cogs_growth: float,
    operating_cost_growth: float
):
    """
    Dự báo tình hình tài chính của cửa hàng.

    revenue_growth:
        Tỷ lệ tăng trưởng doanh thu.
        Ví dụ 0.15 = tăng 15%.

    cogs_growth:
        Tỷ lệ tăng trưởng giá vốn.
        Ví dụ 0.08 = tăng 8%.

    operating_cost_growth:
        Tỷ lệ tăng trưởng chi phí vận hành.
        Ví dụ 0.05 = tăng 5%.
    """

    forecast = deepcopy(company)

    forecast.revenue *= (1 + revenue_growth)

    forecast.cogs *= (1 + cogs_growth)

    forecast.operating_cost *= (
        1 + operating_cost_growth
    )

    return forecast
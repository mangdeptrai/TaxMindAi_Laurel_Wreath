from copy import copy
from taxtwin.models import Company


def simulate_revenue_increase(company: Company, percent: float):
    """
    Mô phỏng doanh thu tăng theo phần trăm.
    Ví dụ: percent = 10 -> doanh thu tăng 10%.
    """

    new_company = copy(company)
    new_company.revenue = company.revenue * (1 + percent / 100)

    return new_company


def simulate_operating_cost_reduction(
    company: Company,
    percent: float
):
    """
    Mô phỏng chi phí vận hành giảm theo phần trăm.
    Ví dụ: percent = 5 -> chi phí vận hành giảm 5%.
    """

    new_company = copy(company)
    new_company.operating_cost = (
        company.operating_cost * (1 - percent / 100)
    )

    return new_company


def simulate_cogs_reduction(
    company: Company,
    percent: float
):
    """
    Mô phỏng giá vốn hàng bán giảm theo phần trăm.
    Ví dụ: percent = 5 -> COGS giảm 5%.
    """

    new_company = copy(company)
    new_company.cogs = (
        company.cogs * (1 - percent / 100)
    )

    return new_company


def simulate_forecast(
    company: Company,
    revenue_growth: float,
    cogs_growth: float,
    operating_cost_growth: float
):
    """
    Mô phỏng dự báo doanh thu, giá vốn và chi phí vận hành.
    """

    new_company = copy(company)

    new_company.revenue = (
        company.revenue * (1 + revenue_growth)
    )

    new_company.cogs = (
        company.cogs * (1 + cogs_growth)
    )

    new_company.operating_cost = (
        company.operating_cost * (1 + operating_cost_growth)
    )

    return new_company
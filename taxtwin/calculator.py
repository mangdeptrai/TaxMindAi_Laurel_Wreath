from copy import copy

from taxtwin.models import Company


def calculate_profit(company: Company):
    return (
        company.revenue
        - company.cogs
        - company.operating_cost
    )


def calculate_cit(company: Company, tax_rate=0.20):
    profit = calculate_profit(company)

    if profit <= 0:
        return 0

    return profit * tax_rate


# ==========================================
# SCENARIO SIMULATION
# ==========================================

def simulate_revenue_increase(company: Company, percent: float):
    """
    Mô phỏng doanh thu tăng theo phần trăm.
    """
    new_company = copy(company)

    new_company.revenue = (
        company.revenue * (1 + percent / 100)
    )

    return new_company


def simulate_operating_cost_reduction(
    company: Company,
    percent: float
):
    """
    Mô phỏng chi phí vận hành giảm theo phần trăm.
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
    """
    new_company = copy(company)

    new_company.cogs = (
        company.cogs * (1 - percent / 100)
    )

    return new_company
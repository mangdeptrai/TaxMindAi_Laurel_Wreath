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


def calculate_vat(company: Company, vat_rate=0.10):
    """
    Tính thuế VAT phải nộp (VAT đầu ra - VAT đầu vào).
    """
    if hasattr(company, "vat_output") and hasattr(company, "vat_input"):
        vat = company.vat_output - company.vat_input
    else:
        vat = (company.revenue - company.cogs) * vat_rate

    return max(0, vat)


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
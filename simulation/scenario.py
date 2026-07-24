from copy import copy
from taxtwin.models import Company

def simulate_revenue_increase(company: Company, percent: float):
    new_company = copy(company)
    new_company.revenue = company.revenue * (1 + percent / 100)
    return new_company
def simulate_cost_increase(company: Company, percent: float):
    new_company = copy(company)
    new_company.cost = company.cost * (1 + percent / 100)
    return new_company
def simulate_forecast(
    company: Company,
    revenue_percent: float,
    cost_percent: float
):
    new_company = simulate_revenue_increase(
        company,
        revenue_percent
    )

    new_company = simulate_cost_increase(
        new_company,
        cost_percent
    )

    return new_company
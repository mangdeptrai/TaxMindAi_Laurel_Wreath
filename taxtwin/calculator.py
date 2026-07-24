from taxtwin.models import Company


def calculate_vat(company: Company):
    return company.vat_output - company.vat_input
def calculate_profit(company: Company):
    return company.revenue - company.cost
def calculate_cit(company: Company):#cit = corporate income tax
    profit = calculate_profit(company)
    return profit * 0.2
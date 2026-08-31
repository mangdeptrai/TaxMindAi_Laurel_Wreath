from taxtwin.loader import load_company
from taxtwin.calculator import calculate_vat
from taxtwin.calculator import calculate_cit

from forecasting.forecast import forecast_company

companies = load_company("data/company/company.csv")

company = companies[0]

future = forecast_company(
    company,
    revenue_growth=0.15,
    cost_growth=0.08
)

print("===== DỰ BÁO =====")
print("Revenue:", future.revenue)
print("Cost:", future.cost)

print("VAT:", calculate_vat(future))
print("CIT:", calculate_cit(future))
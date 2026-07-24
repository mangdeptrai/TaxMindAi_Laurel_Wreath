from taxtwin.loader import load_company

from simulation.scenario import simulate_forecast

companies = load_company("data/company/company.csv")

company = companies[0]

future = simulate_forecast(
    company,
    revenue_percent=15,
    cost_percent=8
)

print("===== COMPANY GỐC =====")
print(f"Revenue: {company.revenue:,.0f}")
print(f"Cost: {company.cost:,.0f}")

print()

print("===== COMPANY DỰ BÁO =====")
print(f"Revenue: {future.revenue:,.0f}")
print(f"Cost: {future.cost:,.0f}")
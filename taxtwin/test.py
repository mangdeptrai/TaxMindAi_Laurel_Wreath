"""
File: test.py

Mô tả
------
Kiểm tra các chức năng của TaxTwin.

Module này kiểm tra xem toàn bộ module có hoạt động đúng hay không..
"""

from taxtwin.loader import load_company
from taxtwin.calculator import calculate_cit, calculate_vat
from simulation.scenario import simulate_revenue_increase

companies = load_company("data/company/company.csv")

for company in companies:
    vat = calculate_vat(company)
    print(company.company_name)
    print(f"VAT phai nop: {vat:,.0f}")
    print(f"CIT phai nop: {calculate_cit(company):,.0f}")
    
for company in companies:
    print(f"\n")
    print(company.company_name)
    print(f"Doanh thu ban dau: {company.revenue:,.0f}")
    new_company = simulate_revenue_increase(company, 10)
    print(f"Doanh thu sau khi tăng 10%: {new_company.revenue:,.0f}")
    print(f"Doanh thu gốc: {company.revenue:,.0f}")

    old_vat = calculate_vat(company)
    new_vat = calculate_vat(new_company)
    
    old_cit = calculate_cit(company)
    new_cit = calculate_cit(new_company)

    print("\n====so sanh VAT va CIT sau khi tang doanh thu 10%====")
    print(f"revenue: {company.revenue:,.0f} -> {new_company.revenue:,.0f}")
    print(f"VAT: {old_vat:,.0f} -> {new_vat:,.0f}")
    print(f"CIT: {old_cit:,.0f} -> {new_cit:,.0f}")
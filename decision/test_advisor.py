from taxtwin.loader import load_company

from montecarlo.simulation import (
    monte_carlo,
    summarize_results,
    probability_over,
    calculate_percentiles,
)

from decision.advisor import generate_report

companies = load_company("data/company/company.csv")
company = companies[0]

results = monte_carlo(company, 1000)

summary = summarize_results(results)

probability = probability_over(
    results,
    900_000_000
)

percentiles = calculate_percentiles(results)

report = generate_report(
    summary,
    probability,
    percentiles
)

print(report)
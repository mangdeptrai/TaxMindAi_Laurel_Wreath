from taxtwin.loader import load_company

from montecarlo.simulation import monte_carlo
from montecarlo.simulation import summarize_results
from montecarlo.simulation import probability_over
from montecarlo.simulation import calculate_percentiles

companies = load_company("data/company/company.csv")
company = companies[0]
#chay mo phong 1000 lan 
results = monte_carlo(company, 1000)
#thong ke ket qua mo phong
summary = summarize_results(results)

print(summary)
#xac suat CIT > 900 trieu
prob = probability_over(
    results,
    900_000_000
)

print(f"Probability CIT > 900 triệu: {prob:.2%}")

# Percentiles
percentiles = calculate_percentiles(results)

print(percentiles)
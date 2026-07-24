from taxtwin.loader import load_company
from finrag.llm import ask_llm
from montecarlo.simulation import (
    monte_carlo,
    summarize_results,
    probability_over,
    calculate_percentiles,
)

from decision.prompt_builder import build_prompt

companies = load_company("data/company/company.csv")

company = companies[0]

results = monte_carlo(company, 1000)

summary = summarize_results(results)

probability = probability_over(
    results,
    900_000_000
)

percentiles = calculate_percentiles(results)

prompt = build_prompt(
    summary,
    probability,
    percentiles
)

answer = ask_llm(prompt)

print(answer)

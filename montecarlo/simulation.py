import numpy as np
from copy import copy
from taxtwin.calculator import calculate_cit


def simulate_forecast(company, revenue_growth, cogs_growth, operating_cost_growth=None):
    """
    Tạo một đối tượng Company mới với các tỷ lệ tăng trưởng giả định.
    """
    new_company = copy(company)
    new_company.revenue = company.revenue * (1 + revenue_growth)
    
    if operating_cost_growth is not None:
        new_company.cogs = company.cogs * (1 + cogs_growth)
        new_company.operating_cost = company.operating_cost * (1 + operating_cost_growth)
    else:
        new_company.cogs = company.cogs * (1 + cogs_growth)
        new_company.operating_cost = company.operating_cost * (1 + cogs_growth)
        
    return new_company


def monte_carlo(company, num_simulations=1000):
    """
    Chạy mô phỏng Monte Carlo cho thuế CIT của doanh nghiệp/cửa hàng.
    """
    results = []
    
    revenue_growths = np.random.normal(0.10, 0.05, num_simulations)
    cost_growths = np.random.normal(0.05, 0.03, num_simulations)

    for i in range(num_simulations):
        rev_g = revenue_growths[i]
        cost_g = cost_growths[i]
        
        try:
            simulated_company = simulate_forecast(company, rev_g, cost_g, cost_g)
        except TypeError:
            simulated_company = simulate_forecast(company, rev_g, cost_g)
            
        cit = calculate_cit(simulated_company)
        results.append(cit)

    return results


def summarize_results(results):
    """
    Tính các chỉ số thống kê cơ bản từ kết quả mô phỏng.
    """
    results_arr = np.array(results)
    return {
        "average_cit": float(np.mean(results_arr)),
        "std_cit": float(np.std(results_arr)),
        "min_cit": float(np.min(results_arr)),
        "max_cit": float(np.max(results_arr)),
    }


def calculate_percentiles(results):
    """
    Tính các mốc phân vị P5, P50 (Median), P95.
    """
    results_arr = np.array(results)
    return {
        "p5": float(np.percentile(results_arr, 5)),
        "p50": float(np.percentile(results_arr, 50)),
        "p95": float(np.percentile(results_arr, 95)),
    }


def probability_over(results, threshold):
    """
    Tính xác suất (tỷ lệ %) kết quả thuế CIT vượt quá một ngưỡng (threshold) nhất định.
    """
    results_arr = np.array(results)
    if len(results_arr) == 0:
        return 0.0
    count_over = np.sum(results_arr > threshold)
    return float(count_over / len(results_arr))
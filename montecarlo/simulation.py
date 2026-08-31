"""
Module Monte Carlo Simulation.

Module này thực hiện mô phỏng Monte Carlo để dự báo
thuế Thu nhập doanh nghiệp (CIT) trong nhiều kịch bản
tăng trưởng doanh thu và chi phí.

Bao gồm các chức năng:
- Sinh tỷ lệ tăng trưởng ngẫu nhiên.
- Thực hiện một lần mô phỏng.
- Thực hiện nhiều lần mô phỏng Monte Carlo.
- Thống kê kết quả mô phỏng.
- Tính xác suất vượt ngưỡng.
- Tính các phân vị (Percentiles).
"""

import random
import statistics

def random_growth(
    minimum: float,
    maximum: float
):
    """
    Sinh ngẫu nhiên một tỷ lệ tăng trưởng.

    Args:
        minimum: Giá trị nhỏ nhất của tỷ lệ tăng trưởng.
        maximum: Giá trị lớn nhất của tỷ lệ tăng trưởng.

    Returns:
        Một giá trị ngẫu nhiên trong khoảng [minimum, maximum].
    """

    return random.uniform(
        minimum,
        maximum
    )
from simulation.scenario import simulate_forecast
from taxtwin.calculator import calculate_cit


def one_simulation(company):
    """
    Thực hiện một lần mô phỏng doanh nghiệp.

    Doanh thu và chi phí sẽ được tăng theo
    các tỷ lệ ngẫu nhiên, sau đó tính thuế
    Thu nhập doanh nghiệp (CIT).

    Args:
        company: Doanh nghiệp gốc.

    Returns:
        Dictionary chứa:
            - revenue_growth
            - cost_growth
            - cit
    """
    revenue_growth = random_growth(10, 20)

    cost_growth = random_growth(5, 10)

    future = simulate_forecast(
        company,
        revenue_growth,
        cost_growth
    )

    cit = calculate_cit(future)

    return {
        "revenue_growth": revenue_growth,
        "cost_growth": cost_growth,
        "cit": cit
    }

def monte_carlo(
    company,
    num_simulations: int
):
    """
    Thực hiện nhiều lần mô phỏng Monte Carlo.

    Args:
        company: Doanh nghiệp cần mô phỏng.
        num_simulations: Số lần mô phỏng.

    Returns:
        Danh sách kết quả của từng lần mô phỏng.
    """
    results = []

    for i in range(num_simulations):

        result = one_simulation(company)

        results.append(result)

    return results

def summarize_results(results):
    """
    Tính các thống kê mô tả của kết quả mô phỏng.

    Bao gồm:

    - Giá trị trung bình.
    - Độ lệch chuẩn.
    - Giá trị nhỏ nhất.
    - Giá trị lớn nhất.

    Args:
        results: Danh sách kết quả mô phỏng.

    Returns:
        Dictionary chứa các thống kê của CIT.
    """
    cit_values = []

    for result in results:
        cit_values.append(result["cit"])

    return {
    "average_cit": sum(cit_values) / len(cit_values),
    "std_cit": statistics.stdev(cit_values),
    "min_cit": min(cit_values),
    "max_cit": max(cit_values)
}
def calculate_std(results):
    """
    Tính độ lệch chuẩn của CIT.

    Args:
        results: Danh sách kết quả mô phỏng.

    Returns:
        Độ lệch chuẩn của CIT.
    """
    cit_values = []

    for result in results:
        cit_values.append(result["cit"])

    return statistics.stdev(cit_values)
def probability_over(
    results,
    threshold: float
):
    """
    Tính xác suất CIT vượt quá một ngưỡng.

    Args:
        results: Danh sách kết quả mô phỏng.
        threshold: Ngưỡng CIT cần kiểm tra.

    Returns:
        Xác suất (0 đến 1) mà CIT lớn hơn threshold.
    """
    count = 0

    for result in results:

        if result["cit"] > threshold:
            count += 1

    return count / len(results)
def calculate_percentiles(results):
    """
    Tính các phân vị của CIT.

    Bao gồm:

    - P5
    - P50 (Median)
    - P95

    Args:
        results: Danh sách kết quả mô phỏng.

    Returns:
        Dictionary chứa các phân vị của CIT.
    """
    cit_values = sorted(
        result["cit"] for result in results
    )

    n = len(cit_values)

    return {
        "p5": cit_values[int(0.05 * n)],
        "p50": cit_values[int(0.50 * n)],
        "p95": cit_values[int(0.95 * n)]
    }
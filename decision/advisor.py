"""
Module tạo báo cáo và khuyến nghị thuế.

Module này chuyển đổi kết quả thống kê từ Monte Carlo
thành báo cáo dễ hiểu cho người dùng.
"""

def generate_report(summary, probability, percentiles):
    """
    Tạo báo cáo tổng hợp từ kết quả Monte Carlo.

    Args:
        summary: Thống kê mô phỏng.
        probability: Xác suất vượt ngưỡng.
        percentiles: Các phân vị.

    Returns:
        Chuỗi báo cáo.
    """
    risk = evaluate_risk(probability)
    recommendation = generate_recommendation(risk)
    report = f"""
=== TaxMind AI Report ===

Average CIT: {summary["average_cit"]:,.0f} VND

Standard Deviation: {summary["std_cit"]:,.0f} VND

Risk Level: {risk}

Probability CIT > 900 triệu:
{probability:.2%}

P5 : {percentiles["p5"]:,.0f}

P50: {percentiles["p50"]:,.0f}

P95: {percentiles["p95"]:,.0f}

Recommendation:
{recommendation}
"""

    return report

def evaluate_risk(probability):
    """
    Đánh giá mức độ rủi ro thuế.

    Args:
        probability: Xác suất CIT vượt ngưỡng.

    Returns:
        Mức độ rủi ro.
    """
    if probability < 0.20:
        return "Low"

    elif probability < 0.50:
        return "Medium"

    else:
        return "High"

def generate_recommendation(risk):
    """
    Tạo khuyến nghị dựa trên mức độ rủi ro thuế.

    Args:
        risk: Mức độ rủi ro (Low, Medium hoặc High).

    Returns:
        Chuỗi khuyến nghị phù hợp.
    """
    if risk == "Low":
        return (
            "Rủi ro thuế ở mức thấp. Doanh nghiệp có thể duy trì "
            "chiến lược kinh doanh hiện tại và tiếp tục theo dõi "
            "nghĩa vụ thuế định kỳ."
        )

    elif risk == "Medium":
        return (
            "Rủi ro thuế ở mức trung bình. Doanh nghiệp nên xem xét lại "
            "kế hoạch tài chính và chuẩn bị cho khả năng tăng thuế."
        )

    else:
        return (
            "Rủi ro thuế ở mức cao. Doanh nghiệp nên xem xét lại "
            "chiến lược thuế và tư vấn với chuyên gia thuế trước "
            "khi đưa ra các quyết định tài chính quan trọng."
        )   
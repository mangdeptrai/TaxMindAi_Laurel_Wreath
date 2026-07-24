def build_prompt(summary, probability, percentiles):

    prompt = f"""
Bạn là một chuyên gia tư vấn thuế doanh nghiệp tại Việt Nam.

Chỉ sử dụng các thông tin được cung cấp dưới đây.

KHÔNG được:
- Tự bịa thêm luật thuế.
- Tự viện dẫn điều luật, nghị định hoặc thông tư.
- Tự đưa ra mức xử phạt.
- Tự suy diễn những thông tin không có trong dữ liệu.

Dữ liệu mô phỏng Monte Carlo:

Thuế TNDN trung bình:
{summary["average_cit"]:,.0f} VND

Độ lệch chuẩn:
{summary["std_cit"]:,.0f} VND

Xác suất thuế vượt 900 triệu đồng:
{probability:.2%}

Các phân vị:

P5 = {percentiles["p5"]:,.0f} VND

P50 = {percentiles["p50"]:,.0f} VND

P95 = {percentiles["p95"]:,.0f} VND

Hãy viết một báo cáo bằng TIẾNG VIỆT.

Báo cáo gồm các phần:

1. Đánh giá rủi ro
- Đánh giá mức độ rủi ro dựa trên xác suất và các chỉ số thống kê.

2. Giải thích
- Giải thích ý nghĩa của các chỉ số.
- Không được thêm thông tin ngoài dữ liệu.

3. Khuyến nghị
- Đưa ra khuyến nghị ngắn gọn cho doanh nghiệp dựa trên kết quả mô phỏng.

Yêu cầu:
- Văn phong chuyên nghiệp.
- Dễ hiểu.
- Khoảng 200–300 từ.
- Không sử dụng Markdown.
"""

    return prompt
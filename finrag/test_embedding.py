from finrag.embedding import create_embedding


text = """
Thuế giá trị gia tăng áp dụng cho hàng hóa.
"""

vector = create_embedding(text)

print(type(vector))
print(len(vector))

print(vector[:10])
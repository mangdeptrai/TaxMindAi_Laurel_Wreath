from langchain_ollama import ChatOllama

def get_llm():
    return ChatOllama(
        model="qwen2.5:7b",
        temperature=0.0  # Bắt buộc đặt = 0.0 để loại bỏ hoàn toàn tính sáng tạo/bịa đặt
    )
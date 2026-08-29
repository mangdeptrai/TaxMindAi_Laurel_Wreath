from langchain_core.prompts import ChatPromptTemplate

from finrag.llm import get_llm


PROMPT = ChatPromptTemplate.from_template("""
Bạn là chuyên gia tư vấn thuế Việt Nam.

Nhiệm vụ của bạn là trả lời câu hỏi dựa trên các tài liệu pháp luật
được cung cấp trong CONTEXT.

QUY TẮC:
1. Chỉ sử dụng thông tin có trong CONTEXT.
2. Không tự suy đoán hoặc bịa thêm quy định pháp luật.
3. Nếu CONTEXT có thông tin liên quan một phần đến câu hỏi,
   hãy trả lời phần có căn cứ và nói rõ phần thông tin còn thiếu.
4. Nếu CONTEXT hoàn toàn không có thông tin liên quan,
   trả lời:
   "Tôi không tìm thấy thông tin phù hợp trong tài liệu."
5. Khi có thể, hãy nêu rõ Điều/Khoản được đề cập trong CONTEXT.
6. Trả lời bằng tiếng Việt, rõ ràng và dễ hiểu.

========================

CONTEXT:

{context}

========================

QUESTION:

{question}

========================

ANSWER:
""")


def ask_question(question, retriever):

    docs = retriever.invoke(question)

    if not docs:
        return {
            "answer": "Tôi không tìm thấy thông tin phù hợp trong tài liệu.",
            "documents": []
        }

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    llm = get_llm()

    prompt = PROMPT.format(
        context=context,
        question=question
    )

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "documents": docs
    }
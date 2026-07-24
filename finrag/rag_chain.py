from langchain_core.prompts import ChatPromptTemplate

from finrag.llm import get_llm


PROMPT = ChatPromptTemplate.from_template("""
Bạn là chuyên gia tư vấn thuế Việt Nam.

Chỉ được trả lời dựa trên CONTEXT.

Nếu CONTEXT không có thông tin thì trả lời:

"Tôi không tìm thấy thông tin trong tài liệu."

========================

CONTEXT:

{context}

========================

QUESTION:

{question}
""")


def ask_question(question, retriever):

    docs = retriever.invoke(question)

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
import fitz  # PyMuPDF
from langchain_core.documents import Document

def ocr_pdf(pdf_path):
    """Đọc trực tiếp nội dung văn bản từ file PDF bằng PyMuPDF"""
    docs = []
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        if text.strip():
            docs.append(Document(
                page_content=text,
                metadata={"source": pdf_path, "page": page_num + 1}
            ))
            
    doc.close()
    return docs
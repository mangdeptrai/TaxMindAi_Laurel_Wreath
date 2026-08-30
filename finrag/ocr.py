import fitz  # PyMuPDF
from PIL import Image
import easyocr
from langchain_core.documents import Document
import numpy as np

ocr_engine = easyocr.Reader(['vi'], gpu=False)


def ocr_pdf(pdf_path: str):
    """OCR mot file PDF scan va tra ve list Document."""

    pdf = fitz.open(pdf_path)
    documents = []

    for page_num in range(len(pdf)):
        page = pdf.load_page(page_num)
        pix = page.get_pixmap(dpi=150)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples).convert("L")
        img_array = np.array(img)

        result = ocr_engine.readtext(img_array, detail=0, paragraph=True, canvas_size=1280)
        text = "\n".join(result)

        documents.append(
            Document(
                page_content=text,
                metadata={"page": page_num + 1, "source": pdf_path},
            )
        )

    pdf.close()
    return documents)

    return documents

import fitz  # PyMuPDF
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
from langchain_core.documents import Document
import numpy as np

ocr_engine = RapidOCR()


def ocr_pdf(pdf_path: str):
    """OCR một file PDF scan và trả về list Document."""

    pdf = fitz.open(pdf_path)
    documents = []

    for page_num in range(len(pdf)):
        page = pdf.load_page(page_num)

        # Render PDF thành ảnh
        pix = page.get_pixmap(dpi=300)

        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        # ÉP KIỂU ẢNH SANG NUMPY ARRAY TRƯỚC KHI OCR
        img_array = np.array(img)

        # OCR
        result, _ = ocr_engine(img_array)

        text = ""

        if result:
            text = "\n".join([line[1] for line in result])

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "page": page_num + 1,
                    "source": pdf_path,
                },
            )
        )

    pdf.close()

    return documents
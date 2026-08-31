from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

from finrag.ocr import ocr_pdf


def load_documents(folder_path: str):
    """
    Đọc tất cả các tài liệu PDF trong cơ sở tri thức (Knowledge Base).

    - PDF có text -> PyPDFLoader
    - PDF scan -> OCR

    Tham số:
        folder_path (str): Đường dẫn đến thư mục chứa cơ sở tri thức.

    Giá trị trả về:
        list: Danh sách các đối tượng Document của LangChain.
    """

    documents = []

    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    pdf_files = sorted(folder.rglob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return []

    print(f"Found {len(pdf_files)} PDF files.")

    for pdf_file in pdf_files:

        print(f"\nLoading {pdf_file.name}...")

        # -----------------------------
        # Đọc PDF bằng PyPDFLoader
        # -----------------------------
        loader = PyPDFLoader(str(pdf_file))
        docs = loader.load()

        # -----------------------------
        # Kiểm tra PDF có text không
        # -----------------------------
        has_text = any(doc.page_content.strip() for doc in docs)

        if has_text:
            print("   ✓ Text PDF")

        else:
            print("   ✓ Scanned PDF -> OCR")

            docs = ocr_pdf(str(pdf_file))

        # -----------------------------
        # Bổ sung metadata
        # -----------------------------
        for doc in docs:
            doc.metadata["category"] = pdf_file.parent.name
            doc.metadata["filename"] = pdf_file.name
            doc.metadata["filepath"] = str(pdf_file)

        documents.extend(docs)

    print(f"\nLoaded {len(documents)} pages.")

    return documents
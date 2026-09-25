from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader

from finrag.ocr import ocr_pdf


def load_documents(folder_path: str):
    """
    Đọc tất cả các tài liệu (PDF, DOCX) trong cơ sở tri thức (Knowledge Base).

    - PDF có text -> PyPDFLoader
    - PDF scan -> OCR
    - Word (.docx) -> Docx2txtLoader

    Tham số:
        folder_path (str): Đường dẫn đến thư mục chứa cơ sở tri thức.

    Giá trị trả về:
        list: Danh sách các đối tượng Document của LangChain.
    """

    documents = []

    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    # Lấy danh sách file PDF và DOCX (bỏ qua file tạm của Word bắt đầu bằng ~$)
    files = sorted([
        f for f in folder.rglob("*")
        if f.suffix.lower() in [".pdf", ".docx"] and not f.name.startswith("~$")
    ])

    if not files:
        print("No supported files (PDF/DOCX) found.")
        return []

    print(f"Found {len(files)} files (PDF/DOCX).")

    for file_path in files:

        print(f"\nLoading {file_path.name}...")

        docs = []

        # -----------------------------
        # Xử lý file PDF
        # -----------------------------
        if file_path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(file_path))
            docs = loader.load()

            # Kiểm tra PDF có text không
            has_text = any(doc.page_content.strip() for doc in docs)

            if has_text:
                print("   ✓ Text PDF")
            else:
                print("   ✓ Scanned PDF -> OCR")
                docs = ocr_pdf(str(file_path))

        # -----------------------------
        # Xử lý file DOCX (Word)
        # -----------------------------
        elif file_path.suffix.lower() == ".docx":
            print("   ✓ Word Document (.docx)")
            loader = Docx2txtLoader(str(file_path))
            docs = loader.load()

        # -----------------------------
        # Bổ sung metadata
        # -----------------------------
        for doc in docs:
            doc.metadata["category"] = file_path.parent.name
            doc.metadata["filename"] = file_path.name
            doc.metadata["filepath"] = str(file_path)

        documents.extend(docs)

    print(f"\nLoaded {len(documents)} pages/documents.")

    return documents
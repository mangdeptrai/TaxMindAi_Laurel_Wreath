from finrag.ocr import ocr_pdf

docs = ocr_pdf("data/knowledge/laws/law_vat.pdf")

print(f"Tổng số trang: {len(docs)}")

print("-" * 50)

print(docs[0].page_content[:1000])
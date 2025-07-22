import fitz  # PyMuPDF
import json

def process_pdf(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    title = extract_title(doc)

    headings = []
    for page_number in range(doc.page_count):
        page = doc.load_page(page_number)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    size = span["size"]
                    if is_heading(text):
                        level = classify_heading(size)
                        headings.append({
                            "level": level,
                            "text": text,
                            "page": page_number + 1
                        })

    output = {
        "title": title,
        "outline": headings
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

def extract_title(doc):
    page = doc.load_page(0)
    blocks = page.get_text("dict")["blocks"]
    candidate = ""
    max_size = 0
    for block in blocks:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if span["size"] > max_size:
                    candidate = span["text"].strip()
                    max_size = span["size"]
    return candidate

def is_heading(text):
    return len(text) > 2 and text[0].isupper()

def classify_heading(size):
    if size >= 20:
        return "H1"
    elif size >= 15:
        return "H2"
    else:
        return "H3"

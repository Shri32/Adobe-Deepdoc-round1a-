import fitz  # PyMuPDF
import os
import json

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []
    title = doc.metadata.get("title") or os.path.basename(pdf_path)

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b['type'] != 0:
                continue
            for line in b["lines"]:
                spans = line["spans"]
                if not spans:
                    continue

                line_text = " ".join([span["text"] for span in spans])
                font_size = spans[0]["size"]

                # Rule for heading levels
                if font_size > 20:
                    level = "H1"
                elif font_size > 16:
                    level = "H2"
                elif font_size > 12:
                    level = "H3"
                else:
                    continue

                outline.append({
                    "level": level,
                    "text": line_text.strip(),
                    "page": page_num
                })

    return {
        "title": title,
        "outline": outline
    }

def main():
    input_dir = "../input"
    output_dir = "../output"

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(input_dir, filename)
            result = extract_headings(filepath)

            out_filename = filename.replace(".pdf", ".json")
            with open(os.path.join(output_dir, out_filename), "w") as f:
                json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()

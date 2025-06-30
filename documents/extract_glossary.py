import re
import json

try:
    import pdfplumber
    PDF_LIB = 'pdfplumber'
except ImportError:
    from PyPDF2 import PdfReader
    PDF_LIB = 'pypdf2'

PDF_PATH = "Siemens_Glossary_Sustainability_Terms.pdf"
OUTPUT_JSON = "full_siemens_glossary.json"

def extract_text_pdfplumber(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

def extract_text_pypdf2(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_terms_from_text(text):
    # Assume format: TERM\nDefinition text possibly spanning multiple lines\nNext TERM
    lines = text.splitlines()
    terms = {}
    current_term = None
    buffer = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Detect likely glossary term (all caps, short, not a sentence)
        if (len(line) < 50 and 
            (line.isupper() or (line[0].isupper() and not " " in line[1:5])) and
            not line.endswith('.')):
            # Save previous term
            if current_term and buffer:
                terms[current_term] = {"content": " ".join(buffer).strip()}
                buffer = []
            current_term = line
        elif current_term:
            buffer.append(line)
    # Save last one
    if current_term and buffer:
        terms[current_term] = {"content": " ".join(buffer).strip()}
    return terms

def main():
    if PDF_LIB == 'pdfplumber':
        text = extract_text_pdfplumber(PDF_PATH)
    else:
        text = extract_text_pypdf2(PDF_PATH)
    terms = extract_terms_from_text(text)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(terms, f, ensure_ascii=False, indent=2)
    print(f"Extracted {len(terms)} glossary terms to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()

import pdfplumber
import re
import json

pdf_path = "Siemens_Glossary_Sustainability_Terms.pdf"
output_json = "full_siemens_glossary.json"
glossary = {}

with pdfplumber.open(pdf_path) as pdf:
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += "\n" + page_text

# Clean up text
text = text.replace('\r', '\n').replace('\u2022', '-')

# Regex to find terms (term is all-caps or Title Case, then a colon or a line break, then definition)
blocks = re.split(r'\n(?=[A-Z][A-Za-z0-9 \-\/\(\)&®™]+\n)', text)

for block in blocks:
    lines = block.strip().split('\n', 1)
    if len(lines) == 2:
        term, definition = lines[0].strip(), lines[1].strip()
        if len(term) < 80 and len(definition) > 0:
            glossary[term] = {
                "content": f"{term}: {definition}",
                "source": "Siemens Glossary Sustainability Terms and Abbreviations, Status: 24.06.2025",
                "section": term,
                "authority": "high"
            }

with open(output_json, "w", encoding="utf-8") as f:
    json.dump(glossary, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(glossary)} terms to {output_json}")

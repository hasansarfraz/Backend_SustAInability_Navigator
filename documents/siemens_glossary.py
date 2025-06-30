import json
from pathlib import Path

GLOSSARY_PATH = Path(__file__).parent / "full_siemens_glossary.json"

with open(GLOSSARY_PATH, encoding="utf-8") as f:
    SIEMENS_OFFICIAL_CONTENT = json.load(f)

def get_all_document_chunks():
    """Return all official Siemens glossary/document chunks."""
    return SIEMENS_OFFICIAL_CONTENT

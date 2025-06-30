"""
Advanced document processing for multiple file formats
Handles PDFs, Word docs, text files, and structured data
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple
import re
from pathlib import Path
import openai

# For PDF processing
try:
    import PyPDF2
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    
# For Word document processing  
try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

logger = logging.getLogger(__name__)

class AdvancedDocumentProcessor:
    """Advanced document processing with intelligent chunking"""
    
    def __init__(self, openai_client):
        self.openai_client = openai_client
        self.chunk_size = 1000
        self.chunk_overlap = 200
        
    async def process_document(self, file_path: str, document_metadata: Dict = None) -> List[Dict]:
        """Process a document and return intelligent chunks"""
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return []
        
        # Extract text based on file type
        if file_path.suffix.lower() == '.pdf':
            text = self._extract_pdf_text(file_path)
        elif file_path.suffix.lower() == '.docx':
            text = self._extract_docx_text(file_path)
        elif file_path.suffix.lower() == '.txt':
            text = self._extract_txt_text(file_path)
        else:
            logger.warning(f"Unsupported file type: {file_path.suffix}")
            return []
        
        if not text.strip():
            logger.warning(f"No text extracted from {file_path}")
            return []
        
        # Intelligent chunking
        chunks = self._intelligent_chunk_document(text, file_path.name, document_metadata)
        
        # Create embeddings for chunks
        processed_chunks = []
        for i, chunk in enumerate(chunks):
            try:
                embedding_response = await self.openai_client.embeddings.acreate(
                    model="text-embedding-3-small",
                    input=chunk['content']
                )
                
                chunk['embedding'] = embedding_response.data[0].embedding
                chunk['chunk_id'] = f"{file_path.stem}_{i}"
                processed_chunks.append(chunk)
                
            except Exception as e:
                logger.error(f"Error creating embedding for chunk {i}: {e}")
        
        logger.info(f"Processed {len(processed_chunks)} chunks from {file_path.name}")
        return processed_chunks
    
    def _extract_pdf_text(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        if not PDF_AVAILABLE:
            logger.error("PDF processing libraries not available. Install: pip install PyPDF2 pdfplumber")
            return ""
        
        text = ""
        try:
            # Try pdfplumber first (better for complex layouts)
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception:
            # Fallback to PyPDF2
            try:
                import PyPDF2
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e:
                logger.error(f"Error extracting PDF text: {e}")
        
        return text
    
    def _extract_docx_text(self, file_path: Path) -> str:
        """Extract text from Word document"""
        if not DOCX_AVAILABLE:
            logger.error("DOCX processing library not available. Install: pip install python-docx")
            return ""
        
        try:
            import docx
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting DOCX text: {e}")
            return ""
    
    def _extract_txt_text(self, file_path: Path) -> str:
        """Extract text from text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error reading text file: {e}")
            return ""
    
    def _intelligent_chunk_document(self, text: str, filename: str, metadata: Dict = None) -> List[Dict]:
        """Intelligently chunk document based on structure"""
        
        # Detect document type and structure
        if self._is_glossary_document(text, filename):
            return self._chunk_glossary_document(text, filename, metadata)
        elif self._is_manual_document(text, filename):
            return self._chunk_manual_document(text, filename, metadata)
        elif self._is_report_document(text, filename):
            return self._chunk_report_document(text, filename, metadata)
        else:
            return self._chunk_generic_document(text, filename, metadata)
    
    def _is_glossary_document(self, text: str, filename: str) -> bool:
        """Detect if document is a glossary"""
        glossary_indicators = ["glossary", "terms", "definitions", "abbreviations"]
        filename_lower = filename.lower()
        return any(indicator in filename_lower for indicator in glossary_indicators)
    
    def _is_manual_document(self, text: str, filename: str) -> bool:
        """Detect if document is a user manual"""
        manual_indicators = ["manual", "guide", "user", "instructions"]
        filename_lower = filename.lower()
        return any(indicator in filename_lower for indicator in manual_indicators)
    
    def _is_report_document(self, text: str, filename: str) -> bool:
        """Detect if document is a report"""
        report_indicators = ["report", "annual", "sustainability", "esg"]
        filename_lower = filename.lower()
        return any(indicator in filename_lower for indicator in report_indicators)
    
    def _chunk_glossary_document(self, text: str, filename: str, metadata: Dict) -> List[Dict]:
        """Chunk glossary documents by term definitions"""
        chunks = []
        
        # Split by term patterns (assuming terms are in title case or all caps)
        sections = re.split(r'\n\n([A-Z][A-Za-z\s®™©\(\)]+)\n', text)
        
        current_term = None
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # Check if this looks like a term name
            if len(section.split()) <= 8 and (section[0].isupper() or section.isupper()):
                current_term = section
            elif current_term and len(section) > 50:  # This looks like a definition
                chunks.append({
                    'content': f"**{current_term}**\n\n{section}",
                    'section_title': current_term,
                    'document_type': 'glossary',
                    'source_document': filename,
                    'metadata': {
                        'term': current_term,
                        'document_type': 'glossary',
                        'authority': 'high',
                        **(metadata if metadata else {})
                    }
                })
                current_term = None
        
        return chunks
    
    def _chunk_manual_document(self, text: str, filename: str, metadata: Dict) -> List[Dict]:
        """Chunk manual documents by sections"""
        chunks = []
        
        # Split by section headers (numbered sections, etc.)
        sections = re.split(r'\n\n(?=\d+\.?\s+[A-Z])', text)
        
        for i, section in enumerate(sections):
            if len(section.strip()) < 100:  # Skip very short sections
                continue
            
            # Extract section title
            lines = section.strip().split('\n')
            section_title = lines[0] if lines else f"Section {i+1}"
            
            # Create chunks if section is too long
            if len(section) > self.chunk_size:
                sub_chunks = self._split_long_section(section, section_title)
                chunks.extend(sub_chunks)
            else:
                chunks.append({
                    'content': section.strip(),
                    'section_title': section_title,
                    'document_type': 'manual',
                    'source_document': filename,
                    'metadata': {
                        'section': section_title,
                        'document_type': 'manual',
                        'authority': 'high',
                        **(metadata if metadata else {})
                    }
                })
        
        return chunks
    
    def _chunk_report_document(self, text: str, filename: str, metadata: Dict) -> List[Dict]:
        """Chunk report documents by logical sections"""
        chunks = []
        
        # Split by major sections (Executive Summary, Introduction, etc.)
        section_patterns = [
            r'\n\n(Executive Summary)',
            r'\n\n(Introduction)',
            r'\n\n(Methodology)',
            r'\n\n(Results?)',
            r'\n\n(Discussion)',
            r'\n\n(Conclusion)',
            r'\n\n(Recommendations?)',
            r'\n\n([A-Z][A-Za-z\s]+(?:Summary|Overview|Analysis))'
        ]
        
        # Generic chunking for reports
        paragraphs = text.split('\n\n')
        current_chunk = ""
        current_section = "Report Content"
        
        for paragraph in paragraphs:
            # Check if this looks like a section header
            if len(paragraph.split()) <= 5 and paragraph.strip().istitle():
                # Save current chunk
                if len(current_chunk) > 200:
                    chunks.append({
                        'content': current_chunk.strip(),
                        'section_title': current_section,
                        'document_type': 'report',
                        'source_document': filename,
                        'metadata': {
                            'section': current_section,
                            'document_type': 'report',
                            'authority': 'medium',
                            **(metadata if metadata else {})
                        }
                    })
                current_section = paragraph.strip()
                current_chunk = ""
            else:
                current_chunk += paragraph + "\n\n"
                
                # Split if chunk gets too large
                if len(current_chunk) > self.chunk_size:
                    chunks.append({
                        'content': current_chunk.strip(),
                        'section_title': current_section,
                        'document_type': 'report',
                        'source_document': filename,
                        'metadata': {
                            'section': current_section,
                            'document_type': 'report',
                            'authority': 'medium',
                            **(metadata if metadata else {})
                        }
                    })
                    current_chunk = ""
        
        # Add final chunk
        if len(current_chunk.strip()) > 200:
            chunks.append({
                'content': current_chunk.strip(),
                'section_title': current_section,
                'document_type': 'report',
                'source_document': filename,
                'metadata': {
                    'section': current_section,
                    'document_type': 'report',
                    'authority': 'medium',
                    **(metadata if metadata else {})
                }
            })
        
        return chunks
    
    def _chunk_generic_document(self, text: str, filename: str, metadata: Dict) -> List[Dict]:
        """Generic chunking for unknown document types"""
        chunks = []
        
        # Simple paragraph-based chunking
        paragraphs = text.split('\n\n')
        current_chunk = ""
        chunk_index = 0
        
        for paragraph in paragraphs:
            if len(current_chunk + paragraph) > self.chunk_size:
                if current_chunk.strip():
                    chunks.append({
                        'content': current_chunk.strip(),
                        'section_title': f"Section {chunk_index + 1}",
                        'document_type': 'generic',
                        'source_document': filename,
                        'metadata': {
                            'chunk_index': chunk_index,
                            'document_type': 'generic',
                            'authority': 'medium',
                            **(metadata if metadata else {})
                        }
                    })
                    chunk_index += 1
                current_chunk = paragraph
            else:
                current_chunk += "\n\n" + paragraph
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append({
                'content': current_chunk.strip(),
                'section_title': f"Section {chunk_index + 1}",
                'document_type': 'generic',
                'source_document': filename,
                'metadata': {
                    'chunk_index': chunk_index,
                    'document_type': 'generic',
                    'authority': 'medium',
                    **(metadata if metadata else {})
                }
            })
        
        return chunks
    
    def _split_long_section(self, section: str, section_title: str) -> List[Dict]:
        """Split long sections into smaller chunks"""
        chunks = []
        sentences = section.split('. ')
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence) > self.chunk_size:
                if current_chunk.strip():
                    chunks.append({
                        'content': current_chunk.strip(),
                        'section_title': section_title,
                        'is_partial': True
                    })
                current_chunk = sentence
            else:
                current_chunk += sentence + ". "
        
        if current_chunk.strip():
            chunks.append({
                'content': current_chunk.strip(),
                'section_title': section_title,
                'is_partial': True
            })
        
        return chunks

# Document metadata templates
SIEMENS_DOCUMENT_METADATA = {
    "dbo_manual": {
        "authority": "high",
        "product": "DBO",
        "version": "1.2.2",
        "date": "2025-03-01",
        "document_type": "user_manual"
    },
    "sustainability_glossary": {
        "authority": "high",
        "scope": "sustainability_terms",
        "version": "24.06.2025", 
        "document_type": "glossary"
    },
    "xcelerator_docs": {
        "authority": "high",
        "product": "Xcelerator",
        "scope": "platform_documentation",
        "document_type": "technical_documentation"
    }
}
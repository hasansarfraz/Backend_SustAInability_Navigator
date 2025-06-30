"""
Document management service for processing and chunking documents
"""

import os
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import hashlib
import PyPDF2
import docx
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class DocumentChunk:
    """Represents a chunk of a document"""
    content: str
    chunk_id: str
    source_document: str
    document_type: str
    section_title: str
    chunk_index: int
    metadata: Dict[str, Any]

class DocumentManager:
    """Manages document processing, chunking, and metadata"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.processed_documents = {}
        
    async def process_document(self, file_path: str, document_type: str = "general") -> List[DocumentChunk]:
        """Process a document into chunks"""
        
        # Extract content based on file type
        if file_path.endswith('.pdf'):
            content = await self._extract_pdf(file_path)
        elif file_path.endswith('.docx'):
            content = await self._extract_docx(file_path)
        elif file_path.endswith(('.txt', '.md')):
            content = await self._extract_text(file_path)
        else:
            logger.warning(f"Unsupported file type: {file_path}")
            return []
        
        # Chunk the content
        chunks = self._chunk_text(content)
        
        # Create DocumentChunk objects
        document_chunks = []
        source_name = os.path.basename(file_path)
        
        for i, chunk_text in enumerate(chunks):
            chunk_id = hashlib.md5(f"{source_name}_{i}_{chunk_text[:50]}".encode()).hexdigest()
            
            chunk = DocumentChunk(
                content=chunk_text,
                chunk_id=chunk_id,
                source_document=source_name,
                document_type=document_type,
                section_title=f"Section {i+1}",
                chunk_index=i,
                metadata={
                    'file_path': file_path,
                    'processed_at': datetime.now().isoformat(),
                    'chunk_size': len(chunk_text)
                }
            )
            document_chunks.append(chunk)
        
        # Store processed document info
        self.processed_documents[source_name] = {
            'chunks': len(document_chunks),
            'processed_at': datetime.now().isoformat(),
            'document_type': document_type
        }
        
        logger.info(f"Processed {source_name}: {len(document_chunks)} chunks")
        return document_chunks
    
    async def _extract_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n\n"
        except Exception as e:
            logger.error(f"Error extracting PDF {file_path}: {e}")
        return text
    
    async def _extract_docx(self, file_path: str) -> str:
        """Extract text from Word document"""
        text = ""
        try:
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            logger.error(f"Error extracting DOCX {file_path}: {e}")
        return text
    
    async def _extract_text(self, file_path: str) -> str:
        """Extract text from plain text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error reading text file {file_path}: {e}")
            return ""
    
    def _chunk_text(self, text: str) -> List[str]:
        """Chunk text with overlap"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Find a good breaking point (end of sentence)
            if end < len(text):
                # Look for sentence endings
                for punct in ['. ', '.\n', '! ', '? ']:
                    last_punct = text.rfind(punct, start, end)
                    if last_punct != -1:
                        end = last_punct + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start with overlap
            start = end - self.chunk_overlap
        
        return chunks
    
    def get_document_stats(self) -> Dict:
        """Get statistics about processed documents"""
        return {
            'total_documents': len(self.processed_documents),
            'documents': self.processed_documents
        }
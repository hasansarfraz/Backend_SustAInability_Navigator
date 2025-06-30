"""
Document management system for handling multiple official documents
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional
from .document_processor import AdvancedDocumentProcessor, SIEMENS_DOCUMENT_METADATA

logger = logging.getLogger(__name__)

class DocumentManager:
    """Manages multiple official documents and their processing"""
    
    def __init__(self, openai_client):
        self.openai_client = openai_client
        self.processor = AdvancedDocumentProcessor(openai_client)
        self.documents = {}
        self.document_chunks = {}
        self.document_embeddings = {}
        
    async def add_documents_from_directory(self, directory_path: str):
        """Add all documents from a directory"""
        directory = Path(directory_path)
        
        if not directory.exists():
            logger.error(f"Directory not found: {directory_path}")
            return
        
        # Process all supported files
        supported_extensions = ['.pdf', '.docx', '.txt']
        
        for file_path in directory.rglob('*'):
            if file_path.suffix.lower() in supported_extensions:
                await self.add_document(str(file_path))
    
    async def add_document(self, file_path: str, metadata: Dict = None):
        """Add a single document to the system"""
        
        logger.info(f"Processing document: {file_path}")
        
        # Determine metadata based on filename
        file_name = Path(file_path).name.lower()
        if not metadata:
            metadata = self._get_metadata_for_file(file_name)
        
        # Process the document
        chunks = await self.processor.process_document(file_path, metadata)
        
        if chunks:
            doc_id = Path(file_path).stem
            self.documents[doc_id] = {
                'file_path': file_path,
                'metadata': metadata,
                'chunk_count': len(chunks)
            }
            
            # Store chunks and embeddings
            for chunk in chunks:
                chunk_id = chunk['chunk_id']
                self.document_chunks[chunk_id] = chunk
                self.document_embeddings[chunk_id] = chunk['embedding']
            
            logger.info(f"Added document {doc_id} with {len(chunks)} chunks")
        else:
            logger.warning(f"No chunks extracted from {file_path}")
    
    def _get_metadata_for_file(self, filename: str) -> Dict:
        """Get appropriate metadata based on filename"""
        
        if 'dbo' in filename and 'manual' in filename:
            return SIEMENS_DOCUMENT_METADATA['dbo_manual'].copy()
        elif 'glossary' in filename or 'terms' in filename:
            return SIEMENS_DOCUMENT_METADATA['sustainability_glossary'].copy()
        elif 'xcelerator' in filename:
            return SIEMENS_DOCUMENT_METADATA['xcelerator_docs'].copy()
        else:
            return {
                'authority': 'medium',
                'document_type': 'general',
                'source': 'siemens_documentation'
            }
    
    async def search_documents(self, query: str, top_k: int = 5, authority_filter: str = None) -> List[Dict]:
        """Search across all documents with optional filtering"""
        
        if not self.document_embeddings:
            logger.warning("No documents loaded")
            return []
        
        try:
            # Create query embedding
            response = await self.openai_client.embeddings.acreate(
                model="text-embedding-3-small",
                input=query
            )
            query_embedding = response.data[0].embedding
            
            # Calculate similarities
            similarities = {}
            for chunk_id, chunk_embedding in self.document_embeddings.items():
                chunk = self.document_chunks[chunk_id]
                
                # Apply authority filter if specified
                if authority_filter and chunk['metadata'].get('authority') != authority_filter:
                    continue
                
                similarity = self._cosine_similarity(query_embedding, chunk_embedding)
                similarities[chunk_id] = similarity
            
            # Get top results
            results = []
            for chunk_id, similarity in sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_k]:
                if similarity > 0.65:  # Confidence threshold
                    chunk = self.document_chunks[chunk_id]
                    results.append({
                        'chunk_id': chunk_id,
                        'content': chunk['content'],
                        'section_title': chunk['section_title'],
                        'source_document': chunk['source_document'],
                        'document_type': chunk['document_type'],
                        'metadata': chunk['metadata'],
                        'similarity': similarity
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error in document search: {e}")
            return []
    
    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors"""
        import numpy as np
        vec1, vec2 = np.array(vec1), np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def get_document_stats(self) -> Dict:
        """Get statistics about loaded documents"""
        return {
            'total_documents': len(self.documents),
            'total_chunks': len(self.document_chunks),
            'documents_by_type': self._get_docs_by_type(),
            'documents_by_authority': self._get_docs_by_authority()
        }
    
    def _get_docs_by_type(self) -> Dict:
        """Group documents by type"""
        type_counts = {}
        for chunk in self.document_chunks.values():
            doc_type = chunk['document_type']
            type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
        return type_counts
    
    def _get_docs_by_authority(self) -> Dict:
        """Group documents by authority level"""
        authority_counts = {}
        for chunk in self.document_chunks.values():
            authority = chunk['metadata'].get('authority', 'unknown')
            authority_counts[authority] = authority_counts.get(authority, 0) + 1
        return authority_counts
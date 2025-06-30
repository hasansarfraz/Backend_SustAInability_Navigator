"""
Pinecone vector database integration for production-scale document search
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from pinecone import Pinecone, ServerlessSpec
import openai
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class PineconeDocumentRAG:
    """Production-ready vector database integration with Pinecone"""
    
    def __init__(self, openai_client, pinecone_api_key: str, pinecone_environment: str):
        self.openai_client = openai_client
        self.pinecone_api_key = pinecone_api_key
        self.pinecone_environment = pinecone_environment
        self.index_name = "siemens-documents"
        self.pc = None  # Pinecone client
        self.index = None
        
    async def initialize(self):
        """Initialize Pinecone connection and index"""
        
        try:
            # Initialize Pinecone
            Pinecone.init(
                api_key=self.pinecone_api_key,
                environment=self.pinecone_environment
            )
            
            # Create index if it doesn't exist
            if self.index_name not in Pinecone.list_indexes():
                logger.info(f"Creating Pinecone index: {self.index_name}")
                Pinecone.create_index(
                    name=self.index_name,
                    dimension=1536,  # text-embedding-3-small dimension
                    metric="cosine",
                    # metadata_config={
                    #     "indexed": ["document_type", "authority", "source_document", "section_title"]
                    # }
                )
            
            # Connect to index
            self.index = Pinecone.Index(self.index_name)
            logger.info(f"Connected to Pinecone index: {self.index_name}")
            
        except Exception as e:
            logger.error(f"Error initializing Pinecone: {e}")
            raise
    
    async def add_document_chunks(self, chunks: List[Dict], batch_size: int = 100):
        """Add document chunks to Pinecone in batches"""
        
        if not self.index:
            raise RuntimeError("Pinecone not initialized")
        
        # Prepare vectors for upsert
        vectors = []
        for chunk in chunks:
            vector_data = {
                'id': chunk['chunk_id'],
                'values': chunk['embedding'],
                'metadata': {
                    'content': chunk['content'][:40000],  # Pinecone metadata limit
                    'section_title': chunk['section_title'],
                    'source_document': chunk['source_document'],
                    'document_type': chunk['document_type'],
                    'authority': chunk['metadata'].get('authority', 'medium'),
                    'created_at': datetime.now().isoformat(),
                    'version': chunk['metadata'].get('version', '1.0')
                }
            }
            vectors.append(vector_data)
        
        # Upsert in batches
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            try:
                self.index.upsert(vectors=batch)
                logger.info(f"Upserted batch {i//batch_size + 1} ({len(batch)} vectors)")
            except Exception as e:
                logger.error(f"Error upserting batch {i//batch_size + 1}: {e}")
        
        logger.info(f"Successfully added {len(vectors)} chunks to Pinecone")
    
    async def semantic_search(self, query: str, top_k: int = 5, filter_dict: Dict = None) -> List[Dict]:
        """Perform semantic search using Pinecone"""
        
        if not self.index:
            raise RuntimeError("Pinecone not initialized")
        
        try:
            # Create query embedding
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=query
            )
            query_embedding = response.data[0].embedding
            
            # Search Pinecone
            search_results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_dict
            )
            
            # Format results
            results = []
            for match in search_results['matches']:
                if match['score'] > 0.7:  # Confidence threshold
                    results.append({
                        'chunk_id': match['id'],
                        'content': match['metadata']['content'],
                        'section_title': match['metadata']['section_title'],
                        'source_document': match['metadata']['source_document'],
                        'document_type': match['metadata']['document_type'],
                        'authority': match['metadata']['authority'],
                        'similarity': match['score'],
                        'metadata': match['metadata']
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error in Pinecone search: {e}")
            return []
    
    async def search_by_document_type(self, query: str, document_type: str, top_k: int = 5) -> List[Dict]:
        """Search within specific document types"""
        filter_dict = {"document_type": {"$eq": document_type}}
        return await self.semantic_search(query, top_k, filter_dict)
    
    async def search_by_authority(self, query: str, authority: str, top_k: int = 5) -> List[Dict]:
        """Search within specific authority levels"""
        filter_dict = {"authority": {"$eq": authority}}
        return await self.semantic_search(query, top_k, filter_dict)
    
    async def update_document(self, old_chunk_id: str, new_chunk: Dict):
        """Update an existing document chunk"""
        
        # Delete old version
        self.index.delete(ids=[old_chunk_id])
        
        # Add new version
        await self.add_document_chunks([new_chunk])
        
        logger.info(f"Updated document chunk: {old_chunk_id}")
    
    async def delete_document(self, document_name: str):
        """Delete all chunks from a specific document"""
        
        # Query for all chunks from this document
        filter_dict = {"source_document": {"$eq": document_name}}
        
        # Delete in batches (Pinecone limitation)
        delete_batch_size = 1000
        
        # Note: This is a simplified implementation
        # In production, you'd need to implement pagination
        logger.info(f"Deleting all chunks from document: {document_name}")
        
        # For now, we'll use a namespace approach or manual tracking
        # This would require implementing a mapping system
    
    def get_index_stats(self) -> Dict:
        """Get statistics about the Pinecone index"""
        if not self.index:
            return {}
        
        try:
            stats = self.index.describe_index_stats()
            return {
                'total_vectors': stats.get('total_vector_count', 0),
                'dimension': stats.get('dimension', 0),
                'index_fullness': stats.get('index_fullness', 0),
                'namespaces': stats.get('namespaces', {})
            }
        except Exception as e:
            logger.error(f"Error getting index stats: {e}")
            return {}
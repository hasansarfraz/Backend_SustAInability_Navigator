"""
Document Intelligence Service for Semantic Search on Official Siemens Documents
Prevents hallucinations by grounding responses in authoritative sources
"""

import os
import logging
from typing import List, Dict, Optional, Tuple
import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)

@dataclass
class DocumentChunk:
    """Represents a chunk of official documentation"""
    content: str
    source_document: str
    section_title: str
    chunk_index: int
    metadata: Dict
    embedding: Optional[List[float]] = None

class DocumentIntelligenceService:
    """
    Enterprise-grade document intelligence using semantic search
    Prevents hallucinations by grounding responses in official Siemens documentation
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.embedding_model = "text-embedding-3-small"
        self.document_chunks = []
        self.embeddings_matrix = None
        self.confidence_threshold = 0.7
        
        # Official Siemens content
        self.siemens_glossary = {}
        self.dbo_manual_sections = {}
        
    async def initialize(self):
        """Initialize document intelligence with official Siemens documents"""
        logger.info("Initializing Document Intelligence Service...")
        
        # Load official documents
        await self._load_siemens_glossary()
        await self._load_dbo_manual()
        
        # Create embeddings for all documents
        await self._create_document_embeddings()
        
        logger.info(f"Document Intelligence initialized with {len(self.document_chunks)} chunks")
        
    async def _load_siemens_glossary(self):
        """Load the official Siemens Glossary content"""
        
        # Based on the Siemens Glossary document you have
        self.siemens_glossary = {
            "dbo": {
                "term": "Digital Business Optimizer (DBO™)",
                "definition": """The Digital Business Optimizer (DBO™), brought to you by Siemens Financial Services, Inc., is your trusted companion in the journey toward a greener future. Developed by Siemens Technology, the DBO™ offers an interactive platform to explore the technology investment options for decarbonizing your facility's energy consumption.

Key Features:
- Customized Decarbonization Strategy
- Data-Driven Insights
- Tailored Scenarios
- Competitive Edge
- Navigating Complexity

Website: https://www.dbo.siemens.com/""",
                "source": "Official Siemens Glossary of Sustainability Terms and Abbreviations, Status: 24.06.2025"
            },
            "sigreen": {
                "term": "SiGREEN",
                "definition": """SiGREEN is a Siemens tool to contribute to decarbonization through digitalization. Customers and Siemens can manage the carbon footprint of products and track and improve product-related emissions based on reliable data.""",
                "source": "Official Siemens Glossary of Sustainability Terms and Abbreviations, Status: 24.06.2025"
            },
            "degree": {
                "term": "DEGREE Framework",
                "definition": """The Siemens framework for sustainability, which constitutes a 360-degree approach for all stakeholders. For each of the six focus areas of the DEGREE framework (Decarbonization, Ethics, Governance, Resource efficiency, Equity, Employability), key performance indicators underpin the ambitions.""",
                "source": "Official Siemens Glossary of Sustainability Terms and Abbreviations, Status: 24.06.2025"
            },
            "xcelerator": {
                "term": "Siemens Xcelerator",
                "definition": """Siemens Xcelerator is an open digital business platform that includes a curated portfolio of IoT-enabled hardware, software and digital services from Siemens and certified third parties.""",
                "source": "Official Siemens Documentation"
            }
        }
        
        # Convert glossary to document chunks
        for key, content in self.siemens_glossary.items():
            chunk = DocumentChunk(
                content=f"{content['term']}\n\n{content['definition']}",
                source_document=content['source'],
                section_title=content['term'],
                chunk_index=0,
                metadata={"type": "glossary", "term": key}
            )
            self.document_chunks.append(chunk)
            
    async def _load_dbo_manual(self):
        """Load sections from the DBO User Manual"""
        
        # Based on the DBO Manual document you have
        dbo_sections = [
            {
                "title": "What is DBO™?",
                "content": """The Digital Business Optimizer (DBO™) is a web-based tool designed to support small and medium-sized enterprises (SMEs) in their decarbonization journey. It provides technology investment options to reduce carbon emissions while optimizing energy costs.""",
                "source": "DBO User Manual v1.2.2"
            },
            {
                "title": "DBO™ Key Features",
                "content": """• Interactive platform for exploring decarbonization options
- Customized scenarios based on facility data
- ROI calculations for sustainability investments
- Integration with Siemens Financial Services
- Support for facilities in the contiguous United States""",
                "source": "DBO User Manual v1.2.2"
            }
        ]
        
        for idx, section in enumerate(dbo_sections):
            chunk = DocumentChunk(
                content=f"{section['title']}\n\n{section['content']}",
                source_document=section['source'],
                section_title=section['title'],
                chunk_index=idx,
                metadata={"type": "manual", "section": section['title']}
            )
            self.document_chunks.append(chunk)
            
    async def _create_document_embeddings(self):
        """Create embeddings for all document chunks"""
        embeddings = []
        
        for chunk in self.document_chunks:
            try:
                response = self.client.embeddings.create(
                    model=self.embedding_model,
                    input=chunk.content
                )
                chunk.embedding = response.data[0].embedding
                embeddings.append(chunk.embedding)
            except Exception as e:
                logger.error(f"Error creating embedding: {e}")
                embeddings.append(np.zeros(1536))  # Default embedding dimension
                
        # Create embeddings matrix for efficient search
        self.embeddings_matrix = np.array(embeddings)
        
    async def semantic_search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Perform semantic search on official documents"""
        
        # Create query embedding
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=query
            )
            query_embedding = np.array(response.data[0].embedding)
        except Exception as e:
            logger.error(f"Error creating query embedding: {e}")
            return []
            
        # Calculate similarities
        similarities = cosine_similarity([query_embedding], self.embeddings_matrix)[0]
        
        # Get top matches above threshold
        results = []
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        for idx in top_indices:
            if similarities[idx] >= self.confidence_threshold:
                chunk = self.document_chunks[idx]
                results.append({
                    "content": chunk.content,
                    "source": chunk.source_document,
                    "section": chunk.section_title,
                    "similarity": float(similarities[idx]),
                    "metadata": chunk.metadata
                })
                
        return results
        
    def get_term_count(self) -> int:
        """Get number of terms indexed"""
        return len(self.siemens_glossary)
        
    def get_document_count(self) -> int:
        """Get number of documents loaded"""
        sources = set(chunk.source_document for chunk in self.document_chunks)
        return len(sources)
        
    def get_chunk_count(self) -> int:
        """Get number of searchable chunks"""
        return len(self.document_chunks)
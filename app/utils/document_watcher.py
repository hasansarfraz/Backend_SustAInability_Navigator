"""
Document watcher for real-time monitoring and updates
"""

import os
import logging
from typing import List, Dict, Set
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class DocumentWatcher(FileSystemEventHandler):
    """Watches directories for document changes"""
    
    def __init__(self, document_manager, vector_db):
        self.document_manager = document_manager
        self.vector_db = vector_db
        self.watched_directories: Set[str] = set()
        self.observers: List[Observer] = []
        self.update_queue = asyncio.Queue()
        self.monitoring_stats = {
            'files_added': 0,
            'files_modified': 0,
            'files_deleted': 0,
            'last_update': None
        }
    
    def on_created(self, event):
        """Handle file creation"""
        if not event.is_directory:
            logger.info(f"New file detected: {event.src_path}")
            self.monitoring_stats['files_added'] += 1
            self.monitoring_stats['last_update'] = datetime.now().isoformat()
            asyncio.create_task(self._process_new_file(event.src_path))
    
    def on_modified(self, event):
        """Handle file modification"""
        if not event.is_directory:
            logger.info(f"File modified: {event.src_path}")
            self.monitoring_stats['files_modified'] += 1
            self.monitoring_stats['last_update'] = datetime.now().isoformat()
            asyncio.create_task(self._process_modified_file(event.src_path))
    
    def on_deleted(self, event):
        """Handle file deletion"""
        if not event.is_directory:
            logger.info(f"File deleted: {event.src_path}")
            self.monitoring_stats['files_deleted'] += 1
            self.monitoring_stats['last_update'] = datetime.now().isoformat()
            # In production, implement document removal from vector DB
    
    async def _process_new_file(self, file_path: str):
        """Process a newly added file"""
        try:
            # Determine document type based on directory
            document_type = self._determine_document_type(file_path)
            
            # Process document into chunks
            chunks = self.document_manager.process_document(file_path, document_type)
            
            # Add to vector database
            if self.vector_db and chunks:
                documents = [
                    {
                        'id': chunk.chunk_id,
                        'content': chunk.content,
                        'source_document': chunk.source_document,
                        'document_type': chunk.document_type,
                        'section_title': chunk.section_title,
                        'authority': 'high' if 'official' in file_path.lower() else 'medium'
                    }
                    for chunk in chunks
                ]
                self.vector_db.add_documents_batch(documents)
                
        except Exception as e:
            logger.error(f"Error processing new file {file_path}: {e}")
    
    async def _process_modified_file(self, file_path: str):
        """Process a modified file"""
        # In production, implement update logic
        # For now, treat as new file
        self._process_new_file(file_path)
    
    def _determine_document_type(self, file_path: str) -> str:
        """Determine document type based on path"""
        path_lower = file_path.lower()
        
        if 'official' in path_lower:
            return 'official_documentation'
        elif 'manual' in path_lower:
            return 'user_manual'
        elif 'report' in path_lower:
            return 'report'
        elif 'glossary' in path_lower:
            return 'glossary'
        else:
            return 'general'
    
    async def start_watching(self, directories: List[str]):
        """Start watching directories"""
        for directory in directories:
            if os.path.exists(directory):
                observer = Observer()
                observer.schedule(self, directory, recursive=True)
                observer.start()
                self.observers.append(observer)
                self.watched_directories.add(directory)
                logger.info(f"Started watching directory: {directory}")
            else:
                logger.warning(f"Directory does not exist: {directory}")
    
    def stop_watching(self):
        """Stop all observers"""
        for observer in self.observers:
            observer.stop()
            observer.join()
        logger.info("Stopped all document watchers")
    
    def get_monitoring_stats(self) -> Dict:
        """Get monitoring statistics"""
        return {
            'watched_directories': list(self.watched_directories),
            'monitoring_stats': self.monitoring_stats,
            'active_observers': len(self.observers)
        }
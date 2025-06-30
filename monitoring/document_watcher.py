"""
Real-time document monitoring and automatic re-processing
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Callable
import hashlib
import time
from datetime import datetime
import json

# For file system monitoring
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False

logger = logging.getLogger(__name__)

class DocumentChangeHandler(FileSystemEventHandler):
    """Handle file system events for document changes"""
    
    def __init__(self, callback: Callable):
        self.callback = callback
        self.supported_extensions = {'.pdf', '.docx', '.txt'}
        
    def on_modified(self, event):
        """Handle file modification events"""
        if not event.is_directory:
            file_path = Path(event.src_path)
            if file_path.suffix.lower() in self.supported_extensions:
                logger.info(f"Document modified: {file_path}")
                asyncio.create_task(self.callback('modified', str(file_path)))
    
    def on_created(self, event):
        """Handle file creation events"""
        if not event.is_directory:
            file_path = Path(event.src_path)
            if file_path.suffix.lower() in self.supported_extensions:
                logger.info(f"Document created: {file_path}")
                asyncio.create_task(self.callback('created', str(file_path)))
    
    def on_deleted(self, event):
        """Handle file deletion events"""
        if not event.is_directory:
            file_path = Path(event.src_path)
            if file_path.suffix.lower() in self.supported_extensions:
                logger.info(f"Document deleted: {file_path}")
                asyncio.create_task(self.callback('deleted', str(file_path)))

class DocumentWatcher:
    """Monitor documents for changes and trigger re-processing"""
    
    def __init__(self, document_manager, vector_db=None):
        self.document_manager = document_manager
        self.vector_db = vector_db
        self.watched_directories = set()
        self.observers = []
        self.document_hashes = {}
        self.change_queue = asyncio.Queue()
        
    async def start_watching(self, directory_paths: List[str]):
        """Start watching directories for document changes"""
        
        if not WATCHDOG_AVAILABLE:
            logger.warning("Watchdog not available. Install with: pip install watchdog")
            logger.info("Falling back to polling mode")
            await self._start_polling_mode(directory_paths)
            return
        
        for directory_path in directory_paths:
            directory = Path(directory_path)
            if directory.exists() and directory.is_dir():
                await self._watch_directory(directory)
            else:
                logger.warning(f"Directory not found: {directory_path}")
    
    async def _watch_directory(self, directory: Path):
        """Watch a specific directory for changes"""
        
        logger.info(f"Starting to watch directory: {directory}")
        
        # Create event handler
        event_handler = DocumentChangeHandler(self._handle_document_change)
        
        # Create observer
        observer = Observer()
        observer.schedule(event_handler, str(directory), recursive=True)
        observer.start()
        
        self.observers.append(observer)
        self.watched_directories.add(str(directory))
        
        # Initialize document hashes for change detection
        await self._initialize_document_hashes(directory)
    
    async def _initialize_document_hashes(self, directory: Path):
        """Initialize hashes for existing documents"""
        
        supported_extensions = {'.pdf', '.docx', '.txt'}
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                file_hash = await self._calculate_file_hash(file_path)
                self.document_hashes[str(file_path)] = {
                    'hash': file_hash,
                    'last_modified': file_path.stat().st_mtime,
                    'last_processed': datetime.now().isoformat()
                }
    
    async def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of a file"""
        
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {e}")
            return ""
    
    async def _handle_document_change(self, event_type: str, file_path: str):
        """Handle document change events"""
        
        logger.info(f"Processing {event_type} event for: {file_path}")
        
        try:
            if event_type in ['created', 'modified']:
                # Check if file actually changed
                if await self._has_file_changed(file_path):
                    await self._reprocess_document(file_path)
                    
            elif event_type == 'deleted':
                await self._remove_document(file_path)
                
        except Exception as e:
            logger.error(f"Error handling document change: {e}")
    
    async def _has_file_changed(self, file_path: str) -> bool:
        """Check if file has actually changed by comparing hashes"""
        
        current_hash = await self._calculate_file_hash(Path(file_path))
        stored_info = self.document_hashes.get(file_path)
        
        if not stored_info or stored_info['hash'] != current_hash:
            # File is new or changed
            self.document_hashes[file_path] = {
                'hash': current_hash,
                'last_modified': Path(file_path).stat().st_mtime,
                'last_processed': datetime.now().isoformat()
            }
            return True
        
        return False
    
    async def _reprocess_document(self, file_path: str):
        """Re-process a changed document"""
        
        logger.info(f"Re-processing document: {file_path}")
        
        try:
            # Remove old version if it exists
            if self.vector_db:
                document_name = Path(file_path).name
                await self._remove_document_from_vector_db(document_name)
            
            # Process new version
            await self.document_manager.add_document(file_path)
            
            logger.info(f"Successfully re-processed: {file_path}")
            
        except Exception as e:
            logger.error(f"Error re-processing document {file_path}: {e}")
    
    async def _remove_document(self, file_path: str):
        """Remove a deleted document from the system"""
        
        logger.info(f"Removing document: {file_path}")
        
        try:
            if self.vector_db:
                document_name = Path(file_path).name
                await self._remove_document_from_vector_db(document_name)
            
            # Remove from local tracking
            if file_path in self.document_hashes:
                del self.document_hashes[file_path]
            
            logger.info(f"Successfully removed: {file_path}")
            
        except Exception as e:
            logger.error(f"Error removing document {file_path}: {e}")
    
    async def _remove_document_from_vector_db(self, document_name: str):
        """Remove document from vector database"""
        
        if hasattr(self.vector_db, 'delete_document'):
            await self.vector_db.delete_document(document_name)
        else:
            logger.warning("Vector database doesn't support document deletion")
    
    async def _start_polling_mode(self, directory_paths: List[str]):
        """Fallback polling mode when watchdog is not available"""
        
        logger.info("Starting polling mode for document monitoring")
        
        # Initialize hashes for all directories
        for directory_path in directory_paths:
            directory = Path(directory_path)
            if directory.exists():
                await self._initialize_document_hashes(directory)
        
        # Start polling task
        asyncio.create_task(self._polling_task(directory_paths))
    
    async def _polling_task(self, directory_paths: List[str]):
        """Polling task to check for document changes"""
        
        while True:
            try:
                for directory_path in directory_paths:
                    directory = Path(directory_path)
                    if directory.exists():
                        await self._check_directory_for_changes(directory)
                
                # Wait before next poll
                await asyncio.sleep(30)  # Poll every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in polling task: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _check_directory_for_changes(self, directory: Path):
        """Check directory for any changes"""
        
        supported_extensions = {'.pdf', '.docx', '.txt'}
        current_files = set()
        
        # Check all files in directory
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                file_path_str = str(file_path)
                current_files.add(file_path_str)
                
                # Check if file is new or modified
                if await self._has_file_changed(file_path_str):
                    await self._reprocess_document(file_path_str)
        
        # Check for deleted files
        tracked_files = set(self.document_hashes.keys())
        deleted_files = tracked_files - current_files
        
        for deleted_file in deleted_files:
            await self._remove_document(deleted_file)
    
    def stop_watching(self):
        """Stop all file system observers"""
        
        for observer in self.observers:
            observer.stop()
            observer.join()
        
        self.observers.clear()
        self.watched_directories.clear()
        
        logger.info("Stopped document watching")
    
    def get_monitoring_stats(self) -> Dict:
        """Get statistics about document monitoring"""
        
        return {
            'watched_directories': list(self.watched_directories),
            'tracked_documents': len(self.document_hashes),
            'active_observers': len(self.observers),
            'monitoring_mode': 'watchdog' if WATCHDOG_AVAILABLE else 'polling'
        }
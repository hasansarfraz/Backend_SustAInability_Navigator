# main.py - Complete updated version with RAG, Auth, and all new endpoints

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
from dotenv import load_dotenv
import os
from pathlib import Path
from documents.document_manager import DocumentManager
from monitoring.document_watcher import DocumentWatcher

# Import all routers
from app.routes.chat import router as chat_router
from app.routes.dbo import router as dbo_router
from app.routes.analytics import router as analytics_router
from app.routes.integration import router as integration_router
from app.services.auth_service import auth_router

# Import services
from app.services.dbo_service import dbo_service
from app.services.rag_agent_service import rag_agent  # New RAG service instead of LangChain
from app.services.xcelerator_service import xcelerator_service
from app.services.supabase_service import db_service

# Add to imports
from app.services.vector_db.pinecone_integration import PineconeDocumentRAG
from app.services.vector_db.document_manager import DocumentManager
from app.utils.document_watcher import DocumentWatcher

#vector_db_import
try:
    from vector_db.pinecone_integration import PineconeDocumentRAG
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="SustAInability Navigator - RAG Enhanced with Supabase",
    description="AI-powered sustainability assistant with RAG architecture, structured responses, and authentication",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS settings - Updated for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://spectacular-dusk-cc7b08.netlify.app",  # Frontend
        "http://localhost:3000",  # Local frontend development
        "http://localhost:3001",  # Alternative local port
        "http://localhost:5173",  # Vite default port
        "*"  # Be careful with this in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EnterpriseRAGAgent:
    """Enterprise wrapper for existing RAG agent with document intelligence"""
    
    def __init__(self, base_rag_agent):
        self.base_rag_agent = base_rag_agent
        self.document_manager = None
        self.vector_db = None
        self.document_watcher = None
        self.enterprise_initialized = False
        
    async def initialize_enterprise_features(self):
        """Initialize enterprise document intelligence features"""
        try:
            # Initialize document manager
            self.document_manager = DocumentManager(self.base_rag_agent.openai_client)
            
            # Initialize vector database (if available)
            vector_db_config = self._get_vector_db_config()
            if vector_db_config:
                self.vector_db = await self._initialize_vector_db(vector_db_config)
            
            # Load official documents
            await self._load_official_documents()
            
            # Initialize document monitoring
            self.document_watcher = DocumentWatcher(self.document_manager, self.vector_db)
            await self._start_document_monitoring()
            
            self.enterprise_initialized = True
            logger.info("✅ Enterprise document intelligence initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing enterprise features: {e}")
            self.enterprise_initialized = False
    
    def _get_vector_db_config(self):
        """Get vector database configuration from environment"""
        pinecone_key = os.getenv("PINECONE_API_KEY")
        pinecone_env = os.getenv("PINECONE_ENVIRONMENT", "us-east1-gcp")
        
        if pinecone_key and PINECONE_AVAILABLE:
            return {
                'type': 'pinecone',
                'api_key': pinecone_key,
                'environment': pinecone_env
            }
        # elif CHROMA_AVAILABLE:
        #     return {
        #         'type': 'chroma',
        #         'persist_directory': './chroma_db'
        #     }
        else:
            return None
    
    async def _initialize_vector_db(self, config):
        """Initialize vector database based on configuration"""
        try:
            if config['type'] == 'pinecone' and PINECONE_AVAILABLE:
                vector_db = PineconeDocumentRAG(
                    self.base_rag_agent.openai_client,
                    config['api_key'],
                    config['environment']
                )
                await vector_db.initialize()
                logger.info("✅ Pinecone vector database initialized")
                return vector_db
                
            # elif config['type'] == 'chroma' and CHROMA_AVAILABLE:
            #     vector_db = ChromaDocumentRAG(
            #         self.base_rag_agent.openai_client,
            #         config['persist_directory']
            #     )
            #     await vector_db.initialize()
            #     logger.info("✅ Chroma vector database initialized")
            #     return vector_db
                
        except Exception as e:
            logger.warning(f"⚠️ Vector database initialization failed: {e}")
            logger.info("📝 Falling back to in-memory document storage")
            return None
    
    async def _load_official_documents(self):
        """Load official Siemens documents"""
        # Create documents directories if they don't exist
        document_dirs = [
            "./documents/official",
            "./documents/manuals", 
            "./documents/reports"
        ]
        
        for dir_path in document_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        # Load from the siemens_glossary.py (your hardcoded official content)
        from documents.siemens_glossary import get_all_document_chunks
        official_content = get_all_document_chunks()
        
        # Process official content into document chunks
        document_count = 0
        for doc_id, doc_data in official_content.items():
            try:
                # Create embedding for the content
                response = self.base_rag_agent.openai_client.embeddings.create(
                    model="text-embedding-3-small",
                    input=doc_data["content"]
                )
                
                # Store in document manager
                chunk = {
                    'chunk_id': doc_id,
                    'content': doc_data["content"],
                    'section_title': doc_data.get("section", "Official Definition"),
                    'source_document': doc_data["source"],
                    'document_type': 'official_glossary',
                    'metadata': {
                        'authority': doc_data["authority"],
                        'keywords': doc_data.get("keywords", [])
                    },
                    'embedding': response.data[0].embedding
                }
                
                self.document_manager.document_chunks[doc_id] = chunk
                self.document_manager.document_embeddings[doc_id] = response.data[0].embedding
                document_count += 1
                
            except Exception as e:
                logger.error(f"Error processing document {doc_id}: {e}")
        
        logger.info(f"✅ Loaded {document_count} official Siemens documents")
        
        # Also load from directories if they contain files
        for dir_path in document_dirs:
            if any(Path(dir_path).iterdir()):
                await self.document_manager.add_documents_from_directory(dir_path)
    
    async def _start_document_monitoring(self):
        """Start monitoring document directories for changes"""
        document_dirs = [
            "./documents/official",
            "./documents/manuals",
            "./documents/reports"
        ]
        
        # Only start monitoring if directories exist and contain files
        dirs_to_monitor = [d for d in document_dirs if Path(d).exists()]
        
        if dirs_to_monitor:
            await self.document_watcher.start_watching(dirs_to_monitor)
            logger.info(f"✅ Document monitoring started for {len(dirs_to_monitor)} directories")
    
    async def search_documents(self, query: str, top_k: int = 3):
        """Search through official documents"""
        if self.document_manager:
            return await self.document_manager.search_documents(query, top_k)
        else:
            return []
    
    def get_enterprise_stats(self):
        """Get enterprise system statistics"""
        if not self.enterprise_initialized:
            return {"enterprise_features": "not_initialized"}
        
        stats = {}
        
        if self.document_manager:
            stats['documents'] = self.document_manager.get_document_stats()
        
        if self.document_watcher:
            stats['monitoring'] = self.document_watcher.get_monitoring_stats()
            
        if self.vector_db and hasattr(self.vector_db, 'get_index_stats'):
            stats['vector_db'] = self.vector_db.get_index_stats()
        elif self.vector_db and hasattr(self.vector_db, 'get_collection_stats'):
            stats['vector_db'] = self.vector_db.get_collection_stats()
        
        return stats
    
    # Delegate all other methods to the base RAG agent
    def __getattr__(self, name):
        return getattr(self.base_rag_agent, name)


@app.get("/")
def read_root():
    return {
        "message": "SustAInability Navigator - RAG Enhanced Version",
        "version": "3.0.0",
        "status": "healthy",
        "architecture": "RAG with Embeddings (No LangChain)",
        "features": [
            "RAG-based Agent with Embeddings",
            "5-Cluster Security System",
            "Structured Chat Responses",
            "User Authentication (JWT)",
            "Supabase Database Integration",
            "Chat History Management",
            "DBO Tool Integration",
            "Xcelerator Marketplace Matching",
            "Persona Intelligence"
        ],
        "api_endpoints": {
            "authentication": {
                "login": "POST /auth/login",
                "register": "POST /auth/register",
                "me": "GET /auth/me"
            },
            "chat": {
                "chat": "POST /chat/",
                "history": "GET /get_chat_history/{chat_ID}",
                "list": "GET /get_chats/"
            },
            "user": {
                "save_params": "POST /save_user_info/",
                "get_params": "GET /get_user_info/"
            },
            "dbo": {
                "scenarios": "GET /api/v1/dbo/scenarios",
                "scenario_detail": "POST /api/v1/dbo/scenario",
                "search": "GET /api/v1/dbo/scenarios/search"
            },
            "system": {
                "health": "GET /health",
                "info": "GET /api/v1/system/info"
            }
        },
        "security": {
            "authentication": "JWT-based",
            "prompt_security": "5-cluster system",
            "jailbreak_protection": "Active",
            "role_boundaries": "Enforced"
        }
    }

@app.get("/health")
def health_check():
    """Enhanced health check with all services status"""
    
    # Check RAG agent status
    rag_status = "operational"
    try:
        if hasattr(rag_agent, 'dbo_embeddings') and len(rag_agent.dbo_embeddings) > 0:
            rag_status = "operational"
        else:
            rag_status = "degraded"
    except:
        rag_status = "error"
    
    # Check database status
    db_status = "operational"
    try:
        # You might want to add a simple DB health check here
        if db_service and hasattr(db_service, 'client'):
            db_status = "operational"
        else:
            db_status = "not_initialized"
    except:
        db_status = "error"
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "3.0.0",
        "services": {
            "rag_agent": rag_status,
            "embeddings": {
                "dbo_scenarios": len(getattr(rag_agent, 'dbo_embeddings', {})),
                "xcelerator_products": len(getattr(rag_agent, 'product_embeddings', {}))
            },
            "database": db_status,
            "dbo_service": "operational" if dbo_service else "error",
            "xcelerator_service": "operational" if xcelerator_service else "error",
            "scenarios_loaded": len(dbo_service.scenarios) if dbo_service else 0,
            "xcelerator_products": len(xcelerator_service.xcelerator_catalog) if xcelerator_service else 0
        },
        "integration_status": {
            "dbo_scenarios": f"{len(dbo_service.scenarios) if dbo_service else 0} scenarios loaded",
            "xcelerator_catalog": f"{len(xcelerator_service.xcelerator_catalog) if xcelerator_service else 0} products available",
            "ai_architecture": "RAG with embeddings",
            "security_model": "5-cluster system",
            "structured_responses": "enabled",
            "user_profiles": "enabled",
            "chat_persistence": "enabled",
            "authentication": "JWT-based"
        },
        "configuration": {
            "external_access": getattr(rag_agent, 'external_access_enabled', False),
            "strict_boundaries": getattr(rag_agent, 'strict_role_boundaries', True),
            "cache_enabled": True,
            "embedding_model": getattr(rag_agent, 'embedding_model', 'unknown'),
            "chat_model": getattr(rag_agent, 'chat_model', 'unknown')
        }
    }

@app.get("/api/v1/system/info")
def get_system_info():
    """System information for frontend initialization"""
    return {
        "available_personas": [
            {"id": "zuri", "name": "Zuri", "description": "Enterprise Sustainability Leader"},
            {"id": "amina", "name": "Amina", "description": "Cost-Conscious Business Owner"},
            {"id": "bjorn", "name": "Björn", "description": "Siemens Customer"},
            {"id": "arjun", "name": "Arjun", "description": "Sustainability Champion"},
            {"id": "general", "name": "General", "description": "Default Assistant"}
        ],
        "available_actions": [
            {
                "action_type": "select_dbo_scenario",
                "description": "Explore a specific DBO scenario",
                "icon": "folder"
            },
            {
                "action_type": "contact_expert",
                "description": "Connect with a Siemens expert",
                "icon": "user"
            },
            {
                "action_type": "provide_information",
                "description": "Provide additional information",
                "icon": "info"
            },
            {
                "action_type": "use_tool",
                "description": "Use a sustainability tool",
                "icon": "tool"
            },
            {
                "action_type": "browse",
                "description": "Browse scenarios or products",
                "icon": "search"
            }
        ],
        "supported_languages": ["en"],  # Can be extended later
        "features": {
            "dbo_scenarios": True,
            "xcelerator_marketplace": True,
            "rag_search": True,
            "embeddings": True,
            "chat_history": True,
            "user_profiles": True,
            "authentication": True,
            "carbon_calculator": False,  # Coming soon
            "roi_calculator": False,     # Coming soon
            "expert_chat": True
        },
        "security_features": {
            "jailbreak_protection": True,
            "prompt_integrity": True,
            "role_boundaries": True,
            "audit_logging": True,
            "data_privacy": True
        },
        "api_version": "3.0.0",
        "build_date": datetime.now().strftime("%Y-%m-%d")
    }

# Include routers
# Authentication routes (no prefix as per standard practice)
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Chat routes at root level as per FrontEnd's specification
app.include_router(chat_router, prefix="", tags=["Chat & User Management"])

# API versioned routes
app.include_router(dbo_router, prefix="/api/v1/dbo", tags=["DBO Scenarios"])
app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(integration_router, prefix="/api/v1/integration", tags=["Siemens Integration"])

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services with enterprise document intelligence"""
    global rag_agent  # Make sure this is your existing global variable
    
    logger.info("=" * 70)
    logger.info("🚀 Starting SustAInability Navigator - Enterprise RAG Version")
    logger.info("=" * 70)
    
    # Check environment variables (your existing code + new ones)
    env_vars = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "not_set"),
        "SUPABASE_URL": os.getenv("SUPABASE_URL", "not_set"),
        "SUPABASE_ANON_KEY": os.getenv("SUPABASE_ANON_KEY", "not_set"),
        "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY", "not_set"),
        # ADD these new environment variables
        "PINECONE_API_KEY": os.getenv("PINECONE_API_KEY", "not_set"),
        "PINECONE_ENVIRONMENT": os.getenv("PINECONE_ENVIRONMENT", "us-east1-gcp")
    }
    
    # Log configuration status (your existing code)
    logger.info("📋 Configuration Status:")
    for var, value in env_vars.items():
        status = "✅" if value != "not_set" else "❌"
        logger.info(f"   {status} {var}: {'Set' if value != 'not_set' else 'Not Set'}")
    
    # Log service status (your existing code - keep all of it)
    logger.info("\n🔧 Service Status:")
    logger.info(f"   🌱 DBO Scenarios: {len(dbo_service.scenarios) if dbo_service else 0} loaded")
    logger.info(f"   🛒 Xcelerator Products: {len(xcelerator_service.xcelerator_catalog) if xcelerator_service else 0} available")
    logger.info(f"   🤖 RAG Agent: {'Initialized' if rag_agent else 'Not Initialized'}")
    logger.info(f"   📊 Embeddings: {len(getattr(rag_agent, 'dbo_embeddings', {}))} DBO, {len(getattr(rag_agent, 'product_embeddings', {}))} products")
    logger.info(f"   🗄️  Database: {'Connected' if db_service else 'Not Connected'}")
    logger.info(f"   🔐 Authentication: Enabled")
    logger.info(f"   💬 Chat System: Structured responses enabled")
    logger.info(f"   🛡️  Security: 5-cluster system active")
    
    # ADD new enterprise features initialization
    logger.info("\n🚀 Initializing Enterprise Document Intelligence...")
    
    if rag_agent:
        # Wrap your existing RAG agent with enterprise features
        enterprise_rag = EnterpriseRAGAgent(rag_agent)
        await enterprise_rag.initialize_enterprise_features()
        
        # Replace the global rag_agent with the enhanced version
        rag_agent = enterprise_rag
        
        # Log enterprise features status
        logger.info("\n📚 Enterprise Document Intelligence:")
        if enterprise_rag.enterprise_initialized:
            stats = enterprise_rag.get_enterprise_stats()
            
            # Document statistics
            if 'documents' in stats:
                doc_stats = stats['documents']
                logger.info(f"   📄 Documents: {doc_stats.get('total_documents', 0)} loaded")
                logger.info(f"   📝 Chunks: {doc_stats.get('total_chunks', 0)} processed")
                
                # Document types
                doc_types = doc_stats.get('documents_by_type', {})
                for doc_type, count in doc_types.items():
                    logger.info(f"   📋 {doc_type.title()}: {count} chunks")
            
            # Vector database status
            if 'vector_db' in stats:
                vector_stats = stats['vector_db']
                if 'total_vectors' in vector_stats:  # Pinecone
                    logger.info(f"   🗄️  Vector DB: Pinecone ({vector_stats['total_vectors']} vectors)")
                elif 'total_documents' in vector_stats:  # Chroma
                    logger.info(f"   🗄️  Vector DB: Chroma ({vector_stats['total_documents']} documents)")
            else:
                logger.info(f"   🗄️  Vector DB: In-memory storage")
            
            # Monitoring status
            if 'monitoring' in stats:
                monitor_stats = stats['monitoring']
                monitored_dirs = len(monitor_stats.get('watched_directories', []))
                logger.info(f"   👁️  Monitoring: {monitored_dirs} directories watched")
                logger.info(f"   🔄 Mode: {monitor_stats.get('monitoring_mode', 'disabled')}")
        else:
            logger.warning("   ⚠️  Enterprise features initialization failed")
    
    # Log architecture info (your existing code + enhancements)
    logger.info("\n🏗️  Architecture:")
    logger.info("   - RAG with embeddings (no LangChain)")
    logger.info("   - Semantic search for scenarios and products")
    logger.info("   - ReAct-style agent reasoning")
    logger.info("   - Supabase for data persistence")
    logger.info("   - JWT-based authentication")
    # ADD these new architecture features
    logger.info("   - Enterprise document intelligence")
    logger.info("   - Vector database integration (optional)")
    logger.info("   - Real-time document monitoring")
    logger.info("   - Multi-format document processing")
    
    # Log key features (your existing code + new features)
    logger.info("\n✨ Key Features:")
    logger.info("   ✅ Structured responses for frontend")
    logger.info("   ✅ Chat history with GET endpoint")
    logger.info("   ✅ User profile management")
    logger.info("   ✅ Persona-aware responses")
    logger.info("   ✅ Jailbreak protection")
    logger.info("   ✅ Professional boundaries enforced")
    # ADD these new enterprise features
    logger.info("   ✅ Official document grounding")
    logger.info("   ✅ Semantic search on Siemens documentation")
    logger.info("   ✅ Source attribution and citation")
    logger.info("   ✅ Anti-hallucination safeguards")
    logger.info("   ✅ Real-time document updates")
    
    logger.info("=" * 70)
    logger.info("🎯 Ready for Siemens Enterprise Demo!")
    logger.info("📝 API Documentation: http://localhost:8000/docs")
    logger.info("🔍 Enterprise Stats: http://localhost:8000/enterprise/stats")
    logger.info("=" * 70)

# ADD new enterprise endpoints
@app.get("/enterprise/stats")
async def get_enterprise_stats():
    """Get enterprise document intelligence statistics"""
    if rag_agent and hasattr(rag_agent, 'get_enterprise_stats'):
        return {
            "status": "success",
            "enterprise_features": rag_agent.get_enterprise_stats(),
            "timestamp": datetime.now().isoformat()
        }
    else:
        raise HTTPException(
            status_code=503, 
            detail="Enterprise features not initialized"
        )

@app.get("/enterprise/health")
async def enterprise_health_check():
    """Check health of enterprise document intelligence features"""
    if not rag_agent or not hasattr(rag_agent, 'enterprise_initialized'):
        return {
            "status": "enterprise_not_available",
            "message": "Enterprise features not initialized"
        }
    
    health_status = {
        "status": "healthy" if rag_agent.enterprise_initialized else "unhealthy",
        "enterprise_initialized": rag_agent.enterprise_initialized,
        "document_manager": rag_agent.document_manager is not None,
        "vector_db": rag_agent.vector_db is not None,
        "document_watcher": rag_agent.document_watcher is not None,
        "timestamp": datetime.now().isoformat()
    }
    
    return health_status

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down SustAInability Navigator")
    
    # Clean up any open connections
    if hasattr(rag_agent, 'conversation_memory'):
        logger.info(f"Clearing {len(rag_agent.conversation_memory)} conversation memories")
        rag_agent.conversation_memory.clear()
    
    # Clear response cache
    if hasattr(rag_agent, 'response_cache'):
        logger.info(f"Clearing {len(rag_agent.response_cache)} cached responses")
        rag_agent.response_cache.clear()
    
    logger.info("Shutdown complete")

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or default
    port = int(os.getenv("PORT", 8000))
    
    # Run with auto-reload for development
    uvicorn.run(
        "main:app",  # Use string to enable auto-reload
        host="0.0.0.0", 
        port=port,
        reload=True if os.getenv("ENVIRONMENT", "development") == "development" else False,
        log_level="info"
    )
# main.py - Complete updated version with RAG, Auth, and all new endpoints

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
from dotenv import load_dotenv
import os

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
    """Initialize services on startup"""
    logger.info("=" * 70)
    logger.info("🚀 Starting SustAInability Navigator - RAG Enhanced Version")
    logger.info("=" * 70)
    
    # Check environment variables
    env_vars = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "not_set"),
        "SUPABASE_URL": os.getenv("SUPABASE_URL", "not_set"),
        "SUPABASE_ANON_KEY": os.getenv("SUPABASE_ANON_KEY", "not_set"),
        "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY", "not_set")
    }
    
    # Log configuration status
    logger.info("📋 Configuration Status:")
    for var, value in env_vars.items():
        status = "✅" if value != "not_set" else "❌"
        logger.info(f"   {status} {var}: {'Set' if value != 'not_set' else 'Not Set'}")
    
    # Log service status
    logger.info("\n🔧 Service Status:")
    logger.info(f"   🌱 DBO Scenarios: {len(dbo_service.scenarios) if dbo_service else 0} loaded")
    logger.info(f"   🛒 Xcelerator Products: {len(xcelerator_service.xcelerator_catalog) if xcelerator_service else 0} available")
    logger.info(f"   🤖 RAG Agent: {'Initialized' if rag_agent else 'Not Initialized'}")
    logger.info(f"   📊 Embeddings: {len(getattr(rag_agent, 'dbo_embeddings', {}))} DBO, {len(getattr(rag_agent, 'product_embeddings', {}))} products")
    logger.info(f"   🗄️  Database: {'Connected' if db_service else 'Not Connected'}")
    logger.info(f"   🔐 Authentication: Enabled")
    logger.info(f"   💬 Chat System: Structured responses enabled")
    logger.info(f"   🛡️  Security: 5-cluster system active")
    
    # Log architecture info
    logger.info("\n🏗️  Architecture:")
    logger.info("   - RAG with embeddings (no LangChain)")
    logger.info("   - Semantic search for scenarios and products")
    logger.info("   - ReAct-style agent reasoning")
    logger.info("   - Supabase for data persistence")
    logger.info("   - JWT-based authentication")
    
    # Log key features
    logger.info("\n✨ Key Features:")
    logger.info("   ✅ Structured responses for frontend")
    logger.info("   ✅ Chat history with GET endpoint")
    logger.info("   ✅ User profile management")
    logger.info("   ✅ Persona-aware responses")
    logger.info("   ✅ Jailbreak protection")
    logger.info("   ✅ Professional boundaries enforced")
    
    logger.info("=" * 70)
    logger.info("🎯 Ready for Siemens presentation!")
    logger.info("📝 API Documentation: http://localhost:8000/docs")
    logger.info("=" * 70)

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
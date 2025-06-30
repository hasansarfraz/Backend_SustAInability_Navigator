# main.py 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
from dotenv import load_dotenv

from app.routes.chat import router as chat_router
from app.routes.dbo import router as dbo_router
from app.routes.analytics import router as analytics_router
from app.routes.integration import router as integration_router
from app.services.dbo_service import dbo_service
from app.services.langchain_service import langchain_service
from app.services.xcelerator_service import xcelerator_service
from app.services.rag_agent_service import rag_agent


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SustAInability Navigator - Enhanced with Frontend Integration",
    description="AI-powered sustainability assistant with structured responses for frontend",
    version="2.2.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS settings - Updated to ensure frontend can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://spectacular-dusk-cc7b08.netlify.app",  # Jonas's frontend
        "http://localhost:3000",  # Local frontend development
        "http://localhost:3001",  # Alternative local port
        "*"  # Be careful with this in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "SustAInability Navigator - Frontend Integrated Version",
        "version": "2.2.0",
        "status": "healthy",
        "features": [
            "Structured Chat Responses",
            "User Profile Management", 
            "Chat History",
            "DBO Tool Integration", 
            "Xcelerator Marketplace Matching",
            "Persona Intelligence"
        ],
        "api_endpoints": {
            "chat": "/chat/",
            "save_user_info": "/save_user_info/",
            "get_user_info": "/get_user_info/",
            "get_chats": "/get_chats/",
            "dbo_scenarios": "/api/v1/dbo/scenarios",
            "health": "/health"
        },
        "frontend_integration": {
            "response_format": "Structured JSON with response, recommendations, and actions",
            "user_management": "Database-backed user profiles",
            "chat_history": "Persistent chat storage with retrieval"
        }
    }

@app.get("/health")
def health_check():
    """Enhanced health check with all services status"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "services": {
            "dbo_service": "operational",
            "langchain_service": "operational" if langchain_service.use_ai else "fallback_mode",
            "xcelerator_service": "operational",
            "database_service": "operational",  # You'll need to implement actual DB health check
            "scenarios_loaded": len(dbo_service.scenarios),
            "xcelerator_products": len(xcelerator_service.xcelerator_catalog)
        },
        "integration_status": {
            "dbo_scenarios": f"{len(dbo_service.scenarios)} scenarios loaded",
            "xcelerator_catalog": f"{len(xcelerator_service.xcelerator_catalog)} products available",
            "ai_model": "gpt-4" if langchain_service.use_ai else "fallback",
            "structured_responses": "enabled",
            "user_profiles": "enabled",
            "chat_persistence": "enabled"
        },
        "frontend_compatibility": {
            "version": "1.0",
            "structured_responses": True,
            "user_management": True,
            "chat_history": True
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
            }
        ],
        "supported_languages": ["en", "de", "es", "fr"],
        "features": {
            "dbo_scenarios": True,
            "xcelerator_marketplace": True,
            "carbon_calculator": False,  # Coming soon
            "roi_calculator": False,     # Coming soon
            "expert_chat": True
        }
    }

# Include routers - Note the main chat endpoints are at root level per Jonas's spec
app.include_router(chat_router, prefix="", tags=["Chat & User Management"])  # No prefix for main endpoints
app.include_router(dbo_router, prefix="/api/v1/dbo", tags=["DBO Scenarios"])
app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(integration_router, prefix="/api/v1/integration", tags=["Siemens Integration"])

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting SustAInability Navigator - Frontend Integrated Version")
    logger.info("=" * 70)
    logger.info(f"🌱 DBO Scenarios loaded: {len(dbo_service.scenarios)}")
    logger.info(f"🛒 Xcelerator products available: {len(xcelerator_service.xcelerator_catalog)}")
    logger.info(f"🤖 LangChain AI: {'Enabled with GPT-4' if langchain_service.use_ai else 'Fallback mode'}")
    logger.info(f"💬 Structured responses: Enabled")
    logger.info(f"👤 User management: Enabled")
    logger.info(f"📝 Chat history: Enabled")
    logger.info("=" * 70)
    logger.info("🚀 Ready for frontend integration!")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down SustAInability Navigator")
    # Clean up any open connections, save cache, etc.
    if hasattr(langchain_service, 'clean_memory'):
        langchain_service.clean_memory()

if __name__ == "__main__":
    import uvicorn
    
    # Run with auto-reload for development
    uvicorn.run(
        "main:app",  # Use string to enable auto-reload
        host="0.0.0.0", 
        port=8000,
        reload=True,  # Enable auto-reload
        log_level="info"
    )
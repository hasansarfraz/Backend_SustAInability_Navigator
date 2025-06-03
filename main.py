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

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SustAInability Navigator - Enhanced Siemens Integration",
    description="AI-powered sustainability assistant bridging DBO Tool outputs with Siemens Xcelerator Marketplace",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://spectacular-dusk-cc7b08.netlify.app", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "SustAInability Navigator - Enhanced Siemens Integration",
        "version": "2.1.0",
        "status": "healthy",
        "features": [
            "DBO Tool Integration", 
            "Xcelerator Marketplace Matching", 
            "User Proficiency Assessment",
            "LangChain AI", 
            "Enhanced DBO Scenarios", 
            "Persona Intelligence"
        ],
        "workflow": "DBO Tool Output → User Profile Assessment → Optimal Xcelerator Solutions",
        "integration_points": {
            "dbo_tool": "https://www.dbo.siemens.com/",
            "xcelerator_marketplace": "https://xcelerator.siemens.com/global/en/all-offerings.html",
            "frontend_ui": "https://spectacular-dusk-cc7b08.netlify.app"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "services": {
            "dbo_service": "operational",
            "langchain_service": "operational" if langchain_service.use_ai else "fallback_mode",
            "xcelerator_service": "operational",
            "scenarios_loaded": len(dbo_service.scenarios),
            "xcelerator_products": len(xcelerator_service.xcelerator_catalog)
        },
        "integration_status": {
            "dbo_scenarios": f"{len(dbo_service.scenarios)} example outputs loaded",
            "xcelerator_catalog": f"{len(xcelerator_service.xcelerator_catalog)} products available",
            "user_proficiency_assessment": "enabled",
            "ai_recommendations": "enabled" if langchain_service.use_ai else "fallback_mode"
        }
    }

@app.get("/api/v1/workflow/overview")
def get_workflow_overview():
    """Get overview of the complete DBO → Xcelerator workflow"""
    return {
        "workflow_description": "Intelligent bridge between Siemens DBO Tool and Xcelerator Marketplace",
        "process_steps": [
            {
                "step": 1,
                "name": "DBO Tool Analysis",
                "description": "SMEs use Siemens DBO Tool to analyze sustainability scenarios",
                "input": "Business requirements and constraints",
                "output": "Optimized scenario recommendations (JSON format)",
                "example_scenarios": list(dbo_service.scenarios.keys())
            },
            {
                "step": 2,
                "name": "User Proficiency Assessment", 
                "description": "Assess user capabilities and preferences",
                "input": "Sustainability proficiency, tech proficiency, communication style, compliance needs",
                "output": "Personalized implementation approach",
                "assessment_methods": ["Web UI settings", "Chat/voice bot interaction"]
            },
            {
                "step": 3,
                "name": "Xcelerator Matching",
                "description": "AI-powered matching to optimal Siemens Xcelerator solutions",
                "input": "DBO output + User profile",
                "output": "Ranked Xcelerator product recommendations with implementation guidance",
                "marketplace_url": "https://xcelerator.siemens.com/global/en/all-offerings.html"
            },
            {
                "step": 4,
                "name": "Implementation Planning",
                "description": "Generate implementation roadmap and next steps",
                "input": "Selected solutions + User profile",
                "output": "Detailed implementation plan with financing options",
                "support_options": ["Siemens consulting", "Training programs", "Financial services"]
            }
        ],
        "key_benefits": [
            "Intelligent product matching based on actual DBO outputs",
            "Proficiency-aware implementation guidance",
            "Complete Siemens ecosystem integration",
            "Financial modeling and ROI optimization",
            "Regulatory compliance alignment"
        ]
    }

# Include routers
app.include_router(chat_router, prefix="/api/v1/chat", tags=["Chat & AI"])
app.include_router(dbo_router, prefix="/api/v1/dbo", tags=["DBO Scenarios"])
app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(integration_router, prefix="/api/v1/integration", tags=["Siemens Integration"])

if __name__ == "__main__":
    import uvicorn
    
    # Log startup information
    logger.info("Starting SustAInability Navigator - Enhanced Siemens Integration")
    logger.info("=" * 70)
    logger.info(f"🌱 DBO Scenarios loaded: {len(dbo_service.scenarios)}")
    logger.info(f"🛒 Xcelerator products available: {len(xcelerator_service.xcelerator_catalog)}")
    logger.info(f"🤖 LangChain AI: {'Enabled' if langchain_service.use_ai else 'Fallback mode'}")
    logger.info(f"🔗 DBO Tool integration: Ready")
    logger.info(f"🛍️  Xcelerator marketplace integration: Ready")
    logger.info(f"👤 User proficiency assessment: Enabled")
    logger.info("=" * 70)
    logger.info("🚀 Ready for SME → DBO → Xcelerator workflow!")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        reload=False
    )
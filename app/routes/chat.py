from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid
import logging

from app.models.chat import ChatRequest, ChatResponse
from app.models.personas import PersonaType, PersonaConfig
from app.services.langchain_service import langchain_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Enhanced chat endpoint with LangChain and persona intelligence"""
    try:
        # Generate session ID if not provided
        session_id = request.session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Get AI response from LangChain
        ai_result = await langchain_service.generate_response(
            message=request.message,
            persona=request.persona,
            session_id=session_id
        )
        
        return ChatResponse(
            response=ai_result["response"],
            persona_context=request.persona,
            session_id=session_id,
            recommendations=ai_result.get("recommendations"),
            dbo_suggestions=ai_result.get("dbo_suggestions"),
            timestamp=datetime.now(),
            confidence_score=ai_result.get("confidence_score")
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

@router.get("/personas")
async def get_personas():
    """Get available personas and their configurations"""
    return {
        "personas": [
            {
                "id": persona.value,
                "name": config["name"],
                "role": config["role"],
                "industry": config["industry"],
                "company_size": config["company_size"],
                "priorities": config["priorities"]
            }
            for persona, config in PersonaConfig.PERSONAS.items()
        ]
    }
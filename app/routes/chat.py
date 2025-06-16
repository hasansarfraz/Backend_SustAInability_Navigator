# app/routes/chat.py - Complete implementation with all endpoints

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from typing import Dict, List, Optional
import uuid
import logging
from pydantic import BaseModel, Field

from app.models.personas import PersonaType, PersonaConfig
from app.services.rag_agent_service import rag_agent
from app.services.supabase_service import db_service
from app.services.auth_service import get_current_user  # We'll create this

router = APIRouter()
logger = logging.getLogger(__name__)

# Request/Response models
class ChatRequest(BaseModel):
    chat_ID: str = Field(..., description="Chat session ID")
    message: str = Field(..., description="User message")

class MarketplaceItem(BaseModel):
    id: str
    name: str
    category: str
    description: str
    url: Optional[str] = None
    relevance_score: Optional[float] = None

class UserAction(BaseModel):
    action_id: str
    action_type: str
    action_label: str
    action_data: Optional[Dict] = None

class ChatResponse(BaseModel):
    response: str = Field(..., description="Textual response to display to user")
    chat_ID: str = Field(..., description="Chat session ID")
    recommendations: Optional[List[MarketplaceItem]] = Field(default=None, description="Xcelerator Marketplace items")
    actions: Optional[List[UserAction]] = Field(default=None, description="Available user actions")

class ChatMessage(BaseModel):
    message_id: str
    user_message: str
    ai_response: Dict
    created_at: str
    message_index: int

class ChatHistoryResponse(BaseModel):
    chat_ID: str
    messages: List[ChatMessage]
    total_messages: int

# Main chat endpoint
@router.post("/chat/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint that processes user messages and returns structured responses.
    """
    try:
        # Get user ID from chat_ID
        user_id = await db_service.get_user_id_from_chat(request.chat_ID)
        
        # Retrieve user parameters
        user_params = await db_service.get_user_params(user_id)
        
        # Determine persona from user_params
        persona = user_params.get("persona", "general")
        
        # Process message with RAG agent
        ai_result = await rag_agent.process_message(
            message=request.message,
            persona=persona,
            session_id=request.chat_ID,
            user_params=user_params
        )
        
        # Parse and structure response
        structured_response = _parse_ai_response(ai_result)
        
        # Save to database
        await db_service.save_chat_message(
            chat_id=request.chat_ID,
            user_id=user_id,
            message=request.message,
            response=structured_response
        )
        
        return ChatResponse(
            response=structured_response["response"],
            chat_ID=request.chat_ID,
            recommendations=structured_response.get("recommendations"),
            actions=structured_response.get("actions")
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

# NEW ENDPOINT: Get chat history
@router.get("/get_chat_history/{chat_ID}", response_model=ChatHistoryResponse)
async def get_chat_history(chat_ID: str):
    """
    Retrieve complete chat history for a given chat ID.
    """
    try:
        # Get messages from database
        messages = await db_service.get_chat_messages(chat_ID)
        
        # If no messages found, return empty history instead of 404
        if not messages:
            return ChatHistoryResponse(
                chat_ID=chat_ID,
                messages=[],
                total_messages=0
            )
        
        # Format messages
        formatted_messages = []
        for msg in messages:
            formatted_messages.append(ChatMessage(
                message_id=str(msg.get("id", "")),
                user_message=msg.get("user_message", ""),
                ai_response=msg.get("ai_response", {}),
                created_at=msg.get("created_at", "").isoformat() if isinstance(msg.get("created_at"), datetime) else str(msg.get("created_at", "")),
                message_index=msg.get("message_index", 0)
            ))
        
        return ChatHistoryResponse(
            chat_ID=chat_ID,
            messages=formatted_messages,
            total_messages=len(formatted_messages)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving chat history: {e}")
        # Return empty history instead of error
        return ChatHistoryResponse(
            chat_ID=chat_ID,
            messages=[],
            total_messages=0
        )

# User management endpoints
class UserParams(BaseModel):
    """User parameters/settings from the frontend menu"""
    sustainability_proficiency: Optional[str] = None
    technological_proficiency: Optional[str] = None
    company_size: Optional[str] = None
    industry: Optional[str] = None
    communication_style: Optional[str] = None
    regulatory_importance: Optional[str] = None
    budget_priority: Optional[str] = None
    preferred_language: Optional[str] = "en"
    notification_preferences: Optional[Dict] = None
    persona: Optional[str] = "general"

@router.post("/save_user_info/")
async def save_user_info(user_params: UserParams, uid: str):
    """Save user parameters to database"""
    try:
        await db_service.save_user_params(uid, user_params.dict(exclude_none=True))
        return {"status": "success", "message": "User parameters saved successfully"}
    except Exception as e:
        logger.error(f"Error saving user params: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save user parameters: {str(e)}")

@router.get("/get_user_info/")
async def get_user_info(uid: str) -> UserParams:
    """Retrieve user parameters from database"""
    try:
        params = await db_service.get_user_params(uid)
        if not params:
            return UserParams()
        return UserParams(**params)
    except Exception as e:
        logger.error(f"Error retrieving user params: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user parameters: {str(e)}")

# Chat list endpoint
class ChatSummary(BaseModel):
    chat_ID: str
    chat_title: str
    chat_ts: str  # YYYY-MM-DD format

@router.get("/get_chats/")
async def get_chats(uid: str, ts_start: str) -> List[ChatSummary]:
    """Retrieve previous chats for the given user"""
    try:
        # Validate date format
        datetime.strptime(ts_start, "%Y-%m-%d")
        
        chats = await db_service.get_user_chats(uid, ts_start)
        
        chat_summaries = []
        for chat in chats:
            summary = ChatSummary(
                chat_ID=chat["chat_id"],
                chat_title=chat.get("title", "Untitled Chat"),
                chat_ts=chat["created_at"].strftime("%Y-%m-%d")
            )
            chat_summaries.append(summary)
        
        return chat_summaries
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        logger.error(f"Error retrieving chats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve chats: {str(e)}")

# Persona endpoint
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

# Helper functions
def _parse_ai_response(ai_result: Dict) -> Dict:
    """Parse AI response and structure it according to frontend requirements"""
    structured_response = {
        "response": ai_result.get("response", "I apologize, but I couldn't process your request properly."),
        "recommendations": None,
        "actions": None
    }
    
    # Extract Xcelerator Marketplace recommendations
    if ai_result.get("recommendations"):
        marketplace_items = []
        for rec in ai_result["recommendations"][:3]:
            item = MarketplaceItem(
                id=rec.get("product_id", rec.get("name", "").lower().replace(" ", "_")),
                name=rec.get("name", "Unknown Product"),
                category=rec.get("category", "General"),
                description=rec.get("description", ""),
                url=rec.get("url"),
                relevance_score=rec.get("relevance_score")
            )
            marketplace_items.append(item)
        
        if marketplace_items:
            structured_response["recommendations"] = marketplace_items
    
    # Extract suggested actions
    actions = []
    
    # Check for DBO scenario suggestions
    if ai_result.get("dbo_suggestions"):
        for scenario_id in ai_result["dbo_suggestions"]:
            action = UserAction(
                action_id=f"select_dbo_{scenario_id}",
                action_type="select_dbo_scenario",
                action_label=f"Explore {scenario_id.replace('_', ' ').title()} Scenario",
                action_data={"scenario_id": scenario_id}
            )
            actions.append(action)
    
    # Add any custom actions from AI
    if ai_result.get("actions"):
        for ai_action in ai_result["actions"]:
            if isinstance(ai_action, dict):
                action = UserAction(
                    action_id=ai_action.get("action_id", "custom_action"),
                    action_type=ai_action.get("action_type", "custom"),
                    action_label=ai_action.get("action_label", "Take Action"),
                    action_data=ai_action.get("action_data", {})
                )
                actions.append(action)
    
    if actions:
        structured_response["actions"] = actions[:3]
    
    return structured_response
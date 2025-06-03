from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    persona: Optional[str] = Field("general", description="User persona (zuri, amina, bjorn, arjun, general)")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")

class ChatResponse(BaseModel):
    response: str
    persona_context: str
    session_id: str
    recommendations: Optional[List[Dict]] = None
    dbo_suggestions: Optional[List[str]] = None
    timestamp: datetime
    confidence_score: Optional[float] = None

class ChatSession(BaseModel):
    session_id: str
    persona: str
    messages: List[Dict[str, Any]] = []
    context: Dict[str, Any] = {}
    created_at: datetime
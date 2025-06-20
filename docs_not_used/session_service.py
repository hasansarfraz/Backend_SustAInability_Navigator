# app/services/session_service.py
from typing import Dict, List, Optional
from app.models.chat import ChatSession
from datetime import datetime

class SessionService:
    def __init__(self):
        self.sessions: Dict[str, ChatSession] = {}
    
    def get_or_create_session(self, session_id: str, persona: str) -> ChatSession:
        """Get existing session or create new one"""
        if session_id not in self.sessions:
            self.sessions[session_id] = ChatSession(
                session_id=session_id,
                persona=persona,
                created_at=datetime.now()
            )
        return self.sessions[session_id]
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add message to session history"""
        if session_id in self.sessions:
            self.sessions[session_id].messages.append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
    
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for OpenAI API format"""
        if session_id not in self.sessions:
            return []
        
        history = []
        for msg in self.sessions[session_id].messages:
            history.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        return history
    
    def update_session_context(self, session_id: str, context: Dict):
        """Update session context"""
        if session_id in self.sessions:
            self.sessions[session_id].context.update(context)
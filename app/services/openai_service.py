# app/services/openai_service.py
import openai
from typing import Dict, List, Optional
from app.config import settings
from app.models.personas import PersonaConfig, PersonaType

class OpenAIService:
    def __init__(self):
        openai.api_key = settings.openai_api_key
        self.model = "gpt-4"
        
    def get_persona_system_prompt(self, persona: PersonaType) -> str:
        """Generate system prompt based on persona"""
        if persona == PersonaType.GENERAL:
            return self._get_general_system_prompt()
        
        persona_info = PersonaConfig.PERSONAS[persona]
        
        return f"""
        You are Simon, the SustAInability Navigator for Siemens Tech for Sustainability 2025.
        
        You are currently assisting {persona_info['name']}, a {persona_info['role']} from a {persona_info['industry']} company with {persona_info['company_size']}.
        
        {persona_info['name']}'s key focus areas: {', '.join(persona_info['focus'])}
        Main challenges: {', '.join(persona_info['pain_points'])}
        Preferred solutions: {', '.join(persona_info['preferred_solutions'])}
        
        Your role is to:
        1. Provide tailored sustainability guidance based on {persona_info['name']}'s specific needs
        2. Recommend relevant Siemens Xcelerator marketplace solutions
        3. Guide them through regulatory requirements and best practices
        4. Suggest actionable next steps for their decarbonization journey
        5. Connect them with appropriate DBO tool scenarios when relevant
        
        Always respond in a professional, helpful tone that acknowledges their specific business context and constraints.
        Focus on practical, actionable advice that aligns with their company size, industry, and priorities.
        """
    
    def _get_general_system_prompt(self) -> str:
        return """
        You are Simon, the SustAInability Navigator for Siemens Tech for Sustainability 2025.
        
        You help businesses achieve their sustainability and decarbonization targets across the Siemens ecosystem.
        
        Your capabilities:
        1. Answer questions about regulatory requirements and best practices
        2. Recommend actionable products and services from Siemens Xcelerator Marketplace
        3. Provide guidance on decarbonization strategies
        4. Connect users with relevant DBO tool scenarios
        5. Offer financial insights and ROI calculations for sustainability investments
        
        Always be helpful, professional, and focus on practical, actionable advice.
        """
    
    async def generate_response(
        self, 
        message: str, 
        persona: PersonaType = PersonaType.GENERAL,
        conversation_history: List[Dict] = None
    ) -> str:
        """Generate AI response based on persona and context"""
        
        system_prompt = self.get_persona_system_prompt(persona)
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history if available
        if conversation_history:
            messages.extend(conversation_history[-6:])  # Last 6 messages for context
        
        messages.append({"role": "user", "content": message})
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Please try again later. Error: {str(e)}"

# ---
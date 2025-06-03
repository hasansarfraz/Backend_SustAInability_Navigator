import os
import logging
from typing import List, Dict
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from app.config import settings
from app.models.personas import PersonaConfig, PersonaType

logger = logging.getLogger(__name__)

class EnhancedLangChainService:
    def __init__(self):
        self.openai_api_key = settings.openai_api_key
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        if self.openai_api_key and self.openai_api_key != "fallback-key":
            self.llm = ChatOpenAI(
                model="gpt-4",
                temperature=0.7,
                max_tokens=500,
                openai_api_key=self.openai_api_key
            )
            self.use_ai = True
        else:
            self.use_ai = False
            logger.warning("OpenAI API key not found, using fallback responses")
        
        self.tools = self._create_tools()
        
        if self.use_ai:
            self.agent = initialize_agent(
                tools=self.tools,
                llm=self.llm,
                agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                memory=self.memory,
                verbose=True,
                handle_parsing_errors=True
            )
    
    def _create_tools(self) -> List[Tool]:
        """Create LangChain tools for DBO scenarios and Siemens products"""
        
        def search_dbo_scenarios(query: str) -> str:
            """Search for relevant DBO scenarios based on query"""
            try:
                from app.services.dbo_service import dbo_service
                results = dbo_service.search_scenarios(query)
                
                if results:
                    response = f"Found {len(results)} relevant scenarios:\n"
                    for i, result in enumerate(results[:3], 1):
                        response += f"{i}. {result['title']} ({result['industry']}) - {result['payback_period']} years payback\n"
                    return response
                else:
                    return f"No scenarios found for '{query}'. Available categories: energy, water, waste, building, supply chain."
                    
            except Exception as e:
                return f"Error searching scenarios: {str(e)}"
        
        def get_dbo_details(scenario_id: str) -> str:
            """Get detailed information about a specific DBO scenario"""
            try:
                from app.services.dbo_service import dbo_service
                
                if scenario_id not in dbo_service.scenarios:
                    return f"Scenario '{scenario_id}' not found. Available: {list(dbo_service.scenarios.keys())}"
                
                scenario = dbo_service.scenarios[scenario_id]
                
                response = f"**{scenario['title']}** ({scenario['industry']})\n"
                response += f"Complexity: {scenario['complexity']}\n"
                response += f"Payback: {scenario['estimated_savings']['payback_period_years']} years\n\n"
                response += f"Description: {scenario['description']}\n\n"
                response += "Key Benefits:\n"
                for key, value in scenario['estimated_savings'].items():
                    if key != 'payback_period_years':
                        response += f"- {key.replace('_', ' ').title()}: {value}\n"
                
                return response
                
            except Exception as e:
                return f"Error retrieving scenario details: {str(e)}"
        
        def get_siemens_products(category: str = "all") -> str:
            """Get information about Siemens products for sustainability solutions"""
            products_info = {
                "building": "Desigo CC - Building management and automation platform",
                "iot": "MindSphere - Industrial IoT platform for predictive analytics", 
                "sustainability": "SiGREEN - Carbon footprint tracking and ESG reporting",
                "energy": "SICAM GridEdge - Smart grid solutions for renewable energy",
                "platform": "Siemens Xcelerator - Digital business platform and marketplace"
            }
            
            if category.lower() == "all":
                response = "Siemens Sustainability Solutions:\n"
                for cat, info in products_info.items():
                    response += f"• {info}\n"
                return response
            else:
                for cat, info in products_info.items():
                    if category.lower() in cat or category.lower() in info.lower():
                        return f"Relevant Siemens solution: {info}"
                return f"No specific product found for '{category}'. Available: building, iot, sustainability, energy, platform"
        
        return [
            Tool(
                name="search_dbo_scenarios",
                description="Search for DBO scenarios based on keywords like 'energy', 'water', 'building', 'waste', 'manufacturing'",
                func=search_dbo_scenarios
            ),
            Tool(
                name="get_dbo_details", 
                description="Get detailed information about a specific DBO scenario by ID",
                func=get_dbo_details
            ),
            Tool(
                name="get_siemens_products",
                description="Get information about Siemens products for sustainability solutions",
                func=get_siemens_products
            )
        ]
    
    def get_persona_system_prompt(self, persona: str) -> str:
        """Get persona-specific system prompt"""
        persona_config = PersonaConfig.PERSONAS.get(persona, PersonaConfig.PERSONAS[PersonaType.ZURI])
        
        return f"""You are Simon, the AI-powered SustAInability Navigator for Siemens Tech for Sustainability 2025.

You are currently assisting {persona_config['name']}, a {persona_config['role']} from a {persona_config['industry']} company with {persona_config['company_size']}.

Your role is to:
1. Provide expert sustainability guidance tailored to their specific business context
2. Recommend relevant Siemens solutions from the Xcelerator marketplace
3. Help them navigate DBO (Decision-Based Optimization) scenarios for their industry
4. Guide them through regulatory requirements and best practices
5. Support their decarbonization journey with actionable next steps

Key priorities for {persona_config['name']}: {', '.join(persona_config['priorities'])}

Always:
- Be professional, knowledgeable, and solution-focused
- Reference specific DBO scenarios when relevant using the search tools
- Recommend appropriate Siemens products and services
- Consider their industry context and company size in your recommendations
- Provide actionable, practical advice

Use the available tools to search for relevant scenarios and product information to give comprehensive, accurate responses."""
    
    async def generate_response(self, message: str, persona: str = "general", session_id: str = None) -> Dict:
        """Generate AI response with LangChain"""
        try:
            if not self.use_ai:
                return self._get_fallback_response(message, persona)
            
            # Set up persona-specific context
            system_prompt = self.get_persona_system_prompt(persona)
            
            # Create enhanced prompt with context
            enhanced_message = f"Context: {system_prompt}\n\nUser Query: {message}"
            
            # Generate response using agent
            response = await self.agent.arun(enhanced_message)
            
            # Extract recommendations and DBO suggestions
            recommendations = self._extract_recommendations(response)
            dbo_suggestions = self._extract_dbo_suggestions(response, message)
            
            return {
                "response": response,
                "recommendations": recommendations,
                "dbo_suggestions": dbo_suggestions,
                "confidence_score": 0.9
            }
            
        except Exception as e:
            logger.error(f"LangChain error: {e}")
            return self._get_fallback_response(message, persona)
    
    def _extract_recommendations(self, response: str) -> List[Dict]:
        """Extract product recommendations from response"""
        recommendations = []
        
        products = {
            "desigo": {"name": "Desigo CC", "category": "Building Management"},
            "mindsphere": {"name": "MindSphere", "category": "IoT Platform"},
            "sigreen": {"name": "SiGREEN", "category": "Sustainability Tracking"},
            "sicam": {"name": "SICAM GridEdge", "category": "Smart Grid"},
            "xcelerator": {"name": "Siemens Xcelerator", "category": "Digital Platform"}
        }
        
        response_lower = response.lower()
        for key, product in products.items():
            if key in response_lower:
                recommendations.append(product)
        
        return recommendations[:3]
    
    def _extract_dbo_suggestions(self, response: str, message: str) -> List[str]:
        """Extract DBO scenario suggestions"""
        suggestions = []
        
        message_lower = message.lower()
        scenario_mapping = {
            "energy": "energy_optimization",
            "water": "water_usage_reduction", 
            "building": "smart_building_retrofitting",
            "waste": "waste_management_optimization",
            "supply": "supply_chain_emission_transparency",
            "monitoring": "remote_energy_monitoring_for_smes"
        }
        
        for keyword, scenario_id in scenario_mapping.items():
            if keyword in message_lower:
                suggestions.append(scenario_id)
        
        return suggestions[:2]
    
    def _get_fallback_response(self, message: str, persona: str) -> Dict:
        """Fallback responses when AI is not available"""
        persona_config = PersonaConfig.PERSONAS.get(persona, PersonaConfig.PERSONAS[PersonaType.ZURI])
        
        fallback_responses = {
            "zuri": f"Hi {persona_config['name']}! As an enterprise sustainability leader, I recommend focusing on scalable solutions that support your global sustainability targets and regulatory compliance.",
            "amina": f"Hi {persona_config['name']}! For cost-effective sustainability improvements, I suggest starting with solutions that provide quick ROI like energy efficiency measures.",
            "bjorn": f"Hi {persona_config['name']}! Given your existing Siemens partnership, I recommend exploring how our latest sustainability solutions integrate with your current systems.",
            "arjun": f"Hi {persona_config['name']}! To build competitive advantage through sustainability, focus on measurable improvements you can showcase to stakeholders."
        }
        
        base_response = fallback_responses.get(persona, "Hi! I'm Simon, your SustAInability Navigator. I help businesses achieve their sustainability and decarbonization targets.")
        
        return {
            "response": f"{base_response} How can I assist you with your sustainability journey today?",
            "recommendations": [],
            "dbo_suggestions": [],
            "confidence_score": 0.7
        }

# Global instance
langchain_service = EnhancedLangChainService()
# app/tools/dbo_tool.py (Updated for FastAPI integration)
from langchain.tools import BaseTool
from typing import Dict, Any
from app.services.dbo_service import EnhancedDBOService

class DBOScenarioTool(BaseTool):
    name = "dbo_scenario_lookup"
    description = "Look up DBO (Decision-Based Optimization) scenarios for sustainability solutions. Input should be a scenario keyword like 'energy', 'water', 'building', 'waste', etc."
    
    def __init__(self):
        super().__init__()
        self.dbo_service = EnhancedDBOService()
    
    def _run(self, query: str) -> str:
        """Execute the DBO scenario lookup"""
        try:
            # Search for matching scenarios
            results = self.dbo_service.search_scenarios(query)
            
            if not results:
                return f"No DBO scenarios found for '{query}'. Available scenarios include energy optimization, water reduction, smart buildings, waste management, and supply chain optimization."
            
            # Format response with top 2-3 scenarios
            response_parts = [f"Found {len(results)} DBO scenarios for '{query}':\n"]
            
            for i, scenario in enumerate(results[:3], 1):
                response_parts.append(
                    f"{i}. **{scenario['title']}** ({scenario['industry']})\n"
                    f"   - Payback: {scenario['payback_period']} years\n"
                    f"   - Complexity: {scenario['complexity']}\n"
                    f"   - {scenario['description'][:100]}...\n"
                )
            
            response_parts.append("\nWould you like detailed information about any of these scenarios?")
            return "\n".join(response_parts)
            
        except Exception as e:
            return f"Error retrieving DBO scenarios: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of the tool"""
        return self._run(query)

# Updated function for backwards compatibility
def get_dbo_strategy():
    """Factory function to create DBO tool instance"""
    return DBOScenarioTool()

# ---
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import logging

from app.models.dbo import DBORequest, DBOResponse, ScenarioSummary
from app.services.dbo_service import dbo_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/scenario", response_model=DBOResponse)
async def get_dbo_scenario(request: DBORequest):
    """Get enhanced DBO scenario with detailed analysis"""
    try:
        scenario = dbo_service.get_enhanced_scenario(request.scenario, request.persona)
        
        return DBOResponse(
            scenario_id=request.scenario,
            title=scenario["title"],
            description=scenario["description"],
            industry=scenario["industry"],
            complexity=scenario["complexity"],
            implementation_steps=scenario["implementation_steps"],
            estimated_savings=scenario["estimated_savings"],
            financial_analysis=scenario["financial_analysis"],
            timeline=scenario["timeline"],
            siemens_products=scenario["siemens_products"],
            sustainability_metrics=scenario["sustainability_metrics"],
            risk_factors=scenario["risk_factors"],
            success_indicators=scenario["success_indicators"],
            persona_insights=scenario["persona_insights"],
            confidence_score=scenario["confidence_score"]
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"DBO scenario error: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving scenario: {str(e)}")

@router.get("/scenarios")
async def list_all_scenarios():
    """List all enhanced DBO scenarios"""
    try:
        scenarios = dbo_service.get_all_scenarios_summary()
        return {
            "scenarios": scenarios,
            "total_count": len(scenarios),
            "categories": list(set(s["industry"] for s in scenarios)),
            "complexity_levels": list(set(s["complexity"] for s in scenarios))
        }
    except Exception as e:
        logger.error(f"List scenarios error: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing scenarios: {str(e)}")

@router.get("/scenarios/search")
async def search_scenarios(
    q: str,
    persona: Optional[str] = None,
    industry: Optional[str] = None,
    complexity: Optional[str] = None
):
    """Advanced scenario search with filters"""
    try:
        # Get base search results
        results = []
        query_lower = q.lower()
        
        for scenario_id, scenario in dbo_service.scenarios.items():
            # Search in multiple fields
            searchable_text = (
                scenario['title'] + " " + 
                scenario['description'] + " " + 
                " ".join(scenario['implementation_steps']) + " " +
                scenario['industry']
            ).lower()
            
            # Apply filters
            if industry and industry.lower() not in scenario['industry'].lower():
                continue
                
            if complexity and complexity.lower() not in scenario['complexity'].lower():
                continue
            
            # Check query match
            if any(word in searchable_text for word in query_lower.split()):
                result = {
                    "id": scenario_id,
                    "title": scenario['title'],
                    "description": scenario['description'][:200] + "...",
                    "industry": scenario['industry'],
                    "complexity": scenario['complexity'],
                    "payback_period": scenario['estimated_savings']['payback_period_years'],
                    "key_benefits": list(scenario['estimated_savings'].keys())[:3]
                }
                
                # Add persona insight if requested
                if persona:
                    try:
                        enhanced_scenario = dbo_service.get_enhanced_scenario(scenario_id, persona)
                        result["persona_insight"] = enhanced_scenario["persona_insights"][:150] + "..."
                    except:
                        pass
                
                results.append(result)
        
        # Sort by relevance (payback period)
        results.sort(key=lambda x: x['payback_period'])
        
        return {
            "query": q,
            "filters": {"persona": persona, "industry": industry, "complexity": complexity},
            "results": results,
            "total_count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Search scenarios error: {e}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@router.get("/scenario/{scenario_id}")
async def get_scenario_summary(scenario_id: str):
    """Get quick scenario summary"""
    try:
        if scenario_id not in dbo_service.scenarios:
            raise HTTPException(status_code=404, detail="Scenario not found")
        
        scenario = dbo_service.scenarios[scenario_id]
        return {
            "id": scenario_id,
            "title": scenario["title"],
            "description": scenario["description"],
            "industry": scenario["industry"],
            "complexity": scenario["complexity"],
            "payback_period": f"{scenario['estimated_savings']['payback_period_years']} years",
            "key_savings": {
                key: value for key, value in scenario["estimated_savings"].items() 
                if key != "payback_period_years"
            },
            "investment_range": scenario["financial_analysis"]["investment_range"]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get scenario summary error: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving scenario summary: {str(e)}")

@router.get("/industries")
async def get_industries():
    """Get list of industries covered by DBO scenarios"""
    try:
        scenarios = dbo_service.get_all_scenarios_summary()
        industries = list(set(scenario["industry"] for scenario in scenarios))
        
        return {
            "industries": sorted(industries),
            "total_count": len(industries)
        }
    except Exception as e:
        logger.error(f"Get industries error: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving industries: {str(e)}")

@router.get("/complexity-levels")
async def get_complexity_levels():
    """Get available complexity levels for scenarios"""
    return {
        "complexity_levels": ["Low to Medium", "Medium", "High"],
        "descriptions": {
            "Low to Medium": "Basic implementations with standard technology",
            "Medium": "Moderate complexity with IoT and analytics integration",
            "High": "Advanced implementations with AI, digital twins, or blockchain"
        }
    }
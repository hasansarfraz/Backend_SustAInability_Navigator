# app/routes/integration.py - New Integration Routes

from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict
import logging

from app.models.user_profile import UserProfile, DBOToolOutput, XceleratorRecommendation
from app.services.xcelerator_service import xcelerator_service
from app.services.dbo_service import dbo_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/dbo-to-xcelerator", response_model=List[XceleratorRecommendation])
async def analyze_dbo_and_recommend_xcelerator(
    dbo_output: DBOToolOutput,
    user_profile: UserProfile
):
    """
    Main integration endpoint: Analyze DBO tool output and recommend optimal Xcelerator solutions
    """
    try:
        logger.info(f"Processing DBO analysis for scenario: {dbo_output.scenario_title}")
        
        # Generate Xcelerator recommendations based on DBO output and user profile
        recommendations = xcelerator_service.analyze_dbo_output_and_recommend(
            dbo_output=dbo_output,
            user_profile=user_profile
        )
        
        logger.info(f"Generated {len(recommendations)} Xcelerator recommendations")
        return recommendations
        
    except Exception as e:
        logger.error(f"DBO to Xcelerator analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/user-profile/assess")
async def assess_user_proficiency(user_profile: UserProfile):
    """
    Assess user proficiency and provide customized guidance
    """
    try:
        # Generate proficiency-based recommendations
        assessment = {
            "profile_summary": {
                "sustainability_level": user_profile.sustainability_proficiency.value,
                "technology_level": user_profile.technological_proficiency.value,
                "communication_preference": user_profile.communication_style.value,
                "compliance_priority": user_profile.regulatory_compliance_importance.value
            },
            "recommended_approach": _generate_approach_recommendation(user_profile),
            "suggested_products": _get_proficiency_based_products(user_profile),
            "implementation_guidance": _generate_implementation_guidance(user_profile),
            "support_requirements": _assess_support_needs(user_profile)
        }
        
        return assessment
        
    except Exception as e:
        logger.error(f"User proficiency assessment failed: {e}")
        raise HTTPException(status_code=500, detail=f"Assessment failed: {str(e)}")

@router.get("/xcelerator/products")
async def get_xcelerator_catalog(
    category: Optional[str] = None,
    complexity: Optional[str] = None
):
    """
    Get Siemens Xcelerator product catalog with filtering options
    """
    try:
        catalog = xcelerator_service.xcelerator_catalog
        
        # Apply filters if provided
        filtered_catalog = {}
        
        for product_id, product_info in catalog.items():
            include_product = True
            
            if category and category.lower() not in product_info["category"].lower():
                include_product = False
            
            if complexity and complexity.lower() != product_info.get("implementation_complexity", "").lower():
                include_product = False
            
            if include_product:
                filtered_catalog[product_id] = {
                    "name": product_info["name"],
                    "category": product_info["category"],
                    "description": product_info["description"],
                    "xcelerator_url": product_info.get("xcelerator_url"),
                    "implementation_complexity": product_info["implementation_complexity"],
                    "typical_timeline": product_info["typical_timeline"],
                    "sustainability_impact": product_info.get("sustainability_impact", {}),
                    "target_company_size": product_info.get("target_company_size", [])
                }
        
        return {
            "products": filtered_catalog,
            "total_count": len(filtered_catalog),
            "available_categories": list(set(p["category"] for p in catalog.values())),
            "complexity_levels": list(set(p["implementation_complexity"] for p in catalog.values()))
        }
        
    except Exception as e:
        logger.error(f"Xcelerator catalog retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Catalog retrieval failed: {str(e)}")

@router.post("/simulate-dbo-workflow")
async def simulate_complete_workflow(
    scenario_id: str,
    user_profile: UserProfile,
    persona: Optional[str] = "general"
):
    """
    Simulate complete workflow: DBO scenario → User proficiency → Xcelerator recommendations
    """
    try:
        # Step 1: Get enhanced DBO scenario
        dbo_scenario = dbo_service.get_enhanced_scenario(scenario_id, persona)
        
        # Step 2: Convert to DBO tool output format
        dbo_output = DBOToolOutput(
            scenario_title=dbo_scenario["title"],
            scenario_description=dbo_scenario["description"],
            recommended_actions=dbo_scenario["implementation_steps"],
            estimated_benefits=dbo_scenario["estimated_savings"],
            sme_context={
                "industry": dbo_scenario["industry"],
                "complexity": dbo_scenario["complexity"]
            },
            complexity_assessment=dbo_scenario["complexity"]
        )
        
        # Step 3: Generate Xcelerator recommendations
        xcelerator_recommendations = xcelerator_service.analyze_dbo_output_and_recommend(
            dbo_output=dbo_output,
            user_profile=user_profile
        )
        
        # Step 4: Compile complete workflow response
        workflow_result = {
            "dbo_analysis": {
                "scenario_id": scenario_id,
                "scenario_title": dbo_scenario["title"],
                "industry": dbo_scenario["industry"],
                "complexity": dbo_scenario["complexity"],
                "estimated_savings": dbo_scenario["estimated_savings"],
                "persona_insights": dbo_scenario["persona_insights"]
            },
            "user_profile_assessment": {
                "sustainability_proficiency": user_profile.sustainability_proficiency.value,
                "technological_proficiency": user_profile.technological_proficiency.value,
                "communication_style": user_profile.communication_style.value,
                "compliance_importance": user_profile.regulatory_compliance_importance.value
            },
            "xcelerator_recommendations": xcelerator_recommendations,
            "implementation_roadmap": _generate_implementation_roadmap(
                dbo_scenario, user_profile, xcelerator_recommendations
            ),
            "next_steps": _generate_next_steps(user_profile, xcelerator_recommendations)
        }
        
        return workflow_result
        
    except Exception as e:
        logger.error(f"Complete workflow simulation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Workflow simulation failed: {str(e)}")

def _generate_approach_recommendation(user_profile: UserProfile) -> Dict:
    """Generate recommended approach based on user profile"""
    
    approach = {
        "implementation_strategy": "guided" if user_profile.sustainability_proficiency == "beginner" else "collaborative",
        "support_level": "high" if user_profile.technological_proficiency == "beginner" else "moderate",
        "communication_approach": user_profile.communication_style.value,
        "compliance_focus": user_profile.regulatory_compliance_importance.value
    }
    
    return approach

def _get_proficiency_based_products(user_profile: UserProfile) -> List[str]:
    """Get product recommendations based on proficiency"""
    
    proficiency_mapping = xcelerator_service.proficiency_matrix["sustainability_proficiency_mapping"]
    return proficiency_mapping[user_profile.sustainability_proficiency]["recommended_products"]

def _generate_implementation_guidance(user_profile: UserProfile) -> Dict:
    """Generate implementation guidance based on profile"""
    
    guidance = {
        "timeline_recommendation": "6-12 months" if user_profile.technological_proficiency.value in ["beginner", "intermediate"] else "3-6 months",
        "training_requirements": "extensive" if user_profile.sustainability_proficiency == "beginner" else "moderate",
        "support_requirements": "high" if user_profile.technological_proficiency == "beginner" else "standard",
        "change_management": "critical" if user_profile.sustainability_proficiency == "beginner" else "important"
    }
    
    return guidance

def _assess_support_needs(user_profile: UserProfile) -> List[str]:
    """Assess specific support needs based on profile"""
    
    support_needs = []
    
    if user_profile.sustainability_proficiency == "beginner":
        support_needs.extend(["Sustainability strategy consulting", "Training programs", "Change management"])
    
    if user_profile.technological_proficiency == "beginner":
        support_needs.extend(["Implementation services", "Technical training", "Ongoing support"])
    
    if user_profile.regulatory_compliance_importance.value in ["high", "critical"]:
        support_needs.extend(["Compliance consulting", "Regulatory guidance", "Audit support"])
    
    return support_needs

def _generate_implementation_roadmap(
    dbo_scenario: Dict, 
    user_profile: UserProfile, 
    recommendations: List[XceleratorRecommendation]
) -> Dict:
    """Generate implementation roadmap"""
    
    roadmap = {
        "phase_1_assessment": {
            "duration": "2-4 weeks",
            "activities": ["Detailed requirements analysis", "Site assessment", "Stakeholder alignment"],
            "deliverables": ["Implementation plan", "Resource requirements", "Timeline"]
        },
        "phase_2_preparation": {
            "duration": "4-8 weeks",
            "activities": ["Team training", "Infrastructure preparation", "Vendor coordination"],
            "deliverables": ["Trained team", "Ready infrastructure", "Implementation contracts"]
        },
        "phase_3_implementation": {
            "duration": "8-16 weeks",
            "activities": ["System deployment", "Integration testing", "User training"],
            "deliverables": ["Operational system", "Trained users", "Performance baseline"]
        },
        "phase_4_optimization": {
            "duration": "4-8 weeks",
            "activities": ["Performance tuning", "Process optimization", "Success measurement"],
            "deliverables": ["Optimized performance", "Measured benefits", "Continuous improvement plan"]
        }
    }
    
    return roadmap

def _generate_next_steps(user_profile: UserProfile, recommendations: List[XceleratorRecommendation]) -> List[str]:
    """Generate immediate next steps"""
    
    next_steps = [
        "Review recommended Xcelerator solutions",
        "Schedule consultation with Siemens experts",
        "Assess budget and timeline requirements"
    ]
    
    if user_profile.sustainability_proficiency == "beginner":
        next_steps.append("Attend sustainability strategy workshop")
    
    if user_profile.technological_proficiency == "beginner":
        next_steps.append("Schedule technical readiness assessment")
    
    if user_profile.regulatory_compliance_importance.value in ["high", "critical"]:
        next_steps.append("Review compliance requirements with regulatory experts")
    
    next_steps.extend([
        "Contact Siemens Financial Services for financing options",
        "Plan pilot implementation for highest-priority solution"
    ])
    
    return next_steps
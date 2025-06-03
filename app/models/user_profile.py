# app/models/user_profile.py - User Proficiency Assessment Models

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum

class ProficiencyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class CommunicationStyle(str, Enum):
    TECHNICAL = "technical"
    BUSINESS_FOCUSED = "business_focused"
    SIMPLE_EXPLANATIONS = "simple_explanations"
    COMPREHENSIVE = "comprehensive"

class ComplianceImportance(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class UserProfile(BaseModel):
    """User proficiency and preferences assessment"""
    
    # Core proficiencies
    sustainability_proficiency: ProficiencyLevel = Field(..., description="User's sustainability knowledge level")
    technological_proficiency: ProficiencyLevel = Field(..., description="User's technology adoption capability")
    
    # Communication preferences
    communication_style: CommunicationStyle = Field(..., description="Preferred communication approach")
    
    # Business context
    regulatory_compliance_importance: ComplianceImportance = Field(..., description="Importance of regulatory compliance")
    
    # Optional company context
    company_size: Optional[str] = Field(None, description="Company size category")
    industry_sector: Optional[str] = Field(None, description="Primary industry sector")
    current_sustainability_initiatives: Optional[bool] = Field(None, description="Existing sustainability programs")
    
    # Preferences
    budget_priority: Optional[str] = Field(None, description="Budget constraint level (low/medium/high)")
    implementation_timeline: Optional[str] = Field(None, description="Preferred implementation speed")

class DBOToolOutput(BaseModel):
    """Model representing output from Siemens DBO Tool"""
    
    # DBO Tool identification
    dbo_source: str = Field(default="siemens_dbo_tool", description="Source: Siemens DBO Tool")
    analysis_date: Optional[str] = Field(None, description="When DBO analysis was performed")
    
    # Scenario details (from your JSON examples)
    scenario_title: str = Field(..., description="DBO scenario name")
    scenario_description: str = Field(..., description="Detailed scenario description")
    recommended_actions: List[str] = Field(..., description="DBO recommended implementation steps")
    estimated_benefits: Dict[str, Any] = Field(..., description="Expected savings and benefits")
    
    # SME context
    sme_context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="SME-specific context from DBO")
    urgency_level: Optional[str] = Field(None, description="Implementation urgency from DBO")
    complexity_assessment: Optional[str] = Field(None, description="DBO complexity evaluation")

class XceleratorRecommendation(BaseModel):
    """Enhanced Siemens Xcelerator product recommendation"""
    
    # Product details
    product_name: str
    product_category: str
    xcelerator_url: Optional[str] = None
    product_id: Optional[str] = None
    
    # Recommendation context
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="How well this matches the DBO output")
    implementation_complexity: str = Field(..., description="Implementation complexity level")
    estimated_timeline: str = Field(..., description="Expected implementation time")
    
    # Financial modeling
    estimated_investment: str = Field(..., description="Investment requirement range")
    expected_roi_timeline: str = Field(..., description="Expected ROI achievement timeline")
    financing_options: List[str] = Field(default_factory=list, description="Available financing through Siemens")
    
    # User proficiency alignment
    proficiency_match: Dict[str, str] = Field(default_factory=dict, description="How this aligns with user proficiencies")
    implementation_support: List[str] = Field(default_factory=list, description="Available implementation support")
    
    # Integration benefits
    ecosystem_benefits: List[str] = Field(default_factory=list, description="Benefits of Siemens ecosystem integration")

# ---
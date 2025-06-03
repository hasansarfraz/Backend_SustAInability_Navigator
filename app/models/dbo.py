from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class DBORequest(BaseModel):
    scenario: str = Field(..., description="Scenario ID")
    persona: Optional[str] = Field("general", description="User persona")
    detailed: Optional[bool] = Field(True, description="Include detailed analysis")

class DBOResponse(BaseModel):
    scenario_id: str
    title: str
    description: str
    industry: str
    complexity: str
    implementation_steps: List[str]
    estimated_savings: Dict[str, Any]
    financial_analysis: Dict[str, Any]
    timeline: Dict[str, str]
    siemens_products: List[Dict[str, str]]
    sustainability_metrics: List[Dict[str, Any]]
    risk_factors: List[str]
    success_indicators: List[str]
    persona_insights: str
    confidence_score: float

class ScenarioSummary(BaseModel):
    id: str
    title: str
    description: str
    industry: str
    company_size: str
    complexity: str
    payback_period: str
    key_benefits: List[str]
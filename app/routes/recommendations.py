# app/routes/recommendations.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

router = APIRouter()

class RecommendationRequest(BaseModel):
    query: str
    persona: Optional[str] = "general"
    industry: Optional[str] = None
    company_size: Optional[str] = None

class Product(BaseModel):
    name: str
    category: str
    description: str
    relevance_score: float
    price_range: Optional[str] = None
    implementation_time: Optional[str] = None
    use_cases: List[str]

class RecommendationResponse(BaseModel):
    recommendations: List[Product]
    total_count: int
    query_context: str
    persona_focus: Optional[str] = None

class SiemensRecommendationService:
    def __init__(self):
        self.products = self._load_siemens_products()
    
    def _load_siemens_products(self) -> Dict:
        """Load Siemens product catalog"""
        return {
            "sigreen": {
                "name": "SiGREEN",
                "category": "Sustainability Tracking",
                "description": "Carbon footprint tracking and sustainability reporting platform",
                "price_range": "Enterprise pricing available",
                "implementation_time": "2-4 weeks",
                "use_cases": ["Carbon tracking", "ESG reporting", "Sustainability analytics"],
                "keywords": ["carbon", "sustainability", "reporting", "esg", "tracking"]
            },
            "desigo_cc": {
                "name": "Desigo CC",
                "category": "Building Management",
                "description": "Integrated building management and automation platform",
                "price_range": "$10,000 - $100,000+",
                "implementation_time": "4-12 weeks",
                "use_cases": ["Building automation", "Energy efficiency", "HVAC control"],
                "keywords": ["building", "hvac", "automation", "energy", "efficiency"]
            },
            "building_x": {
                "name": "Building X",
                "category": "Digital Building Platform",
                "description": "Cloud-based building performance optimization and analytics",
                "price_range": "Subscription-based",
                "implementation_time": "2-6 weeks", 
                "use_cases": ["Building analytics", "Performance optimization", "Predictive maintenance"],
                "keywords": ["analytics", "optimization", "cloud", "performance", "digital"]
            },
            "mindsphere": {
                "name": "MindSphere",
                "category": "IoT Platform",
                "description": "Industrial IoT operating system for digital transformation",
                "price_range": "Usage-based pricing",
                "implementation_time": "6-16 weeks",
                "use_cases": ["Industrial IoT", "Predictive analytics", "Asset optimization"],
                "keywords": ["iot", "industrial", "analytics", "predictive", "manufacturing"]
            },
            "sicam_gridedge": {
                "name": "SICAM GridEdge", 
                "category": "Grid Integration",
                "description": "Smart grid edge device for renewable energy integration",
                "price_range": "$5,000 - $25,000",
                "implementation_time": "3-8 weeks",
                "use_cases": ["Renewable integration", "Grid stability", "Energy storage"],
                "keywords": ["solar", "renewable", "grid", "storage", "integration"]
            },
            "simatic_pcs7": {
                "name": "Simatic PCS 7",
                "category": "Process Control",
                "description": "Distributed control system for industrial processes",
                "price_range": "$50,000 - $500,000+",
                "implementation_time": "12-32 weeks",
                "use_cases": ["Process automation", "Industrial control", "Manufacturing optimization"],
                "keywords": ["process", "control", "automation", "manufacturing", "industrial"]
            }
        }
    
    def get_recommendations(
        self, 
        query: str, 
        persona: str = "general",
        limit: int = 5
    ) -> RecommendationResponse:
        """Get product recommendations based on query and persona"""
        
        query_lower = query.lower()
        scored_products = []
        
        # Score products based on keyword matching
        for product_id, product_data in self.products.items():
            score = 0.0
            
            # Keyword matching
            for keyword in product_data["keywords"]:
                if keyword in query_lower:
                    score += 1.0
            
            # Boost score based on persona preferences
            persona_boost = self._get_persona_boost(product_id, persona)
            score += persona_boost
            
            if score > 0:
                product = Product(
                    name=product_data["name"],
                    category=product_data["category"],
                    description=product_data["description"],
                    relevance_score=score,
                    price_range=product_data["price_range"],
                    implementation_time=product_data["implementation_time"],
                    use_cases=product_data["use_cases"]
                )
                scored_products.append(product)
        
        # Sort by relevance score and limit results
        scored_products.sort(key=lambda x: x.relevance_score, reverse=True)
        recommendations = scored_products[:limit]
        
        return RecommendationResponse(
            recommendations=recommendations,
            total_count=len(scored_products),
            query_context=query,
            persona_focus=self._get_persona_focus(persona)
        )
    
    def _get_persona_boost(self, product_id: str, persona: str) -> float:
        """Add persona-specific boost to product scores"""
        persona_preferences = {
            "zuri": {
                "sigreen": 2.0,  # ESG reporting important for large corps
                "building_x": 1.5,  # Cloud solutions for enterprise scale
                "mindsphere": 1.5   # Enterprise IoT platform
            },
            "amina": {
                "desigo_cc": 2.0,  # Cost-effective building efficiency
                "sicam_gridedge": 1.5,  # Solar with clear ROI
                "sigreen": 0.5   # Lower priority for cost-conscious
            },
            "bjorn": {
                "desigo_cc": 2.0,  # Existing Siemens customer
                "simatic_pcs7": 2.0,  # Industrial Siemens solutions
                "building_x": 1.5   # Familiar Siemens ecosystem
            },
            "arjun": {
                "sigreen": 2.0,  # Sustainability metrics crucial
                "building_x": 1.5,  # Performance tracking
                "mindsphere": 1.0   # Analytics for insights
            }
        }
        
        return persona_preferences.get(persona, {}).get(product_id, 0.0)
    
    def _get_persona_focus(self, persona: str) -> str:
        """Get persona-specific focus description"""
        focus_areas = {
            "zuri": "Enterprise-scale solutions with strong ESG reporting capabilities",
            "amina": "Cost-effective solutions with clear ROI and immediate benefits",
            "bjorn": "Siemens ecosystem integration with proven reliability",
            "arjun": "Sustainability metrics and competitive advantage tools"
        }
        return focus_areas.get(persona, "Comprehensive sustainability solutions")

# Initialize service
recommendation_service = SiemensRecommendationService()

@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """Get Siemens product recommendations based on query and persona"""
    return recommendation_service.get_recommendations(
        query=request.query,
        persona=request.persona,
        limit=5
    )

@router.get("/products")
async def list_products():
    """List all available Siemens products"""
    products = []
    for product_id, product_data in recommendation_service.products.items():
        products.append({
            "id": product_id,
            "name": product_data["name"],
            "category": product_data["category"],
            "description": product_data["description"],
            "price_range": product_data["price_range"]
        })
    return {"products": products}

@router.get("/categories")
async def get_categories():
    """Get product categories"""
    categories = set()
    for product_data in recommendation_service.products.values():
        categories.add(product_data["category"])
    
    return {"categories": list(categories)}

# ---
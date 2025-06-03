import json
import os
from typing import Dict, List, Optional
import logging
from app.models.personas import PersonaType, PersonaConfig

logger = logging.getLogger(__name__)

class EnhancedDBOService:
    def __init__(self):
        self.scenarios = self._load_and_enhance_scenarios()
        self.persona_configs = PersonaConfig.PERSONAS
        
    def _load_and_enhance_scenarios(self) -> Dict:
        """Load and enhance DBO scenarios with detailed analysis"""
        
        scenarios_file = "dbo_scenarios.json"
        base_scenarios = []
        
        if os.path.exists(scenarios_file):
            with open(scenarios_file, 'r') as f:
                base_scenarios = json.load(f)
        else:
            logger.warning(f"Scenarios file {scenarios_file} not found")
            return {}
        
        enhanced_scenarios = {}
        
        for scenario in base_scenarios:
            scenario_id = scenario["scenario"].lower().replace(" ", "_").replace("-", "_")
            
            enhanced_scenarios[scenario_id] = {
                "title": scenario["scenario"],
                "description": scenario["description"],
                "industry": self._classify_industry(scenario["description"]),
                "company_size": self._determine_company_size(scenario["description"]),
                "complexity": self._assess_complexity(scenario["recommendations"]),
                "implementation_steps": scenario["recommendations"],
                "estimated_savings": scenario["estimated_savings"],
                "financial_analysis": self._create_financial_analysis(scenario["estimated_savings"]),
                "timeline": self._create_implementation_timeline(scenario["estimated_savings"]["payback_period_years"]),
                "siemens_products": self._map_siemens_products(scenario["recommendations"]),
                "sustainability_metrics": self._extract_sustainability_metrics(scenario["estimated_savings"]),
                "risk_factors": self._identify_risks(scenario),
                "success_indicators": self._define_success_kpis(scenario),
                "market_context": self._add_market_context(scenario),
                "regulatory_compliance": self._assess_regulatory_impact(scenario)
            }
            
        logger.info(f"Loaded and enhanced {len(enhanced_scenarios)} scenarios")
        return enhanced_scenarios
    
    def _classify_industry(self, description: str) -> str:
        """AI-powered industry classification"""
        description_lower = description.lower()
        
        industry_mapping = {
            "Manufacturing": ["manufacturing", "facility", "production", "factory", "plant"],
            "Food & Beverage": ["beverage", "food", "restaurant", "kitchen", "processing"],
            "Logistics & Transportation": ["logistics", "fleet", "transport", "shipping", "supply chain"],
            "Government & Public Sector": ["municipal", "government", "public", "city", "office building"],
            "Waste Management": ["recycler", "waste", "sorting", "recycling", "circular"],
            "Retail": ["retail", "smes", "small business", "store", "commercial"],
            "Energy & Utilities": ["energy", "grid", "utilities", "power", "renewable"]
        }
        
        for industry, keywords in industry_mapping.items():
            if any(keyword in description_lower for keyword in keywords):
                return industry
        
        return "General Industry"
    
    def _determine_company_size(self, description: str) -> str:
        """Determine company size from description"""
        description_lower = description.lower()
        
        if "mid-sized" in description_lower:
            return "Medium (50-500 employees)"
        elif "sme" in description_lower or "cluster" in description_lower:
            return "Small (10-50 employees)"
        elif "municipal" in description_lower:
            return "Government/Public Sector"
        else:
            return "Small to Medium (10-500 employees)"
    
    def _assess_complexity(self, recommendations: List[str]) -> str:
        """Assess implementation complexity using AI analysis"""
        rec_text = " ".join(recommendations).lower()
        
        complexity_indicators = {
            "high": ["digital twin", "blockchain", "machine vision", "ai-based"],
            "medium": ["iot", "smart", "analytics", "automation", "predictive"],
            "low": ["led", "insulation", "training", "monitoring", "upgrade"]
        }
        
        high_score = sum(2 for indicator in complexity_indicators["high"] if indicator in rec_text)
        medium_score = sum(1 for indicator in complexity_indicators["medium"] if indicator in rec_text)
        
        total_score = high_score + medium_score
        
        if total_score >= 4:
            return "High"
        elif total_score >= 2:
            return "Medium"
        else:
            return "Low to Medium"
    
    def _create_financial_analysis(self, savings: Dict) -> Dict:
        """Create detailed financial analysis"""
        payback_years = savings.get("payback_period_years", 3)
        
        if payback_years <= 2:
            investment_range = "$25,000 - $150,000"
            annual_savings = "$20,000 - $75,000"
            risk_level = "Low"
            irr = "40-55%"
        elif payback_years <= 3:
            investment_range = "$50,000 - $300,000"
            annual_savings = "$25,000 - $100,000"
            risk_level = "Low to Medium"
            irr = "25-40%"
        else:
            investment_range = "$100,000 - $500,000"
            annual_savings = "$30,000 - $125,000"
            risk_level = "Medium"
            irr = "15-30%"
        
        return {
            "investment_range": investment_range,
            "annual_savings": annual_savings,
            "payback_period": f"{payback_years} years",
            "internal_rate_return": irr,
            "risk_level": risk_level,
            "financing_options": ["Siemens Financial Services", "Green bonds", "Equipment leasing"],
            "tax_incentives": ["Federal tax credits", "Local rebates", "Depreciation benefits"]
        }
    
    def _create_implementation_timeline(self, payback_years: float) -> Dict:
        """Create detailed implementation timeline"""
        if payback_years <= 2:
            return {
                "planning_phase": "3-4 weeks",
                "procurement": "2-3 weeks", 
                "installation": "4-8 weeks",
                "testing": "1-2 weeks",
                "optimization": "2-4 weeks",
                "total_duration": "3-5 months"
            }
        elif payback_years <= 3:
            return {
                "planning_phase": "4-6 weeks",
                "procurement": "4-6 weeks",
                "installation": "6-12 weeks", 
                "testing": "2-4 weeks",
                "optimization": "4-6 weeks",
                "total_duration": "5-8 months"
            }
        else:
            return {
                "planning_phase": "6-10 weeks",
                "procurement": "8-12 weeks",
                "installation": "12-20 weeks",
                "testing": "4-6 weeks", 
                "optimization": "6-10 weeks",
                "total_duration": "8-12 months"
            }
    
    def _map_siemens_products(self, recommendations: List[str]) -> List[Dict]:
        """Map to specific Siemens products with detailed information"""
        rec_text = " ".join(recommendations).lower()
        
        product_catalog = {
            "building_automation": {
                "name": "Desigo CC",
                "category": "Building Management Systems",
                "description": "Integrated building management and automation platform for optimal building performance",
                "key_features": ["Energy optimization", "Predictive maintenance", "Occupant comfort"],
                "typical_savings": "15-30%"
            },
            "iot_platform": {
                "name": "MindSphere",
                "category": "Industrial IoT Platform",
                "description": "Cloud-based IoT operating system for industrial digital transformation",
                "key_features": ["Data analytics", "Predictive insights", "Asset optimization"],
                "typical_savings": "10-25%"
            },
            "sustainability_tracking": {
                "name": "SiGREEN",
                "category": "Sustainability & Carbon Management",
                "description": "Comprehensive platform for carbon footprint tracking and ESG reporting",
                "key_features": ["Carbon accounting", "ESG reporting", "Compliance tracking"],
                "typical_savings": "5-15% through visibility"
            },
            "energy_management": {
                "name": "SICAM GridEdge",
                "category": "Smart Grid & Energy Management",
                "description": "Smart grid edge device for renewable energy integration and grid optimization",
                "key_features": ["Grid integration", "Energy storage management", "Demand response"],
                "typical_savings": "20-40%"
            }
        }
        
        mapped_products = []
        
        if any(word in rec_text for word in ["building", "hvac", "automation"]):
            mapped_products.append(product_catalog["building_automation"])
        
        if any(word in rec_text for word in ["iot", "sensors", "monitoring", "smart"]):
            mapped_products.append(product_catalog["iot_platform"])
        
        if any(word in rec_text for word in ["carbon", "sustainability", "emissions"]):
            mapped_products.append(product_catalog["sustainability_tracking"])
        
        if any(word in rec_text for word in ["energy", "grid", "renewable", "smart meter"]):
            mapped_products.append(product_catalog["energy_management"])
        
        # Always include Xcelerator as umbrella platform
        mapped_products.append({
            "name": "Siemens Xcelerator",
            "category": "Digital Business Platform",
            "description": "Comprehensive digital business platform and marketplace",
            "key_features": ["Digital marketplace", "Solution integration", "Collaboration tools"],
            "typical_savings": "Platform enables 10-30% efficiency gains"
        })
        
        return mapped_products
    
    def _extract_sustainability_metrics(self, savings: Dict) -> List[Dict]:
        """Extract detailed sustainability metrics"""
        metrics = []
        
        for key, value in savings.items():
            if key != "payback_period_years":
                metric_name = key.replace("_", " ").title()
                metrics.append({
                    "metric": metric_name,
                    "improvement": value,
                    "category": "Environmental Impact",
                    "measurement_type": "Percentage Improvement",
                    "reporting_standard": "ISO 14001",
                    "monitoring_frequency": "Monthly"
                })
        
        return metrics
    
    def _identify_risks(self, scenario: Dict) -> List[str]:
        """Identify comprehensive risk factors"""
        risks = []
        description = scenario["description"].lower()
        payback = scenario["estimated_savings"]["payback_period_years"]
        
        # Financial risks
        if payback > 3:
            risks.append("Extended payback period increases financial risk")
        
        # Operational risks
        if "manufacturing" in description:
            risks.append("Production downtime during implementation")
        
        # Technology risks
        risks.extend([
            "Technology standards evolution may impact compatibility",
            "Integration complexity with existing systems"
        ])
        
        return risks[:5]
    
    def _define_success_kpis(self, scenario: Dict) -> List[str]:
        """Define comprehensive success indicators"""
        indicators = []
        savings = scenario["estimated_savings"]
        payback = savings["payback_period_years"]
        
        indicators.append(f"Achieve positive ROI within {payback} years")
        
        for metric, value in savings.items():
            if metric != "payback_period_years":
                metric_name = metric.replace("_", " ").title()
                indicators.append(f"{metric_name}: Achieve {value} improvement")
        
        indicators.extend([
            "Project completion within budget and timeline",
            "System uptime >99% after stabilization",
            "Staff training completion rate >95%"
        ])
        
        return indicators[:8]
    
    def _add_market_context(self, scenario: Dict) -> Dict:
        """Add market context and trends"""
        return {
            "market_trends": ["Digital transformation", "Sustainability focus", "Regulatory compliance"],
            "competitive_advantage": "Innovation in sustainability practices"
        }
    
    def _assess_regulatory_impact(self, scenario: Dict) -> Dict:
        """Assess regulatory compliance and impact"""
        return {
            "current_regulations": ["ISO 14001", "ISO 50001", "GHG Protocol"],
            "compliance_benefits": ["Proactive compliance reduces risk", "ESG rating improvement"]
        }
    
    def get_enhanced_scenario(self, scenario_id: str, persona: str = "general") -> Dict:
        """Get fully enhanced scenario with persona-specific insights"""
        if scenario_id not in self.scenarios:
            raise ValueError(f"Scenario '{scenario_id}' not found")
        
        scenario = self.scenarios[scenario_id].copy()
        
        # Add persona-specific analysis
        scenario["persona_insights"] = self._get_persona_insights(scenario_id, persona, scenario)
        scenario["persona_recommendations"] = self._get_persona_recommendations(persona, scenario)
        scenario["confidence_score"] = self._calculate_confidence_score(scenario, persona)
        
        return scenario
    
    def _get_persona_insights(self, scenario_id: str, persona: str, scenario: Dict) -> str:
        """Generate detailed persona-specific insights"""
        
        persona_insights = {
            "zuri": f"For enterprise implementation, this {scenario['title'].lower()} solution can be scaled across multiple facilities with strong ESG reporting benefits.",
            "amina": f"Focus on immediate cost savings with {scenario['estimated_savings']['payback_period_years']}-year payback, perfect for cost-conscious operations.",
            "bjorn": f"This solution leverages existing Siemens infrastructure and integrates well with current systems for reliable performance.",
            "arjun": f"Provides clear sustainability metrics for competitive advantage with measurable environmental impact."
        }
        
        return persona_insights.get(persona, "This solution offers strong sustainability and financial benefits for your organization.")
    
    def _get_persona_recommendations(self, persona: str, scenario: Dict) -> List[str]:
        """Get persona-specific implementation recommendations"""
        base_recs = scenario["implementation_steps"]
        
        persona_additions = {
            "zuri": ["Develop enterprise rollout strategy", "Integrate with ESG reporting"],
            "amina": ["Prioritize highest-ROI components", "Secure financing options"],
            "bjorn": ["Leverage existing Siemens contracts", "Plan system integration"],
            "arjun": ["Establish sustainability metrics", "Create communication strategy"]
        }
        
        return base_recs + persona_additions.get(persona, [])
    
    def _calculate_confidence_score(self, scenario: Dict, persona: str) -> float:
        """Calculate confidence score for scenario recommendation"""
        score = 0.8  # Base confidence
        
        if len(scenario["implementation_steps"]) >= 4:
            score += 0.05
        if scenario["estimated_savings"]["payback_period_years"] <= 3:
            score += 0.05
        if persona in ["zuri", "amina", "bjorn", "arjun"]:
            score += 0.05
        
        return min(score, 0.95)
    
    def search_scenarios(self, query: str) -> List[Dict]:
        """Search scenarios based on keywords"""
        query_lower = query.lower()
        matching_scenarios = []
        
        for scenario_id, scenario in self.scenarios.items():
            searchable_text = (
                scenario['title'] + " " + 
                scenario['description'] + " " + 
                " ".join(scenario['implementation_steps'])
            ).lower()
            
            if any(word in searchable_text for word in query_lower.split()):
                matching_scenarios.append({
                    "id": scenario_id,
                    "title": scenario['title'],
                    "description": scenario['description'],
                    "industry": scenario['industry'],
                    "complexity": scenario['complexity'],
                    "payback_period": scenario['estimated_savings']['payback_period_years']
                })
        
        return sorted(matching_scenarios, key=lambda x: x['payback_period'])
    
    def get_all_scenarios_summary(self) -> List[Dict]:
        """Get summary of all scenarios"""
        summaries = []
        
        for scenario_id, scenario in self.scenarios.items():
            summaries.append({
                "id": scenario_id,
                "title": scenario['title'],
                "description": scenario['description'][:150] + "...",
                "industry": scenario['industry'],
                "company_size": scenario['company_size'],
                "complexity": scenario['complexity'],
                "payback_period": f"{scenario['estimated_savings']['payback_period_years']} years",
                "key_benefits": list(scenario['estimated_savings'].keys())[:3]
            })
        
        return summaries

# Global instance
dbo_service = EnhancedDBOService()
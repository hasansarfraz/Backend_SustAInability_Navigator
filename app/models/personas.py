from enum import Enum
from typing import Dict, List

class PersonaType(str, Enum):
    ZURI = "zuri"
    AMINA = "amina" 
    BJORN = "bjorn"
    ARJUN = "arjun"
    GENERAL = "general"

class PersonaConfig:
    PERSONAS = {
        PersonaType.ZURI: {
            "name": "Zuri",
            "role": "Multinational Corporate Sustainability Leader",
            "company_size": "10,000+ employees",
            "industry": "Tech",
            "focus": ["strategic sustainability", "global compliance", "investor expectations"],
            "pain_points": ["execution challenges", "regulatory compliance", "scale implementation"],
            "preferred_solutions": ["enterprise-grade tools", "strategic solutions", "global implementation"],
            "priorities": ["ESG compliance", "Investor relations", "Global scalability", "Strategic sustainability"]
        },
        PersonaType.AMINA: {
            "name": "Amina", 
            "role": "Cost-Conscious Business Owner",
            "company_size": "50-200 employees",
            "industry": "Manufacturing",
            "focus": ["cost savings", "efficiency", "profitability"],
            "pain_points": ["sustainability costs", "ROI concerns", "resource constraints"],
            "preferred_solutions": ["clear ROI", "cost-effective solutions", "immediate benefits"],
            "priorities": ["Cost optimization", "Quick ROI", "Operational efficiency", "Resource management"]
        },
        PersonaType.BJORN: {
            "name": "Björn",
            "role": "Head of Finance, Long-Time Siemens Customer", 
            "company_size": "500+ employees",
            "industry": "Construction",
            "focus": ["DBO integration", "existing workflows", "financial impact"],
            "pain_points": ["workflow changes", "DBO adoption", "process integration"],
            "preferred_solutions": ["Siemens ecosystem", "guided implementation", "proven ROI"],
            "priorities": ["Technology integration", "Vendor relationships", "Risk management", "Proven solutions"]
        },
        PersonaType.ARJUN: {
            "name": "Arjun",
            "role": "Sustainability Champion",
            "company_size": "80-300 employees", 
            "industry": "Retail",
            "focus": ["competitive advantage", "transparency", "business growth"],
            "pain_points": ["implementation support", "metrics tracking", "impact measurement"],
            "preferred_solutions": ["clear metrics", "transparency tools", "growth alignment"],
            "priorities": ["Sustainability impact", "Brand positioning", "Stakeholder engagement", "Competitive advantage"]
        }
    }
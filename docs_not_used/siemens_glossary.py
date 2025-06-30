"""
Official Siemens Glossary Content for Semantic Search
Extracted from: Siemens Glossary of Sustainability Terms and Abbreviations, Status: 24.06.2025
"""

SIEMENS_OFFICIAL_CONTENT = {
    "dbo_definition": {
        "content": """Digital Business Optimizer (DBO™)

The Digital Business Optimizer (DBO™), brought to you by Siemens Financial Services, Inc., is your trusted companion in the journey toward a greener future. Developed by Siemens Technology, the DBO™ offers an interactive platform to explore the technology investment options for decarbonizing your facility's energy consumption.

Key Features:
- Customized Decarbonization Strategy: The DBO™ allows you to digitally customize a decarbonization strategy for your facilities within the contiguous United States.
- Data-Driven Insights: The DBO™ draws data from trusted sources to provide accurate and reliable information.
- Tailored Scenarios: The DBO™ crafts scenarios that align with your preferences.
- Competitive Edge: By reducing energy costs and enhancing efficiency, you can gain a competitive edge.
- Navigating Complexity: The DBO™ simplifies the process, offering a straightforward pathway to assess decarbonization measures.

Website: https://www.dbo.siemens.com/

What Questions Can DBO™ Answer?
- What technologies should I consider for my facility?
- What is the potential return on investment (ROI) for various decarbonization measures?
- How can I reduce my facility's carbon footprint while staying within budget?
- What are the financial incentives available for implementing these technologies?
- How do I prioritize different decarbonization strategies?""",
        "source": "Official Siemens Glossary of Sustainability Terms and Abbreviations, Status: 24.06.2025",
        "section": "DBO Definition",
        "authority": "high",
        "keywords": ["dbo", "digital business optimizer", "decarbonization", "siemens financial services"]
    },
    
    "sigreen_definition": {
        "content": """SiGREEN

SiGREEN is a Siemens tool to contribute to decarbonization through digitalization. Customers and Siemens can manage the carbon footprint of products and track and improve product-related emissions based on reliable data.

Key Capabilities:
- Carbon footprint management for products
- Track and improve product-related emissions
- Based on reliable data
- Contribution to decarbonization through digitalization

Website: https://xcelerator.siemens.com/global/en/all-offerings/products/s/sigreen.html""",
        "source": "Official Siemens Glossary of Sustainability Terms and Abbreviations, Status: 24.06.2025",
        "section": "SiGREEN Definition",
        "authority": "high",
        "keywords": ["sigreen", "carbon footprint", "digitalization", "emissions tracking"]
    },
    
    "degree_framework": {
        "content": """DEGREE Sustainability Framework

The Siemens framework for sustainability, which constitutes a 360-degree approach for all stakeholders. For each of the six focus areas of the DEGREE framework (Decarbonization, Ethics, Governance, Resource efficiency, Equity, Employability), key performance indicators underpin the ambitions.

Six Focus Areas:
1. Decarbonization: Support the 1.5°C target to fight global warming
2. Ethics: Foster a culture of trust, adhere to ethical standards and handle data with care
3. Governance: Apply state-of-the-art systems for effective and responsible business conduct
4. Resource efficiency: Achieve circularity and dematerialization
5. Equity: Foster diversity, inclusion, and community development to create a sense of belonging
6. Employability: Enable our people to stay resilient and relevant in a permanently changing environment""",
        "source": "Official Siemens Glossary of Sustainability Terms and Abbreviations, Status: 24.06.2025",
        "section": "DEGREE Framework",
        "authority": "high",
        "keywords": ["degree", "sustainability framework", "decarbonization", "ethics", "governance", "equity", "employability"]
    },
    
    "b2s_methodology": {
        "content": """Business to Society® (B2S)

The Business to Society® (B2S) methodology is Siemens' way to evaluate our contributions to society. It allows us to measure and communicate progress in various dimensions: strengthening the economy, developing jobs and skills, driving innovation, protecting the environment and improving quality of life.

Website: https://www.siemens.com/global/en/company/about/history/specials/175-years/business-to-society.html""",
        "source": "Official Siemens Glossary of Sustainability Terms and Abbreviations, Status: 24.06.2025",
        "section": "B2S Methodology",
        "authority": "high",
        "keywords": ["b2s", "business to society", "contributions to society", "methodology"]
    },
    
    "esg_radar": {
        "content": """ESG Radar

Siemens internal digital risk due diligence tool. It helps Siemens identify and assess potential environmental and social risks, and the associated human rights and reputational risks related to customer business.""",
        "source": "Official Siemens Glossary of Sustainability Terms and Abbreviations, Status: 24.06.2025",
        "section": "ESG Radar",
        "authority": "high",
        "keywords": ["esg radar", "risk due diligence", "environmental risks", "social risks"]
    },
    
    "cwa_assessment": {
        "content": """Carbon Web Assessment (CWA)

Siemens developed the CWA to enable suppliers an assessment of their own carbon emissions. A second step also provides detailed ways of reducing the emissions.""",
        "source": "Official Siemens Glossary of Sustainability Terms and Abbreviations, Status: 24.06.2025",
        "section": "CWA Assessment",
        "authority": "high",
        "keywords": ["cwa", "carbon web assessment", "suppliers", "carbon emissions"]
    }
}

def get_all_document_chunks():
    """Get all document chunks for processing"""
    return SIEMENS_OFFICIAL_CONTENT

def get_document_by_keywords(keywords):
    """Find documents matching keywords"""
    results = []
    for doc_id, doc_data in SIEMENS_OFFICIAL_CONTENT.items():
        doc_keywords = doc_data.get("keywords", [])
        if any(keyword in doc_keywords for keyword in keywords):
            results.append((doc_id, doc_data))
    return results
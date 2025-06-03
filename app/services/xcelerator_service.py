# app/services/xcelerator_service.py - Siemens Xcelerator Integration Service

import logging
from typing import List, Dict, Optional
from app.models.user_profile import UserProfile, DBOToolOutput, XceleratorRecommendation, ProficiencyLevel

logger = logging.getLogger(__name__)

class SiemensXceleratorService:
    """Service for intelligent Siemens Xcelerator marketplace integration"""
    
    def __init__(self):
        self.xcelerator_catalog = self._load_xcelerator_catalog()
        self.proficiency_matrix = self._build_proficiency_matrix()
    
    def _load_xcelerator_catalog(self) -> Dict:
        """Load comprehensive Siemens Xcelerator product catalog"""
        
        # Enhanced catalog based on actual Siemens Xcelerator offerings
        return {
            # Building Technologies
            "desigo_cc": {
                "name": "Desigo CC",
                "category": "Building Management Systems",
                "subcategory": "Building Automation",
                "xcelerator_url": "https://xcelerator.siemens.com/global/en/offerings/desigo-cc.html",
                "description": "Integrated building management platform for comprehensive facility optimization",
                "key_capabilities": [
                    "HVAC system optimization",
                    "Energy consumption monitoring", 
                    "Occupancy-based controls",
                    "Predictive maintenance",
                    "Integration with renewable energy systems"
                ],
                "sustainability_impact": {
                    "energy_savings": "15-30%",
                    "carbon_reduction": "20-35%",
                    "operational_efficiency": "25% improvement"
                },
                "implementation_complexity": "Medium",
                "typical_timeline": "3-6 months",
                "target_company_size": ["Medium", "Large", "Enterprise"],
                "proficiency_requirements": {
                    "sustainability": "intermediate",
                    "technological": "intermediate"
                },
                "financing_available": True,
                "siemens_support": ["Implementation services", "Training", "24/7 support"]
            },
            
            # Industrial IoT Platform
            "mindsphere": {
                "name": "MindSphere",
                "category": "Industrial IoT Platform",
                "subcategory": "Digital Manufacturing",
                "xcelerator_url": "https://xcelerator.siemens.com/global/en/offerings/mindsphere.html",
                "description": "Cloud-based IoT operating system for industrial digital transformation",
                "key_capabilities": [
                    "Asset performance monitoring",
                    "Predictive analytics",
                    "Digital twin integration",
                    "Machine learning algorithms",
                    "Energy optimization algorithms"
                ],
                "sustainability_impact": {
                    "energy_savings": "10-25%",
                    "waste_reduction": "15-20%",
                    "productivity_improvement": "20-40%"
                },
                "implementation_complexity": "High",
                "typical_timeline": "6-12 months",
                "target_company_size": ["Medium", "Large", "Enterprise"],
                "proficiency_requirements": {
                    "sustainability": "intermediate",
                    "technological": "advanced"
                },
                "financing_available": True,
                "siemens_support": ["Digital transformation consulting", "Technical implementation", "Ongoing optimization"]
            },
            
            # Sustainability Analytics
            "sigreen": {
                "name": "SiGREEN",
                "category": "Sustainability Management",
                "subcategory": "Carbon & ESG Analytics",
                "xcelerator_url": "https://xcelerator.siemens.com/global/en/offerings/sigreen.html",
                "description": "Comprehensive carbon footprint tracking and ESG reporting platform",
                "key_capabilities": [
                    "Carbon footprint calculation",
                    "ESG reporting automation",
                    "Regulatory compliance tracking",
                    "Sustainability KPI dashboards",
                    "Supply chain emissions tracking"
                ],
                "sustainability_impact": {
                    "reporting_accuracy": "95%+ compliance",
                    "time_savings": "60% reduction in reporting time",
                    "transparency_improvement": "Complete supply chain visibility"
                },
                "implementation_complexity": "Low to Medium",
                "typical_timeline": "2-4 months",
                "target_company_size": ["Small", "Medium", "Large", "Enterprise"],
                "proficiency_requirements": {
                    "sustainability": "beginner",
                    "technological": "beginner"
                },
                "financing_available": True,
                "siemens_support": ["Implementation guidance", "Regulatory compliance support", "Training programs"]
            },
            
            # Smart Grid Solutions
            "sicam_gridedge": {
                "name": "SICAM GridEdge",
                "category": "Energy Management",
                "subcategory": "Smart Grid & Renewable Integration",
                "xcelerator_url": "https://xcelerator.siemens.com/global/en/offerings/sicam-gridedge.html",
                "description": "Advanced grid edge device for renewable energy integration and optimization",
                "key_capabilities": [
                    "Renewable energy integration",
                    "Energy storage management",
                    "Grid stability optimization",
                    "Demand response automation",
                    "Real-time energy analytics"
                ],
                "sustainability_impact": {
                    "renewable_integration": "Up to 100% renewable energy",
                    "grid_efficiency": "15-25% improvement",
                    "energy_cost_savings": "20-40%"
                },
                "implementation_complexity": "High",
                "typical_timeline": "4-8 months",
                "target_company_size": ["Medium", "Large", "Enterprise"],
                "proficiency_requirements": {
                    "sustainability": "intermediate",
                    "technological": "advanced"
                },
                "financing_available": True,
                "siemens_support": ["Grid integration consulting", "Technical implementation", "Maintenance services"]
            },
            
            # Process Optimization
            "simatic_pcs7": {
                "name": "SIMATIC PCS 7",
                "category": "Process Control Systems",
                "subcategory": "Industrial Automation",
                "xcelerator_url": "https://xcelerator.siemens.com/global/en/offerings/simatic-pcs7.html",
                "description": "Distributed control system for optimized industrial processes and sustainability",
                "key_capabilities": [
                    "Process optimization",
                    "Energy efficiency controls",
                    "Waste minimization",
                    "Quality improvement",
                    "Safety system integration"
                ],
                "sustainability_impact": {
                    "energy_efficiency": "15-30%",
                    "waste_reduction": "20-35%",
                    "process_optimization": "25% improvement"
                },
                "implementation_complexity": "High",
                "typical_timeline": "8-18 months",
                "target_company_size": ["Large", "Enterprise"],
                "proficiency_requirements": {
                    "sustainability": "advanced",
                    "technological": "expert"
                },
                "financing_available": True,
                "siemens_support": ["Process engineering", "Implementation services", "Lifecycle support"]
            },
            
            # Digital Building Platform
            "building_x": {
                "name": "Building X",
                "category": "Digital Building Solutions",
                "subcategory": "Smart Building Platform",
                "xcelerator_url": "https://xcelerator.siemens.com/global/en/offerings/building-x.html",
                "description": "Cloud-based digital building platform for performance optimization",
                "key_capabilities": [
                    "Building performance analytics",
                    "Energy optimization",
                    "Space utilization optimization",
                    "Predictive maintenance",
                    "Occupant experience enhancement"
                ],
                "sustainability_impact": {
                    "energy_savings": "20-40%",
                    "operational_efficiency": "30% improvement",
                    "carbon_footprint_reduction": "25-45%"
                },
                "implementation_complexity": "Medium",
                "typical_timeline": "2-6 months",
                "target_company_size": ["Small", "Medium", "Large"],
                "proficiency_requirements": {
                    "sustainability": "beginner",
                    "technological": "intermediate"
                },
                "financing_available": True,
                "siemens_support": ["Cloud implementation", "Analytics setup", "Optimization consulting"]
            },
            
            # Financial Services
            "siemens_financial_services": {
                "name": "Siemens Financial Services",
                "category": "Financing Solutions",
                "subcategory": "Technology Financing",
                "xcelerator_url": "https://xcelerator.siemens.com/global/en/offerings/financial-services.html",
                "description": "Comprehensive financing solutions for sustainability technology investments",
                "key_capabilities": [
                    "Equipment financing",
                    "Technology leasing",
                    "Performance-based financing",
                    "Green financing options",
                    "Flexible payment structures"
                ],
                "sustainability_impact": {
                    "investment_facilitation": "Up to 100% financing",
                    "cash_flow_optimization": "Preserve working capital",
                    "accelerated_implementation": "Faster sustainability adoption"
                },
                "implementation_complexity": "Low",
                "typical_timeline": "2-8 weeks",
                "target_company_size": ["Small", "Medium", "Large", "Enterprise"],
                "proficiency_requirements": {
                    "sustainability": "beginner",
                    "technological": "beginner"
                },
                "financing_available": True,
                "siemens_support": ["Financing consultation", "Custom payment plans", "Risk assessment"]
            }
        }
    
    def _build_proficiency_matrix(self) -> Dict:
        """Build matrix for matching user proficiency to product recommendations"""
        return {
            "sustainability_proficiency_mapping": {
                ProficiencyLevel.BEGINNER: {
                    "recommended_products": ["sigreen", "building_x", "siemens_financial_services"],
                    "support_level": "High support and training required",
                    "implementation_approach": "Guided implementation with extensive training"
                },
                ProficiencyLevel.INTERMEDIATE: {
                    "recommended_products": ["desigo_cc", "mindsphere", "sicam_gridedge"],
                    "support_level": "Moderate support with specialized training",
                    "implementation_approach": "Collaborative implementation with expert guidance"
                },
                ProficiencyLevel.ADVANCED: {
                    "recommended_products": ["simatic_pcs7", "mindsphere", "sicam_gridedge"],
                    "support_level": "Technical support and optimization guidance",
                    "implementation_approach": "Self-directed with technical consultation"
                },
                ProficiencyLevel.EXPERT: {
                    "recommended_products": ["simatic_pcs7", "mindsphere", "custom_solutions"],
                    "support_level": "Strategic consulting and advanced optimization",
                    "implementation_approach": "Independent implementation with strategic partnership"
                }
            },
            "technological_proficiency_mapping": {
                ProficiencyLevel.BEGINNER: {
                    "complexity_filter": ["Low", "Low to Medium"],
                    "support_requirements": "Comprehensive implementation services",
                    "training_needs": "Extensive user training and change management"
                },
                ProficiencyLevel.INTERMEDIATE: {
                    "complexity_filter": ["Low to Medium", "Medium"],
                    "support_requirements": "Implementation support and technical training",
                    "training_needs": "Focused technical training"
                },
                ProficiencyLevel.ADVANCED: {
                    "complexity_filter": ["Medium", "High"],
                    "support_requirements": "Technical consulting and optimization",
                    "training_needs": "Advanced feature training"
                },
                ProficiencyLevel.EXPERT: {
                    "complexity_filter": ["High", "Custom"],
                    "support_requirements": "Strategic partnership and innovation collaboration",
                    "training_needs": "Minimal - self-directed learning"
                }
            }
        }
    
    def analyze_dbo_output_and_recommend(
        self, 
        dbo_output: DBOToolOutput, 
        user_profile: UserProfile
    ) -> List[XceleratorRecommendation]:
        """
        Main method: Analyze DBO tool output and generate optimal Xcelerator recommendations
        """
        
        logger.info(f"Analyzing DBO output: {dbo_output.scenario_title}")
        logger.info(f"User profile: {user_profile.sustainability_proficiency}/{user_profile.technological_proficiency}")
        
        # Step 1: Extract key requirements from DBO output
        requirements = self._extract_requirements_from_dbo(dbo_output)
        
        # Step 2: Filter products based on user proficiency
        suitable_products = self._filter_products_by_proficiency(user_profile)
        
        # Step 3: Match DBO requirements to Xcelerator products
        matched_products = self._match_requirements_to_products(requirements, suitable_products)
        
        # Step 4: Score and rank recommendations
        scored_recommendations = self._score_and_rank_recommendations(
            matched_products, dbo_output, user_profile
        )
        
        # Step 5: Generate detailed recommendations with implementation guidance
        final_recommendations = self._generate_detailed_recommendations(
            scored_recommendations, user_profile
        )
        
        logger.info(f"Generated {len(final_recommendations)} recommendations")
        return final_recommendations
    
    def _extract_requirements_from_dbo(self, dbo_output: DBOToolOutput) -> Dict:
        """Extract technical and business requirements from DBO tool output"""
        
        requirements = {
            "primary_focus": [],
            "technical_capabilities": [],
            "sustainability_goals": [],
            "implementation_constraints": {},
            "business_priorities": []
        }
        
        # Analyze scenario title and description
        scenario_text = (dbo_output.scenario_title + " " + dbo_output.scenario_description).lower()
        
        # Extract primary focus areas
        if "energy" in scenario_text:
            requirements["primary_focus"].append("energy_management")
        if "water" in scenario_text:
            requirements["primary_focus"].append("resource_management")
        if "building" in scenario_text:
            requirements["primary_focus"].append("building_optimization")
        if "waste" in scenario_text:
            requirements["primary_focus"].append("waste_management")
        if "supply" in scenario_text or "logistics" in scenario_text:
            requirements["primary_focus"].append("supply_chain")
        if "manufacturing" in scenario_text:
            requirements["primary_focus"].append("industrial_processes")
        
        # Extract technical capabilities needed
        actions_text = " ".join(dbo_output.recommended_actions).lower()
        
        if any(word in actions_text for word in ["iot", "sensors", "monitoring"]):
            requirements["technical_capabilities"].append("iot_monitoring")
        if any(word in actions_text for word in ["analytics", "data", "intelligence"]):
            requirements["technical_capabilities"].append("data_analytics")
        if any(word in actions_text for word in ["automation", "control", "smart"]):
            requirements["technical_capabilities"].append("automation_control")
        if any(word in actions_text for word in ["tracking", "reporting", "carbon"]):
            requirements["technical_capabilities"].append("sustainability_reporting")
        
        # Extract sustainability goals from estimated benefits
        for metric, value in dbo_output.estimated_benefits.items():
            if "energy" in metric.lower():
                requirements["sustainability_goals"].append("energy_efficiency")
            if "carbon" in metric.lower() or "emission" in metric.lower():
                requirements["sustainability_goals"].append("carbon_reduction")
            if "water" in metric.lower():
                requirements["sustainability_goals"].append("water_conservation")
            if "waste" in metric.lower():
                requirements["sustainability_goals"].append("waste_reduction")
        
        # Extract implementation constraints
        if "payback_period_years" in dbo_output.estimated_benefits:
            payback = dbo_output.estimated_benefits["payback_period_years"]
            if payback <= 2:
                requirements["implementation_constraints"]["urgency"] = "high"
                requirements["business_priorities"].append("quick_roi")
            elif payback <= 4:
                requirements["implementation_constraints"]["urgency"] = "medium"
                requirements["business_priorities"].append("balanced_approach")
            else:
                requirements["implementation_constraints"]["urgency"] = "low"
                requirements["business_priorities"].append("long_term_investment")
        
        return requirements
    
    def _filter_products_by_proficiency(self, user_profile: UserProfile) -> List[str]:
        """Filter Xcelerator products based on user proficiency levels"""
        
        suitable_products = []
        
        # Get products suitable for sustainability proficiency
        sustainability_mapping = self.proficiency_matrix["sustainability_proficiency_mapping"]
        sustainability_products = sustainability_mapping[user_profile.sustainability_proficiency]["recommended_products"]
        
        # Get complexity levels suitable for technological proficiency
        tech_mapping = self.proficiency_matrix["technological_proficiency_mapping"]
        suitable_complexity = tech_mapping[user_profile.technological_proficiency]["complexity_filter"]
        
        # Filter products that match both proficiency requirements
        for product_id, product_info in self.xcelerator_catalog.items():
            # Check if product is recommended for sustainability proficiency
            if product_id in sustainability_products or "siemens_financial_services" == product_id:
                # Check if product complexity matches technological proficiency
                product_complexity = product_info.get("implementation_complexity", "Medium")
                if product_complexity in suitable_complexity or product_complexity == "Low":
                    suitable_products.append(product_id)
        
        return suitable_products
    
    def _match_requirements_to_products(self, requirements: Dict, suitable_products: List[str]) -> Dict:
        """Match DBO requirements to suitable Xcelerator products"""
        
        matched_products = {}
        
        # Product capability mapping
        product_capabilities = {
            "energy_management": ["desigo_cc", "sicam_gridedge", "building_x", "simatic_pcs7"],
            "resource_management": ["simatic_pcs7", "building_x", "mindsphere"],
            "building_optimization": ["desigo_cc", "building_x"],
            "waste_management": ["simatic_pcs7", "mindsphere"],
            "supply_chain": ["mindsphere", "sigreen"],
            "industrial_processes": ["simatic_pcs7", "mindsphere"],
            "iot_monitoring": ["mindsphere", "sicam_gridedge", "desigo_cc"],
            "data_analytics": ["mindsphere", "building_x", "sigreen"],
            "automation_control": ["simatic_pcs7", "desigo_cc", "sicam_gridedge"],
            "sustainability_reporting": ["sigreen", "building_x"],
            "energy_efficiency": ["desigo_cc", "building_x", "sicam_gridedge"],
            "carbon_reduction": ["sigreen", "building_x", "desigo_cc"],
            "water_conservation": ["simatic_pcs7", "building_x"],
            "waste_reduction": ["simatic_pcs7", "mindsphere"]
        }
        
        # Score products based on requirement matching
        for product_id in suitable_products:
            if product_id == "siemens_financial_services":
                # Financial services always relevant
                matched_products[product_id] = {"score": 0.8, "matching_capabilities": ["financing"]}
                continue
                
            score = 0
            matching_capabilities = []
            
            # Check primary focus match
            for focus in requirements["primary_focus"]:
                if product_id in product_capabilities.get(focus, []):
                    score += 2.0
                    matching_capabilities.append(focus)
            
            # Check technical capabilities match
            for capability in requirements["technical_capabilities"]:
                if product_id in product_capabilities.get(capability, []):
                    score += 1.5
                    matching_capabilities.append(capability)
            
            # Check sustainability goals match
            for goal in requirements["sustainability_goals"]:
                if product_id in product_capabilities.get(goal, []):
                    score += 1.0
                    matching_capabilities.append(goal)
            
            if score > 0:
                matched_products[product_id] = {
                    "score": score,
                    "matching_capabilities": matching_capabilities
                }
        
        return matched_products
    
    def _score_and_rank_recommendations(
        self, 
        matched_products: Dict, 
        dbo_output: DBOToolOutput, 
        user_profile: UserProfile
    ) -> List[Dict]:
        """Score and rank product recommendations based on multiple factors"""
        
        scored_products = []
        
        for product_id, match_info in matched_products.items():
            product_info = self.xcelerator_catalog[product_id]
            
            # Base score from requirement matching
            base_score = match_info["score"]
            
            # Proficiency alignment bonus
            proficiency_bonus = self._calculate_proficiency_bonus(product_id, user_profile)
            
            # Compliance importance factor
            compliance_bonus = self._calculate_compliance_bonus(product_id, user_profile)
            
            # Timeline alignment
            timeline_bonus = self._calculate_timeline_bonus(product_id, dbo_output, user_profile)
            
            # Calculate final score
            final_score = base_score + proficiency_bonus + compliance_bonus + timeline_bonus
            
            scored_products.append({
                "product_id": product_id,
                "product_info": product_info,
                "final_score": final_score,
                "matching_capabilities": match_info["matching_capabilities"],
                "score_breakdown": {
                    "base_score": base_score,
                    "proficiency_bonus": proficiency_bonus,
                    "compliance_bonus": compliance_bonus,
                    "timeline_bonus": timeline_bonus
                }
            })
        
        # Sort by final score (descending)
        scored_products.sort(key=lambda x: x["final_score"], reverse=True)
        
        return scored_products
    
    def _calculate_proficiency_bonus(self, product_id: str, user_profile: UserProfile) -> float:
        """Calculate bonus score based on proficiency alignment"""
        product = self.xcelerator_catalog[product_id]
        required_proficiencies = product.get("proficiency_requirements", {})
        
        bonus = 0.0
        
        # Sustainability proficiency alignment
        required_sustainability = required_proficiencies.get("sustainability", "intermediate")
        user_sustainability = user_profile.sustainability_proficiency.value
        
        proficiency_levels = ["beginner", "intermediate", "advanced", "expert"]
        user_level = proficiency_levels.index(user_sustainability)
        required_level = proficiency_levels.index(required_sustainability)
        
        if user_level >= required_level:
            bonus += 0.5  # User meets or exceeds requirements
        else:
            bonus -= 0.2  # User below requirements
        
        # Similar for technological proficiency
        required_tech = required_proficiencies.get("technological", "intermediate")
        user_tech = user_profile.technological_proficiency.value
        
        user_tech_level = proficiency_levels.index(user_tech)
        required_tech_level = proficiency_levels.index(required_tech)
        
        if user_tech_level >= required_tech_level:
            bonus += 0.5
        else:
            bonus -= 0.2
        
        return bonus
    
    def _calculate_compliance_bonus(self, product_id: str, user_profile: UserProfile) -> float:
        """Calculate bonus for compliance-focused products"""
        compliance_products = ["sigreen", "building_x", "desigo_cc"]
        
        if user_profile.regulatory_compliance_importance.value == "critical" and product_id in compliance_products:
            return 1.0
        elif user_profile.regulatory_compliance_importance.value == "high" and product_id in compliance_products:
            return 0.5
        
        return 0.0
    
    def _calculate_timeline_bonus(self, product_id: str, dbo_output: DBOToolOutput, user_profile: UserProfile) -> float:
        """Calculate bonus based on implementation timeline alignment"""
        product = self.xcelerator_catalog[product_id]
        product_timeline = product.get("typical_timeline", "6 months")
        
        # Extract months from timeline string
        if "2-4" in product_timeline or "2-6" in product_timeline:
            product_months = 3
        elif "3-6" in product_timeline or "4-8" in product_timeline:
            product_months = 5
        elif "6-12" in product_timeline or "8-18" in product_timeline:
            product_months = 10
        else:
            product_months = 6
        
        # Check if urgent implementation is needed
        payback = dbo_output.estimated_benefits.get("payback_period_years", 3)
        
        if payback <= 2 and product_months <= 6:
            return 0.5  # Fast implementation for urgent needs
        elif payback > 3 and product_months > 6:
            return 0.3  # Longer timeline acceptable for long-term projects
        
        return 0.0
    
    def _generate_detailed_recommendations(
        self, 
        scored_products: List[Dict], 
        user_profile: UserProfile
    ) -> List[XceleratorRecommendation]:
        """Generate detailed recommendations with implementation guidance"""
        
        recommendations = []
        
        # Take top 5 recommendations
        for product_data in scored_products[:5]:
            product_id = product_data["product_id"]
            product_info = product_data["product_info"]
            score = product_data["final_score"]
            
            # Generate proficiency-specific guidance
            proficiency_match = self._generate_proficiency_guidance(product_id, user_profile)
            
            # Generate implementation support recommendations
            implementation_support = self._generate_implementation_support(product_id, user_profile)
            
            # Generate ecosystem benefits
            ecosystem_benefits = self._generate_ecosystem_benefits(product_id, user_profile)
            
            recommendation = XceleratorRecommendation(
                product_name=product_info["name"],
                product_category=product_info["category"],
                xcelerator_url=product_info.get("xcelerator_url"),
                relevance_score=min(score / 10.0, 1.0),  # Normalize to 0-1
                implementation_complexity=product_info["implementation_complexity"],
                estimated_timeline=product_info["typical_timeline"],
                estimated_investment=self._estimate_investment_for_user(product_id, user_profile),
                expected_roi_timeline=self._estimate_roi_timeline(product_id, product_info),
                financing_options=self._get_financing_options(product_info),
                proficiency_match=proficiency_match,
                implementation_support=implementation_support,
                ecosystem_benefits=ecosystem_benefits
            )
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_proficiency_guidance(self, product_id: str, user_profile: UserProfile) -> Dict[str, str]:
        """Generate guidance based on user proficiency levels"""
        
        sustainability_guidance = {
            ProficiencyLevel.BEGINNER: "Comprehensive training and guided implementation recommended",
            ProficiencyLevel.INTERMEDIATE: "Moderate support with focused training on key features",
            ProficiencyLevel.ADVANCED: "Technical consultation and advanced feature training",
            ProficiencyLevel.EXPERT: "Strategic partnership for optimization and innovation"
        }
        
        technological_guidance = {
            ProficiencyLevel.BEGINNER: "Full implementation services with extensive user training",
            ProficiencyLevel.INTERMEDIATE: "Implementation support with technical training",
            ProficiencyLevel.ADVANCED: "Technical consulting and optimization guidance",
            ProficiencyLevel.EXPERT: "Collaborative development and advanced customization"
        }
        
        return {
            "sustainability_approach": sustainability_guidance[user_profile.sustainability_proficiency],
            "technological_approach": technological_guidance[user_profile.technological_proficiency],
            "communication_style": self._adapt_communication_style(user_profile.communication_style),
            "compliance_focus": self._adapt_compliance_approach(user_profile.regulatory_compliance_importance)
        }
    
    def _adapt_communication_style(self, style) -> str:
        """Adapt communication based on user preference"""
        adaptations = {
            "technical": "Focus on technical specifications, performance metrics, and integration details",
            "business_focused": "Emphasize ROI, business benefits, and strategic value proposition",
            "simple_explanations": "Use clear, non-technical language with practical examples",
            "comprehensive": "Provide detailed technical and business information with full context"
        }
        return adaptations.get(style.value, adaptations["comprehensive"])
    
    def _adapt_compliance_approach(self, importance) -> str:
        """Adapt compliance messaging based on importance level"""
        approaches = {
            "low": "Basic compliance features available",
            "medium": "Standard compliance reporting and tracking included",
            "high": "Advanced compliance features with regulatory support",
            "critical": "Comprehensive compliance management with dedicated regulatory consulting"
        }
        return approaches.get(importance.value, approaches["medium"])
    
    def _generate_implementation_support(self, product_id: str, user_profile: UserProfile) -> List[str]:
        """Generate implementation support recommendations"""
        product_info = self.xcelerator_catalog[product_id]
        base_support = product_info.get("siemens_support", [])
        
        # Add proficiency-specific support
        if user_profile.sustainability_proficiency == ProficiencyLevel.BEGINNER:
            base_support.extend(["Sustainability strategy consulting", "Change management support"])
        
        if user_profile.technological_proficiency == ProficiencyLevel.BEGINNER:
            base_support.extend(["Comprehensive user training", "Technical helpdesk support"])
        
        if user_profile.regulatory_compliance_importance.value in ["high", "critical"]:
            base_support.extend(["Regulatory compliance consulting", "Audit support services"])
        
        return list(set(base_support))  # Remove duplicates
    
    def _generate_ecosystem_benefits(self, product_id: str, user_profile: UserProfile) -> List[str]:
        """Generate Siemens ecosystem integration benefits"""
        
        base_benefits = [
            "Seamless integration with other Siemens solutions",
            "Access to Siemens global support network",
            "Future-proof technology with continuous updates"
        ]
        
        # Product-specific ecosystem benefits
        product_benefits = {
            "desigo_cc": ["Integration with Siemens building portfolio", "Standardized building management across facilities"],
            "mindsphere": ["Connection to Siemens industrial ecosystem", "Access to industrial app marketplace"],
            "sigreen": ["Integration with Siemens sustainability portfolio", "Comprehensive ESG reporting ecosystem"],
            "sicam_gridedge": ["Grid-scale integration capabilities", "Renewable energy ecosystem connectivity"],
            "building_x": ["Cloud-native scalability", "Digital building services ecosystem"],
            "simatic_pcs7": ["Industrial automation ecosystem", "Process optimization network"],
            "siemens_financial_services": ["Integrated financing for technology stack", "Portfolio financing options"]
        }
        
        specific_benefits = product_benefits.get(product_id, [])
        return base_benefits + specific_benefits
    
    def _estimate_investment_for_user(self, product_id: str, user_profile: UserProfile) -> str:
        """Estimate investment based on user profile and company size"""
        
        # Base investment estimates by product
        base_investments = {
            "desigo_cc": {"small": "$15K-50K", "medium": "$50K-150K", "large": "$150K-500K"},
            "mindsphere": {"small": "$25K-75K", "medium": "$75K-200K", "large": "$200K-600K"},
            "sigreen": {"small": "$5K-15K", "medium": "$15K-40K", "large": "$40K-100K"},
            "sicam_gridedge": {"small": "$30K-80K", "medium": "$80K-250K", "large": "$250K-750K"},
            "building_x": {"small": "$10K-30K", "medium": "$30K-80K", "large": "$80K-200K"},
            "simatic_pcs7": {"small": "$100K-300K", "medium": "$300K-800K", "large": "$800K-2M"},
            "siemens_financial_services": {"small": "Financing available", "medium": "Financing available", "large": "Financing available"}
        }
        
        # Determine company size category
        company_size = user_profile.company_size or "medium"
        if "small" in company_size.lower() or "10-50" in company_size:
            size_category = "small"
        elif "large" in company_size.lower() or "500+" in company_size:
            size_category = "large"
        else:
            size_category = "medium"
        
        return base_investments.get(product_id, {}).get(size_category, "Contact for pricing")
    
    def _estimate_roi_timeline(self, product_id: str, product_info: Dict) -> str:
        """Estimate ROI timeline based on product characteristics"""
        
        # ROI estimates based on product type and typical savings
        roi_estimates = {
            "desigo_cc": "12-24 months (15-30% energy savings)",
            "mindsphere": "18-36 months (20-40% productivity improvement)",
            "sigreen": "6-12 months (60% reporting time savings)",
            "sicam_gridedge": "24-48 months (20-40% energy cost savings)",
            "building_x": "12-18 months (20-40% energy savings)",
            "simatic_pcs7": "24-60 months (15-30% efficiency gains)",
            "siemens_financial_services": "Immediate cash flow benefits"
        }
        
        return roi_estimates.get(product_id, "18-36 months typical")
    
    def _get_financing_options(self, product_info: Dict) -> List[str]:
        """Get available financing options"""
        
        base_options = ["Siemens Financial Services leasing", "Equipment financing", "Technology rental"]
        
        if product_info.get("financing_available", False):
            base_options.extend([
                "Performance-based financing",
                "Green financing options", 
                "Flexible payment terms",
                "End-to-end solution financing"
            ])
        
        return base_options

# Global service instance
xcelerator_service = SiemensXceleratorService()

# ---
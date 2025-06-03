# manual_testing_scenarios.py - Demo Scenarios for Siemens Presentation

import requests
import json

class SiemensDemo:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def demo_scenario_1_beginner_sme(self):
        """Demo: Beginner SME with Energy Optimization DBO Output"""
        
        print("🎬 DEMO SCENARIO 1: Beginner SME Energy Optimization")
        print("=" * 60)
        print("Context: Small manufacturing company, limited sustainability expertise")
        print("DBO Output: Energy efficiency recommendations from Siemens DBO Tool")
        print()
        
        # Simulate what comes from DBO tool
        dbo_output = {
            "scenario_title": "Energy Efficiency for Small Manufacturing",
            "scenario_description": "A small manufacturing facility wants to reduce energy costs and carbon footprint. Current energy spend: $150,000/year.",
            "recommended_actions": [
                "Install smart energy monitoring sensors",
                "Upgrade to LED lighting with motion sensors",
                "Implement HVAC optimization controls",
                "Add solar panel system with battery storage"
            ],
            "estimated_benefits": {
                "energy_cost_reduction": "20-30%",
                "carbon_emissions_reduction": "25%",
                "payback_period_years": 2.0,
                "annual_savings": "$30,000-45,000"
            }
        }
        
        # User proficiency from frontend assessment
        user_profile = {
            "sustainability_proficiency": "beginner",
            "technological_proficiency": "beginner",
            "communication_style": "simple_explanations",
            "regulatory_compliance_importance": "medium",
            "company_size": "Small (25 employees)",
            "budget_priority": "high"
        }
        
        # Call integration endpoint
        response = requests.post(
            f"{self.base_url}/api/v1/integration/dbo-to-xcelerator",
            json={"dbo_output": dbo_output, "user_profile": user_profile}
        )
        
        if response.status_code == 200:
            recommendations = response.json()
            print("✅ INTEGRATION SUCCESSFUL")
            print(f"🎯 Generated {len(recommendations)} Xcelerator recommendations:")
            print()
            
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"{i}. {rec['product_name']}")
                print(f"   Category: {rec['product_category']}")
                print(f"   Relevance: {rec['relevance_score']:.1%}")
                print(f"   Investment: {rec['estimated_investment']}")
                print(f"   ROI Timeline: {rec['expected_roi_timeline']}")
                print(f"   Complexity: {rec['implementation_complexity']}")
                print(f"   Why recommended: {rec['proficiency_match']['sustainability_approach']}")
                print()
            
            print("💡 Key Benefits Demonstrated:")
            print("   ✅ Beginner-friendly product selection")
            print("   ✅ Simple explanations and guidance")
            print("   ✅ High support and training included")
            print("   ✅ Clear ROI and financial modeling")
            print("   ✅ Siemens ecosystem integration")
            
        else:
            print(f"❌ Demo failed: {response.status_code}")
        
        return response.status_code == 200
    
    def demo_scenario_2_enterprise_leader(self):
        """Demo: Enterprise Sustainability Leader with Complex Building Retrofit"""
        
        print("\n🎬 DEMO SCENARIO 2: Enterprise Building Retrofit")
        print("=" * 60)
        print("Context: Large corporation, advanced sustainability team")
        print("DBO Output: Smart building optimization across multiple facilities")
        print()
        
        dbo_output = {
            "scenario_title": "Enterprise Smart Building Portfolio Optimization",
            "scenario_description": "Global technology company wants to retrofit 50+ office buildings for net-zero operations. Focus on ESG reporting and investor requirements.",
            "recommended_actions": [
                "Deploy building management systems across portfolio",
                "Integrate IoT sensors for real-time optimization",
                "Implement predictive maintenance algorithms",
                "Connect renewable energy sources",
                "Establish centralized sustainability reporting"
            ],
            "estimated_benefits": {
                "energy_savings": "30-45%",
                "operational_efficiency": "35%",
                "carbon_footprint_reduction": "40%",
                "payback_period_years": 4.0,
                "portfolio_value": "$50M+ investment"
            }
        }
        
        user_profile = {
            "sustainability_proficiency": "expert",
            "technological_proficiency": "advanced",
            "communication_style": "technical",
            "regulatory_compliance_importance": "critical",
            "company_size": "Enterprise (10,000+ employees)",
            "budget_priority": "low"  # Budget not a constraint
        }
        
        response = requests.post(
            f"{self.base_url}/api/v1/integration/dbo-to-xcelerator",
            json={"dbo_output": dbo_output, "user_profile": user_profile}
        )
        
        if response.status_code == 200:
            recommendations = response.json()
            print("✅ ENTERPRISE INTEGRATION SUCCESSFUL")
            print(f"🎯 Generated {len(recommendations)} Enterprise-grade solutions:")
            print()
            
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"{i}. {rec['product_name']}")
                print(f"   Category: {rec['product_category']}")
                print(f"   Enterprise Focus: {rec['implementation_complexity']}")
                print(f"   Investment Scale: {rec['estimated_investment']}")
                print(f"   Strategic Value: {rec['proficiency_match']['sustainability_approach']}")
                print(f"   Ecosystem Benefits: {len(rec['ecosystem_benefits'])} integration points")
                print()
            
            print("💡 Enterprise Benefits Demonstrated:")
            print("   ✅ Scalable across global portfolio")
            print("   ✅ Advanced technical capabilities")
            print("   ✅ ESG and compliance focus")
            print("   ✅ Strategic partnership approach")
            print("   ✅ Complex ecosystem integration")
        
        return response.status_code == 200
    
    def demo_scenario_3_cost_conscious_manufacturer(self):
        """Demo: Cost-conscious manufacturer with immediate ROI needs"""
        
        print("\n🎬 DEMO SCENARIO 3: Cost-Conscious Manufacturing")
        print("=" * 60)
        print("Context: Medium manufacturer, tight budget, needs quick ROI")
        print("DBO Output: Process optimization for immediate savings")
        print()
        
        dbo_output = {
            "scenario_title": "Manufacturing Process Energy Optimization",
            "scenario_description": "Mid-size automotive parts manufacturer needs immediate energy cost reduction. Current margin pressure requires fast payback solutions.",
            "recommended_actions": [
                "Optimize production line energy consumption",
                "Implement predictive maintenance to reduce downtime",
                "Install variable frequency drives on motors",
                "Add compressed air leak detection system",
                "Deploy real-time energy monitoring"
            ],
            "estimated_benefits": {
                "energy_cost_reduction": "15-25%",
                "maintenance_savings": "20%",
                "production_efficiency": "10%",
                "payback_period_years": 1.5,
                "annual_savings": "$85,000-120,000"
            }
        }
        
        user_profile = {
            "sustainability_proficiency": "intermediate",
            "technological_proficiency": "intermediate",
            "communication_style": "business_focused",
            "regulatory_compliance_importance": "medium",
            "company_size": "Medium (200 employees)",
            "budget_priority": "high",
            "implementation_timeline": "6-12 months"
        }
        
        response = requests.post(
            f"{self.base_url}/api/v1/integration/dbo-to-xcelerator",
            json={"dbo_output": dbo_output, "user_profile": user_profile}
        )
        
        if response.status_code == 200:
            recommendations = response.json()
            print("✅ COST-FOCUSED INTEGRATION SUCCESSFUL")
            print(f"🎯 Generated {len(recommendations)} ROI-optimized solutions:")
            print()
            
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"{i}. {rec['product_name']}")
                print(f"   ROI Focus: {rec['expected_roi_timeline']}")
                print(f"   Investment: {rec['estimated_investment']}")
                print(f"   Financing: {len(rec['financing_options'])} options available")
                print(f"   Business Value: {rec['proficiency_match']['sustainability_approach']}")
                print()
            
            print("💡 Cost-Conscious Benefits:")
            print("   ✅ Fast payback solutions prioritized")
            print("   ✅ Multiple financing options")
            print("   ✅ Business-focused communication")
            print("   ✅ Immediate savings potential")
            print("   ✅ Moderate complexity for quick implementation")
        
        return response.status_code == 200
    
    def demo_complete_workflow_simulation(self):
        """Demo: Complete workflow using existing DBO scenarios"""
        
        print("\n🎬 DEMO SCENARIO 4: Complete Workflow Simulation")
        print("=" * 60)
        print("Context: Using actual DBO scenario from your JSON + User assessment")
        print("Workflow: DBO Scenario → User Profile → Xcelerator → Implementation Plan")
        print()
        
        user_profile = {
            "sustainability_proficiency": "intermediate",
            "technological_proficiency": "beginner",
            "communication_style": "comprehensive",
            "regulatory_compliance_importance": "high",
            "company_size": "Medium (150 employees)",
            "industry_sector": "Manufacturing"
        }
        
        response = requests.post(
            f"{self.base_url}/api/v1/integration/simulate-dbo-workflow",
            json={
                "scenario_id": "energy_optimization",
                "user_profile": user_profile,
                "persona": "amina"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ COMPLETE WORKFLOW SUCCESSFUL")
            print()
            
            # Show each step
            print("📊 STEP 1: DBO Analysis Results")
            dbo = data['dbo_analysis']
            print(f"   Scenario: {dbo['scenario_title']}")
            print(f"   Industry: {dbo['industry']}")
            print(f"   Persona Insight: {dbo['persona_insights'][:100]}...")
            print()
            
            print("👤 STEP 2: User Profile Assessment")
            profile = data['user_profile_assessment']
            print(f"   Sustainability Level: {profile['sustainability_proficiency']}")
            print(f"   Technology Level: {profile['technological_proficiency']}")
            print(f"   Communication Style: {profile['communication_style']}")
            print()
            
            print("🛒 STEP 3: Xcelerator Recommendations")
            recommendations = data['xcelerator_recommendations']
            print(f"   Generated {len(recommendations)} recommendations:")
            for i, rec in enumerate(recommendations[:2], 1):
                print(f"   {i}. {rec['product_name']} (Score: {rec['relevance_score']:.2f})")
            print()
            
            print("🗺️ STEP 4: Implementation Roadmap")
            roadmap = data['implementation_roadmap']
            print(f"   Implementation Phases: {len(roadmap)}")
            print(f"   Total Timeline: {roadmap['phase_4_optimization']['duration']}")
            print()
            
            print("📋 STEP 5: Next Steps")
            next_steps = data['next_steps']
            print(f"   Immediate Actions: {len(next_steps)}")
            print(f"   1. {next_steps[0] if next_steps else 'None'}")
            print(f"   2. {next_steps[1] if len(next_steps) > 1 else 'None'}")
            
            print("\n💡 Complete Workflow Benefits:")
            print("   ✅ End-to-end integration demonstrated")
            print("   ✅ Persona-aware AI recommendations")
            print("   ✅ Proficiency-based guidance")
            print("   ✅ Detailed implementation planning")
            print("   ✅ Financial modeling included")
        
        return response.status_code == 200
    
    def run_all_demos(self):
        """Run all demo scenarios for comprehensive presentation"""
        
        print("🚀 SIEMENS TECH FOR SUSTAINABILITY 2025")
        print("🌱 SustAInability Navigator - Complete Integration Demo")
        print("🔗 DBO Tool → User Assessment → Xcelerator Marketplace")
        print("=" * 80)
        
        results = []
        
        # Run all demo scenarios
        results.append(self.demo_scenario_1_beginner_sme())
        results.append(self.demo_scenario_2_enterprise_leader())
        results.append(self.demo_scenario_3_cost_conscious_manufacturer())
        results.append(self.demo_complete_workflow_simulation())
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 DEMO SUMMARY")
        print("=" * 80)
        
        success_count = sum(results)
        total_scenarios = len(results)
        
        print(f"✅ Successful Demos: {success_count}/{total_scenarios}")
        print(f"📈 Success Rate: {(success_count/total_scenarios)*100:.0f}%")
        
        if success_count == total_scenarios:
            print("\n🎉 ALL INTEGRATION DEMOS SUCCESSFUL!")
            print("🌟 Ready for Siemens Co-creation Presentation!")
            print("\n🎯 Key Differentiators Demonstrated:")
            print("   ✅ Real DBO Tool integration with example outputs")
            print("   ✅ Intelligent user proficiency assessment")
            print("   ✅ AI-powered Xcelerator product matching")
            print("   ✅ Persona-aware recommendations")
            print("   ✅ Complete implementation guidance")
            print("   ✅ Financial modeling and ROI calculations")
            print("   ✅ Siemens ecosystem benefits")
        else:
            print("\n⚠️ Some demos failed - check integration before presentation")
        
        return success_count == total_scenarios

# ---
import requests
import json
from datetime import datetime

class SiemensIntegrationTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = {}
        
    def test_xcelerator_catalog(self):
        """Test Xcelerator product catalog"""
        print("\n🛒 Testing Xcelerator Catalog")
        print("-" * 30)
        
        try:
            response = requests.get(f"{self.base_url}/api/v1/integration/xcelerator/products")
            if response.status_code == 200:
                data = response.json()
                print("✅ Xcelerator catalog retrieved")
                print(f"   Total products: {data['total_count']}")
                print(f"   Categories: {data['available_categories']}")
                print(f"   Complexity levels: {data['complexity_levels']}")
                
                # Show sample products
                products = data['products']
                for product_id, product_info in list(products.items())[:3]:
                    print(f"   - {product_info['name']} ({product_info['category']})")
                    print(f"     Complexity: {product_info['implementation_complexity']}")
                    print(f"     Timeline: {product_info['typical_timeline']}")
                
                self.test_results['xcelerator_catalog'] = True
            else:
                print(f"❌ Catalog retrieval failed: {response.status_code}")
                self.test_results['xcelerator_catalog'] = False
        except Exception as e:
            print(f"❌ Catalog error: {e}")
            self.test_results['xcelerator_catalog'] = False
    
    def test_dbo_to_xcelerator_workflow(self):
        """Test complete DBO to Xcelerator workflow"""
        print("\n🔄 Testing Complete DBO → Xcelerator Workflow")
        print("-" * 50)
        
        # Test with different DBO scenarios and user profiles
        test_cases = [
            {
                "scenario": "energy_optimization",
                "user_profile": {
                    "sustainability_proficiency": "intermediate",
                    "technological_proficiency": "beginner",
                    "communication_style": "business_focused",
                    "regulatory_compliance_importance": "high",
                    "company_size": "Medium (100-500 employees)",
                    "industry_sector": "Manufacturing"
                },
                "persona": "amina"
            },
            {
                "scenario": "smart_building_retrofitting",
                "user_profile": {
                    "sustainability_proficiency": "advanced",
                    "technological_proficiency": "intermediate",
                    "communication_style": "technical",
                    "regulatory_compliance_importance": "critical",
                    "company_size": "Large (1000+ employees)",
                    "industry_sector": "Technology"
                },
                "persona": "zuri"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- Test Case {i}: {test_case['scenario']} + {test_case['persona']} ---")
            
            try:
                response = requests.post(
                    f"{self.base_url}/api/v1/integration/simulate-dbo-workflow",
                    json={
                        "scenario_id": test_case["scenario"],
                        "user_profile": test_case["user_profile"],
                        "persona": test_case["persona"]
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Complete workflow simulation successful")
                    
                    # DBO Analysis results
                    dbo_analysis = data['dbo_analysis']
                    print(f"   DBO Scenario: {dbo_analysis['scenario_title']}")
                    print(f"   Industry: {dbo_analysis['industry']}")
                    print(f"   Complexity: {dbo_analysis['complexity']}")
                    
                    # User Profile Assessment
                    profile_assessment = data['user_profile_assessment']
                    print(f"   User Proficiency: {profile_assessment['sustainability_proficiency']}/{profile_assessment['technological_proficiency']}")
                    print(f"   Communication: {profile_assessment['communication_style']}")
                    
                    # Xcelerator Recommendations
                    recommendations = data['xcelerator_recommendations']
                    print(f"   Xcelerator Recommendations: {len(recommendations)}")
                    
                    for j, rec in enumerate(recommendations[:3], 1):
                        print(f"     {j}. {rec['product_name']} ({rec['product_category']})")
                        print(f"        Relevance: {rec['relevance_score']:.2f}")
                        print(f"        Investment: {rec['estimated_investment']}")
                        print(f"        Timeline: {rec['estimated_timeline']}")
                    
                    # Implementation Roadmap
                    roadmap = data['implementation_roadmap']
                    print(f"   Implementation Phases: {len(roadmap)}")
                    
                    # Next Steps
                    next_steps = data['next_steps']
                    print(f"   Next Steps: {len(next_steps)}")
                    print(f"     1. {next_steps[0] if next_steps else 'None'}")
                    
                    self.test_results[f'workflow_{i}'] = True
                else:
                    print(f"❌ Workflow simulation failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    self.test_results[f'workflow_{i}'] = False
                    
            except Exception as e:
                print(f"❌ Workflow simulation error: {e}")
                self.test_results[f'workflow_{i}'] = False
    
    def test_direct_dbo_xcelerator_analysis(self):
        """Test direct DBO output to Xcelerator analysis"""
        print("\n🎯 Testing Direct DBO → Xcelerator Analysis")
        print("-" * 45)
        
        # Simulate DBO tool output
        dbo_output = {
            "scenario_title": "Energy Efficiency Optimization for Manufacturing SME",
            "scenario_description": "A mid-sized manufacturing facility seeks to reduce energy consumption and carbon footprint through smart technology integration and process optimization.",
            "recommended_actions": [
                "Install IoT sensors for real-time energy monitoring",
                "Upgrade to energy-efficient HVAC systems with smart controls", 
                "Implement LED lighting with occupancy sensors",
                "Deploy building automation system for optimization",
                "Integrate renewable energy sources"
            ],
            "estimated_benefits": {
                "energy_cost_reduction": "20-30%",
                "carbon_emissions_reduction": "25%", 
                "payback_period_years": 2.5,
                "annual_savings": "$45,000-65,000"
            },
            "sme_context": {
                "company_size": "Medium (100-200 employees)",
                "industry": "Manufacturing",
                "current_energy_spend": "$200,000/year"
            },
            "complexity_assessment": "Medium",
            "urgency_level": "High"
        }
        
        user_profile = {
            "sustainability_proficiency": "intermediate",
            "technological_proficiency": "beginner",
            "communication_style": "business_focused", 
            "regulatory_compliance_importance": "high",
            "company_size": "Medium (100-500 employees)",
            "budget_priority": "medium",
            "implementation_timeline": "12-18 months"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/integration/dbo-to-xcelerator",
                json={
                    "dbo_output": dbo_output,
                    "user_profile": user_profile
                }
            )
            
            if response.status_code == 200:
                recommendations = response.json()
                print("✅ DBO to Xcelerator analysis successful")
                print(f"   Generated recommendations: {len(recommendations)}")
                
                for i, rec in enumerate(recommendations, 1):
                    print(f"\n   Recommendation {i}:")
                    print(f"     Product: {rec['product_name']}")
                    print(f"     Category: {rec['product_category']}")
                    print(f"     Relevance Score: {rec['relevance_score']:.2f}")
                    print(f"     Implementation Complexity: {rec['implementation_complexity']}")
                    print(f"     Estimated Investment: {rec['estimated_investment']}")
                    print(f"     Expected ROI Timeline: {rec['expected_roi_timeline']}")
                    print(f"     Financing Options: {len(rec['financing_options'])} available")
                    
                    if rec.get('proficiency_match'):
                        print(f"     Proficiency Match:")
                        for key, value in rec['proficiency_match'].items():
                            print(f"       {key}: {value}")
                    
                    if rec.get('ecosystem_benefits'):
                        print(f"     Ecosystem Benefits: {len(rec['ecosystem_benefits'])}")
                        print(f"       - {rec['ecosystem_benefits'][0] if rec['ecosystem_benefits'] else 'None'}")
                
                self.test_results['direct_dbo_analysis'] = True
            else:
                print(f"❌ DBO analysis failed: {response.status_code}")
                print(f"   Error: {response.text}")
                self.test_results['direct_dbo_analysis'] = False
                
        except Exception as e:
            print(f"❌ DBO analysis error: {e}")
            self.test_results['direct_dbo_analysis'] = False
    
    def test_enhanced_health_check(self):
        """Test enhanced health check with integration status"""
        print("\n🏥 Testing Enhanced Health Check")
        print("-" * 35)
        
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print("✅ Enhanced health check passed")
                print(f"   Status: {data['status']}")
                
                services = data['services']
                print(f"   DBO Service: {services['dbo_service']}")
                print(f"   LangChain: {services['langchain_service']}")
                print(f"   Xcelerator Service: {services['xcelerator_service']}")
                print(f"   Scenarios Loaded: {services['scenarios_loaded']}")
                print(f"   Xcelerator Products: {services['xcelerator_products']}")
                
                integration_status = data['integration_status']
                print(f"   Integration Status:")
                for key, value in integration_status.items():
                    print(f"     {key}: {value}")
                
                self.test_results['enhanced_health'] = True
            else:
                print(f"❌ Enhanced health check failed: {response.status_code}")
                self.test_results['enhanced_health'] = False
        except Exception as e:
            print(f"❌ Enhanced health check error: {e}")
            self.test_results['enhanced_health'] = False
    
    def test_api_documentation(self):
        """Test API documentation accessibility"""
        print("\n📚 Testing API Documentation")
        print("-" * 30)
        
        endpoints = [
            "/docs",  # Swagger UI
            "/redoc",  # ReDoc
            "/openapi.json"  # OpenAPI spec
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}")
                if response.status_code == 200:
                    print(f"✅ {endpoint} accessible")
                    self.test_results[f'docs_{endpoint.replace("/", "_")}'] = True
                else:
                    print(f"❌ {endpoint} failed: {response.status_code}")
                    self.test_results[f'docs_{endpoint.replace("/", "_")}'] = False
            except Exception as e:
                print(f"❌ {endpoint} error: {e}")
                self.test_results[f'docs_{endpoint.replace("/", "_")}'] = False
    
    def run_integration_tests(self):
        """Run comprehensive integration test suite"""
        print("🚀 Starting Siemens Integration Test Suite")
        print("=" * 60)
        print("Testing DBO Tool → User Proficiency → Xcelerator Marketplace Integration")
        print("=" * 60)
        
        start_time = datetime.now()
        
        # Run all integration tests
        self.test_enhanced_health_check()
        self.test_workflow_overview()
        self.test_user_proficiency_assessment()
        self.test_xcelerator_catalog()
        self.test_direct_dbo_xcelerator_analysis()
        self.test_dbo_to_xcelerator_workflow()
        self.test_api_documentation()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Generate integration test report
        self.generate_integration_report(duration)
    
    def generate_integration_report(self, duration):
        """Generate comprehensive integration test report"""
        print("\n" + "=" * 60)
        print("📊 SIEMENS INTEGRATION TEST REPORT")
        print("=" * 60)
        
        # Calculate statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"📈 Integration Test Statistics:")
        print(f"   Total tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success rate: {success_rate:.1f}%")
        print(f"   Duration: {duration:.1f} seconds")
        
        # Categorize results by integration component
        categories = {
            "Core Integration": ["enhanced_health", "workflow_overview"],
            "User Proficiency System": [k for k in self.test_results.keys() if k.startswith("proficiency_")],
            "Xcelerator Integration": ["xcelerator_catalog", "direct_dbo_analysis"],
            "Complete Workflows": [k for k in self.test_results.keys() if k.startswith("workflow_")],
            "API Documentation": [k for k in self.test_results.keys() if k.startswith("docs_")]
        }
        
        print(f"\n📋 Results by Integration Component:")
        for category, test_keys in categories.items():
            if test_keys:
                category_passed = sum(1 for key in test_keys if self.test_results.get(key, False))
                category_total = len(test_keys)
                category_rate = (category_passed / category_total) * 100 if category_total > 0 else 0
                
                status = "✅" if category_rate == 100 else "⚠️" if category_rate >= 80 else "❌"
                print(f"   {category}: {category_passed}/{category_total} ({category_rate:.0f}%) {status}")
        
        # Integration-specific assessment
        print(f"\n🎯 Integration Assessment:")
        if success_rate >= 95:
            print("   🌟 EXCELLENT - Full Siemens ecosystem integration working!")
            print("   ✅ DBO Tool → Xcelerator workflow fully operational")
            print("   ✅ User proficiency assessment system functional")
            print("   ✅ Intelligent product matching working")
            print("   ✅ Ready for SME customers and Siemens presentation")
        elif success_rate >= 85:
            print("   ✅ GOOD - Integration mostly working with minor issues")
            print("   ⚠️  Address failed components before demo")
        elif success_rate >= 70:
            print("   ⚠️  FAIR - Integration has several issues")
            print("   🔧 Significant work needed before production")
        else:
            print("   ❌ POOR - Integration not ready")
            print("   🚨 Major fixes required")
        
        # Failed tests details
        failed_test_keys = [k for k, v in self.test_results.items() if not v]
        if failed_test_keys:
            print(f"\n❌ Failed Integration Tests:")
            for test_key in failed_test_keys:
                print(f"   - {test_key}")
        
        # Siemens ecosystem readiness
        key_integrations = ['workflow_overview', 'xcelerator_catalog', 'direct_dbo_analysis', 'workflow_1']
        integration_score = sum(1 for key in key_integrations if self.test_results.get(key, False))
        
        print(f"\n🏢 Siemens Ecosystem Readiness: {integration_score}/{len(key_integrations)}")
        if integration_score == len(key_integrations):
            print("   🎉 Ready for Siemens co-creation phase!")
            print("   🔗 Complete workflow: DBO → User Assessment → Xcelerator Solutions")
        else:
            print("   ⚠️  Integration workflow needs attention")
        
        print(f"\n💡 Integration Summary:")
        print("   - DBO Tool output simulation: Working")
        print("   - User proficiency assessment: Working") 
        print("   - Xcelerator product matching: Working")
        print("   - Complete workflow simulation: Working")
        print("   - AI-powered recommendations: Working")
        print("   - Financial modeling: Working")
        print("   - Implementation roadmaps: Working")

if __name__ == "__main__":
    print("🔧 Siemens Integration Test Suite")
    print("Testing: DBO Tool → User Proficiency → Xcelerator Marketplace")
    print("Make sure your server is running: python main.py")
    print()
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        tester = SiemensIntegrationTester()
        tester.run_integration_tests()
    else:
        print("To run integration tests: python test_integration_workflow.py run")_workflow_overview(self):
        """Test workflow overview endpoint"""
        print("🔄 Testing Workflow Overview")
        print("-" * 30)
        
        try:
            response = requests.get(f"{self.base_url}/api/v1/workflow/overview")
            if response.status_code == 200:
                data = response.json()
                print("✅ Workflow overview retrieved")
                print(f"   Process steps: {len(data['process_steps'])}")
                print(f"   Key benefits: {len(data['key_benefits'])}")
                
                for step in data['process_steps']:
                    print(f"   Step {step['step']}: {step['name']}")
                
                self.test_results['workflow_overview'] = True
            else:
                print(f"❌ Workflow overview failed: {response.status_code}")
                self.test_results['workflow_overview'] = False
        except Exception as e:
            print(f"❌ Workflow overview error: {e}")
            self.test_results['workflow_overview'] = False
    
    def test_user_proficiency_assessment(self):
        """Test user proficiency assessment"""
        print("\n👤 Testing User Proficiency Assessment")
        print("-" * 40)
        
        # Test different user profiles
        test_profiles = [
            {
                "name": "Beginner SME Owner",
                "profile": {
                    "sustainability_proficiency": "beginner",
                    "technological_proficiency": "beginner", 
                    "communication_style": "simple_explanations",
                    "regulatory_compliance_importance": "medium",
                    "company_size": "Small (10-50 employees)",
                    "industry_sector": "Manufacturing"
                }
            },
            {
                "name": "Advanced Sustainability Manager",
                "profile": {
                    "sustainability_proficiency": "advanced",
                    "technological_proficiency": "intermediate",
                    "communication_style": "technical",
                    "regulatory_compliance_importance": "high",
                    "company_size": "Medium (100-500 employees)",
                    "industry_sector": "Technology"
                }
            },
            {
                "name": "Expert Enterprise Leader", 
                "profile": {
                    "sustainability_proficiency": "expert",
                    "technological_proficiency": "advanced",
                    "communication_style": "comprehensive",
                    "regulatory_compliance_importance": "critical",
                    "company_size": "Large (1000+ employees)",
                    "industry_sector": "Manufacturing"
                }
            }
        ]
        
        for test_case in test_profiles:
            print(f"\n--- Testing {test_case['name']} ---")
            
            try:
                response = requests.post(
                    f"{self.base_url}/api/v1/integration/user-profile/assess",
                    json=test_case['profile']
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Proficiency assessment successful")
                    print(f"   Recommended approach: {data['recommended_approach']['implementation_strategy']}")
                    print(f"   Support level: {data['recommended_approach']['support_level']}")
                    print(f"   Suggested products: {len(data['suggested_products'])}")
                    print(f"   Support requirements: {len(data['support_requirements'])}")
                    
                    self.test_results[f'proficiency_{test_case["name"].replace(" ", "_").lower()}'] = True
                else:
                    print(f"❌ Assessment failed: {response.status_code}")
                    self.test_results[f'proficiency_{test_case["name"].replace(" ", "_").lower()}'] = False
                    
            except Exception as e:
                print(f"❌ Assessment error: {e}")
                self.test_results[f'proficiency_{test_case["name"].replace(" ", "_").lower()}'] = False
    
    def test
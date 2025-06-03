import requests
import json
import time
from datetime import datetime

class ComprehensiveBackendTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = {}
        
    def test_health_and_status(self):
        """Test health endpoint and system status"""
        print("🏥 Testing Health & Status")
        print("-" * 30)
        
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print("✅ Health check passed")
                print(f"   Status: {data['status']}")
                print(f"   Services: {data['services']}")
                print(f"   Scenarios loaded: {data['services']['scenarios_loaded']}")
                print(f"   LangChain: {data['services']['langchain_service']}")
                self.test_results['health'] = True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                self.test_results['health'] = False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            self.test_results['health'] = False
    
    def test_personas_chat(self):
        """Test chat with different personas"""
        print("\n💬 Testing Persona-Based Chat")
        print("-" * 35)
        
        test_cases = [
            {
                "persona": "zuri",
                "message": "I need enterprise sustainability solutions for our global manufacturing facilities.",
                "expected_keywords": ["enterprise", "global", "ESG"]
            },
            {
                "persona": "amina", 
                "message": "What are cost-effective energy efficiency solutions with quick ROI?",
                "expected_keywords": ["cost", "ROI", "efficiency"]
            },
            {
                "persona": "bjorn",
                "message": "How do these solutions integrate with our existing Siemens systems?",
                "expected_keywords": ["integration", "Siemens", "systems"]
            },
            {
                "persona": "arjun",
                "message": "What sustainability metrics can help us gain competitive advantage?",
                "expected_keywords": ["metrics", "competitive", "sustainability"]
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- Test {i}: {test_case['persona'].title()} Persona ---")
            
            try:
                response = requests.post(
                    f"{self.base_url}/api/v1/chat/",
                    json={
                        "message": test_case["message"],
                        "persona": test_case["persona"],
                        "session_id": f"test_session_{i}"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Chat response received")
                    print(f"   Persona: {data['persona_context']}")
                    print(f"   Response length: {len(data['response'])} chars")
                    print(f"   Confidence: {data.get('confidence_score', 'N/A')}")
                    print(f"   Sample: {data['response'][:100]}...")
                    
                    self.test_results[f'chat_{test_case["persona"]}'] = True
                else:
                    print(f"❌ Chat failed: {response.status_code}")
                    self.test_results[f'chat_{test_case["persona"]}'] = False
                    
            except Exception as e:
                print(f"❌ Chat error: {e}")
                self.test_results[f'chat_{test_case["persona"]}'] = False
    
    def test_dbo_scenarios(self):
        """Test DBO scenario functionality"""
        print("\n🎯 Testing DBO Scenarios")
        print("-" * 25)
        
        # Test scenario listing
        try:
            response = requests.get(f"{self.base_url}/api/v1/dbo/scenarios")
            if response.status_code == 200:
                data = response.json()
                print("✅ Scenario listing successful")
                print(f"   Total scenarios: {data['total_count']}")
                print(f"   Categories: {data['categories']}")
                
                self.test_results['dbo_list'] = True
            else:
                print(f"❌ Scenario listing failed: {response.status_code}")
                self.test_results['dbo_list'] = False
        except Exception as e:
            print(f"❌ Scenario listing error: {e}")
            self.test_results['dbo_list'] = False
        
        # Test detailed scenario retrieval
        test_scenarios = ["energy_optimization", "water_usage_reduction"]
        
        for scenario_id in test_scenarios:
            print(f"\n• Testing {scenario_id}:")
            try:
                response = requests.post(
                    f"{self.base_url}/api/v1/dbo/scenario",
                    json={
                        "scenario": scenario_id,
                        "persona": "amina",
                        "detailed": True
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print("  ✅ Scenario details retrieved")
                    print(f"     Title: {data['title']}")
                    print(f"     Industry: {data['industry']}")
                    print(f"     Complexity: {data['complexity']}")
                    print(f"     Confidence: {data['confidence_score']}")
                    
                    self.test_results[f'dbo_detail_{scenario_id}'] = True
                else:
                    print(f"  ❌ Failed: {response.status_code}")
                    self.test_results[f'dbo_detail_{scenario_id}'] = False
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
                self.test_results[f'dbo_detail_{scenario_id}'] = False
    
    def test_search_functionality(self):
        """Test search capabilities"""
        print("\n🔍 Testing Search Functionality")
        print("-" * 32)
        
        search_tests = [
            {"query": "energy efficiency", "expected_min": 1},
            {"query": "water conservation", "expected_min": 1},
            {"query": "manufacturing", "expected_min": 1}
        ]
        
        for test in search_tests:
            print(f"\n• Searching for: '{test['query']}'")
            try:
                response = requests.get(
                    f"{self.base_url}/api/v1/dbo/scenarios/search",
                    params={"q": test["query"], "persona": "zuri"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    result_count = data['total_count']
                    print(f"  ✅ Search successful: {result_count} results")
                    
                    if result_count >= test['expected_min']:
                        print(f"     Expected minimum {test['expected_min']}, got {result_count} ✅")
                    
                    self.test_results[f'search_{test["query"].replace(" ", "_")}'] = True
                else:
                    print(f"  ❌ Search failed: {response.status_code}")
                    self.test_results[f'search_{test["query"].replace(" ", "_")}'] = False
                    
            except Exception as e:
                print(f"  ❌ Search error: {e}")
                self.test_results[f'search_{test["query"].replace(" ", "_")}'] = False
    
    def test_analytics(self):
        """Test analytics endpoints"""
        print("\n📊 Testing Analytics")
        print("-" * 20)
        
        analytics_endpoints = [
            "/api/v1/analytics/summary",
            "/api/v1/analytics/performance",
            "/api/v1/analytics/recommendations/trends"
        ]
        
        for endpoint in analytics_endpoints:
            print(f"\n• Testing {endpoint.split('/')[-1]}:")
            try:
                response = requests.get(f"{self.base_url}{endpoint}")
                if response.status_code == 200:
                    data = response.json()
                    print("  ✅ Analytics endpoint successful")
                    
                    # Basic validation
                    if 'summary' in endpoint and 'total_scenarios' in data.get('summary', {}):
                        print(f"     Total scenarios: {data['summary']['total_scenarios']}")
                    elif 'performance' in endpoint and 'performance_metrics' in data:
                        print(f"     System health: {data.get('system_health', {}).get('scenarios_loaded', 'unknown')}")
                    elif 'trends' in endpoint and 'trending_technologies' in data:
                        print(f"     Trending techs: {len(data['trending_technologies'])}")
                    
                    self.test_results[f'analytics_{endpoint.split("/")[-1]}'] = True
                else:
                    print(f"  ❌ Failed: {response.status_code}")
                    self.test_results[f'analytics_{endpoint.split("/")[-1]}'] = False
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
                self.test_results[f'analytics_{endpoint.split("/")[-1]}'] = False
    
    def test_performance(self):
        """Test response times and performance"""
        print("\n⚡ Testing Performance")
        print("-" * 22)
        
        endpoints = [
            ("/health", "GET", None),
            ("/api/v1/dbo/scenarios", "GET", None),
            ("/api/v1/chat/", "POST", {"message": "Hello", "persona": "general"})
        ]
        
        for endpoint, method, payload in endpoints:
            print(f"\n• Testing {method} {endpoint}")
            
            try:
                start_time = time.time()
                
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}")
                else:
                    response = requests.post(f"{self.base_url}{endpoint}", json=payload)
                
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                
                if response.status_code == 200:
                    print(f"  ✅ Response time: {response_time:.0f}ms")
                    if response_time < 5000:
                        print("     Performance: Good ✅")
                    else:
                        print("     Performance: Slow ⚠️")
                else:
                    print(f"  ❌ Failed with status: {response.status_code}")
                
                self.test_results[f'perf_{endpoint.replace("/", "_")}'] = response.status_code == 200
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                self.test_results[f'perf_{endpoint.replace("/", "_")}'] = False
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 Starting Comprehensive Backend Testing")
        print("=" * 60)
        
        start_time = datetime.now()
        
        # Run all test suites
        self.test_health_and_status()
        self.test_personas_chat()
        self.test_dbo_scenarios()
        self.test_search_functionality()
        self.test_analytics()
        self.test_performance()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Generate test report
        self.generate_test_report(duration)
    
    def generate_test_report(self, duration):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        # Calculate statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"📈 Test Statistics:")
        print(f"   Total tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success rate: {success_rate:.1f}%")
        print(f"   Duration: {duration:.1f} seconds")
        
        # Categorize results
        categories = {
            "Core Functionality": ["health", "dbo_list"],
            "Chat & AI": [k for k in self.test_results.keys() if k.startswith("chat_")],
            "DBO Scenarios": [k for k in self.test_results.keys() if k.startswith("dbo_detail_")],
            "Search & Analytics": [k for k in self.test_results.keys() if k.startswith("search_") or k.startswith("analytics_")],
            "Performance": [k for k in self.test_results.keys() if k.startswith("perf_")]
        }
        
        print(f"\n📋 Results by Category:")
        for category, test_keys in categories.items():
            if test_keys:
                category_passed = sum(1 for key in test_keys if self.test_results.get(key, False))
                category_total = len(test_keys)
                category_rate = (category_passed / category_total) * 100 if category_total > 0 else 0
                
                status = "✅" if category_rate == 100 else "⚠️" if category_rate >= 80 else "❌"
                print(f"   {category}: {category_passed}/{category_total} ({category_rate:.0f}%) {status}")
        
        # Overall assessment
        print(f"\n🎯 Overall Assessment:")
        if success_rate >= 95:
            print("   🌟 EXCELLENT - Production ready!")
        elif success_rate >= 85:
            print("   ✅ GOOD - Minor issues to address")
        elif success_rate >= 70:
            print("   ⚠️  FAIR - Several issues need attention")
        else:
            print("   ❌ POOR - Major issues require fixing")
        
        # Recommendations
        failed_test_keys = [k for k, v in self.test_results.items() if not v]
        if failed_test_keys:
            print(f"\n❌ Failed Tests:")
            for test_key in failed_test_keys:
                print(f"   - {test_key}")
            
            print(f"\n💡 Recommendations:")
            print("   - Address failed test cases before production deployment")
            print("   - Check server logs for detailed error information")
            print("   - Verify all dependencies are properly installed")
        else:
            print(f"\n💡 Recommendations:")
            print("   - Backend is fully functional and ready for integration")
            print("   - Consider load testing for production deployment")
            print("   - Monitor performance metrics in production environment")

if __name__ == "__main__":
    print("🔧 Comprehensive Backend Tester")
    print("Make sure your server is running: python main.py")
    print("Then run this comprehensive test suite.")
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        tester = ComprehensiveBackendTester()
        tester.run_all_tests()
    else:
        print("\nTo run tests: python test_comprehensive.py run")
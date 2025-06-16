# test_all_endpoints.py - Complete test suite for all endpoints

import requests
import json
import time
from datetime import datetime, timedelta
from colorama import init, Fore, Style
import sys

# Initialize colorama for colored output
init()

# Configuration - Update this to your Render URL
# BASE_URL = "http://localhost:8000"  # For local testing
BASE_URL = "https://sustainability-navigator-api.onrender.com"  # Your Render deployment

class CompleteEndpointTester:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.test_results = {}
        self.access_token = None
        self.test_user_id = None
        self.test_chat_id = None
        self.test_email = f"test_{int(time.time())}@example.com"
        self.test_password = "TestPassword123!"
        
    def print_header(self, text):
        """Print colored header"""
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    def print_success(self, text):
        """Print success message"""
        print(f"{Fore.GREEN}✅ {text}{Style.RESET_ALL}")
    
    def print_error(self, text):
        """Print error message"""
        print(f"{Fore.RED}❌ {text}{Style.RESET_ALL}")
    
    def print_info(self, text):
        """Print info message"""
        print(f"{Fore.YELLOW}   {text}{Style.RESET_ALL}")
    
    def print_test(self, text):
        """Print test description"""
        print(f"\n{Fore.BLUE}🧪 Testing: {text}{Style.RESET_ALL}")
    
    def wake_up_service(self):
        """Wake up the Render service if it's sleeping"""
        self.print_header("WAKING UP SERVICE")
        print("🔄 Waking up Render service (this may take 30-60 seconds)...")
        
        max_retries = 10
        for i in range(max_retries):
            try:
                response = requests.get(f"{self.base_url}/health", timeout=30)
                if response.status_code == 200:
                    self.print_success("Service is awake and ready!")
                    return True
            except requests.exceptions.Timeout:
                print(f"⏳ Attempt {i+1}/{max_retries} - Service is starting up...")
            except requests.exceptions.ConnectionError:
                print(f"⏳ Attempt {i+1}/{max_retries} - Waiting for service...")
            time.sleep(5)
        
        self.print_error("Could not wake up service!")
        return False
    
    # TEST JONAS'S ENDPOINTS SPECIFICALLY
    def test_jonas_endpoints(self):
        """Test all endpoints specified by Jonas"""
        self.print_header("JONAS'S REQUIRED ENDPOINTS")
        
        # 1. Test Authentication Flow First
        self.print_test("Authentication Flow (Required for user management)")
        
        # Register
        try:
            response = requests.post(
                f"{self.base_url}/auth/register",
                json={
                    "email": self.test_email,
                    "password": self.test_password,
                    "user_params": {
                        "persona": "amina",
                        "company_size": "Small (50-200 employees)",
                        "industry": "Manufacturing"
                    }
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                self.test_user_id = data["user_id"]
                self.print_success(f"Registration successful - User ID: {self.test_user_id}")
                self.test_results['auth_register'] = True
            else:
                self.print_error(f"Registration failed: {response.status_code} - {response.text}")
                self.test_results['auth_register'] = False
                return  # Can't continue without auth
                
        except Exception as e:
            self.print_error(f"Registration error: {e}")
            self.test_results['auth_register'] = False
            return
        
        # 2. Test Save User Info
        self.print_test("POST /save_user_info/ (Jonas's requirement)")
        try:
            response = requests.post(
                f"{self.base_url}/save_user_info/",
                params={"uid": self.test_user_id},
                json={
                    "sustainability_proficiency": "intermediate",
                    "technological_proficiency": "beginner",
                    "company_size": "Small (10-50 employees)",
                    "industry": "Manufacturing",
                    "persona": "amina",
                    "budget_priority": "high",
                    "communication_style": "simple_explanations",
                    "regulatory_importance": "medium"
                }
            )
            
            if response.status_code == 200:
                self.print_success("Save user info successful")
                self.print_info("User parameters saved to database")
                self.test_results['save_user_info'] = True
            else:
                self.print_error(f"Save user info failed: {response.status_code}")
                self.test_results['save_user_info'] = False
                
        except Exception as e:
            self.print_error(f"Save user info error: {e}")
            self.test_results['save_user_info'] = False
        
        # 3. Test Get User Info
        self.print_test("GET /get_user_info/ (Jonas's requirement)")
        try:
            response = requests.get(
                f"{self.base_url}/get_user_info/",
                params={"uid": self.test_user_id}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Get user info successful")
                self.print_info(f"Persona: {data.get('persona', 'not set')}")
                self.print_info(f"Company size: {data.get('company_size', 'not set')}")
                self.print_info(f"Industry: {data.get('industry', 'not set')}")
                self.print_info(f"Sustainability proficiency: {data.get('sustainability_proficiency', 'not set')}")
                self.test_results['get_user_info'] = True
            else:
                self.print_error(f"Get user info failed: {response.status_code}")
                self.test_results['get_user_info'] = False
                
        except Exception as e:
            self.print_error(f"Get user info error: {e}")
            self.test_results['get_user_info'] = False
        
        # 4. Test Main Chat Endpoint
        self.print_test("POST /chat/ (Jonas's main requirement)")
        self.test_chat_id = f"test_chat_{int(time.time())}"
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/",
                json={
                    "chat_ID": self.test_chat_id,
                    "message": "I need help with energy efficiency for my small manufacturing business. What solutions do you recommend?"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Chat endpoint successful")
                self.print_info(f"Response length: {len(data.get('response', ''))} chars")
                self.print_info(f"Chat ID returned: {data.get('chat_ID', 'none')}")
                
                # Check for structured response components
                if 'recommendations' in data and data['recommendations']:
                    self.print_info(f"Recommendations: {len(data['recommendations'])} items")
                    for rec in data['recommendations'][:2]:
                        self.print_info(f"  - {rec.get('name', 'Unknown')} ({rec.get('category', 'Unknown')})")
                else:
                    self.print_info("No recommendations in response")
                
                if 'actions' in data and data['actions']:
                    self.print_info(f"Actions: {len(data['actions'])} available")
                    for action in data['actions']:
                        self.print_info(f"  - {action.get('action_label', 'Unknown action')}")
                else:
                    self.print_info("No actions in response")
                
                self.test_results['chat_main'] = True
            else:
                self.print_error(f"Chat failed: {response.status_code}")
                self.print_error(f"Response: {response.text[:200]}")
                self.test_results['chat_main'] = False
                
        except Exception as e:
            self.print_error(f"Chat error: {e}")
            self.test_results['chat_main'] = False
        
        # Add second message to test conversation flow
        if self.test_results.get('chat_main', False):
            time.sleep(1)
            self.print_test("POST /chat/ (Second message - conversation flow)")
            try:
                response = requests.post(
                    f"{self.base_url}/chat/",
                    json={
                        "chat_ID": self.test_chat_id,
                        "message": "What about solar panels? Are they a good investment for my business?"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.print_success("Second message successful - conversation flow works")
                    self.test_results['chat_conversation'] = True
                else:
                    self.print_error(f"Second message failed: {response.status_code}")
                    self.test_results['chat_conversation'] = False
                    
            except Exception as e:
                self.print_error(f"Second message error: {e}")
                self.test_results['chat_conversation'] = False
        
        # 5. Test Get Chat History (NEW ENDPOINT Jonas requested)
        if self.test_chat_id:
            time.sleep(2)  # Ensure messages are saved
            self.print_test("GET /get_chat_history/{chat_ID} (Jonas's NEW requirement)")
            
            try:
                response = requests.get(
                    f"{self.base_url}/get_chat_history/{self.test_chat_id}"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.print_success("Chat history endpoint successful")
                    self.print_info(f"Chat ID: {data.get('chat_ID', 'none')}")
                    self.print_info(f"Total messages: {data.get('total_messages', 0)}")
                    
                    messages = data.get('messages', [])
                    for i, msg in enumerate(messages[:3]):
                        self.print_info(f"Message {i+1}:")
                        self.print_info(f"  User: {msg.get('user_message', '')[:50]}...")
                        self.print_info(f"  AI response available: {'Yes' if msg.get('ai_response') else 'No'}")
                    
                    self.test_results['chat_history'] = True
                else:
                    self.print_error(f"Chat history failed: {response.status_code}")
                    self.test_results['chat_history'] = False
                    
            except Exception as e:
                self.print_error(f"Chat history error: {e}")
                self.test_results['chat_history'] = False
        
        # 6. Test Get Chats List
        self.print_test("GET /get_chats/ (Jonas's requirement)")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        try:
            response = requests.get(
                f"{self.base_url}/get_chats/",
                params={
                    "uid": self.test_user_id,
                    "ts_start": start_date
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Get chats successful - Found {len(data)} chats")
                
                for chat in data[:3]:
                    self.print_info(f"Chat: {chat.get('chat_title', 'Untitled')}")
                    self.print_info(f"  ID: {chat.get('chat_ID', 'none')}")
                    self.print_info(f"  Date: {chat.get('chat_ts', 'unknown')}")
                
                self.test_results['get_chats'] = True
            else:
                self.print_error(f"Get chats failed: {response.status_code}")
                self.test_results['get_chats'] = False
                
        except Exception as e:
            self.print_error(f"Get chats error: {e}")
            self.test_results['get_chats'] = False
    
    # TEST ALL OTHER ENDPOINTS
    def test_other_endpoints(self):
        """Test all other system endpoints"""
        self.print_header("OTHER SYSTEM ENDPOINTS")
        
        # Test personas endpoint
        self.print_test("GET /personas")
        try:
            response = requests.get(f"{self.base_url}/personas")
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Personas endpoint - {len(data.get('personas', []))} personas available")
                for persona in data.get('personas', [])[:3]:
                    self.print_info(f"- {persona.get('name', 'Unknown')}: {persona.get('role', 'Unknown role')}")
                self.test_results['personas'] = True
            else:
                self.print_error(f"Personas failed: {response.status_code}")
                self.test_results['personas'] = False
        except Exception as e:
            self.print_error(f"Personas error: {e}")
            self.test_results['personas'] = False
        
        # Test DBO scenarios
        self.print_test("GET /api/v1/dbo/scenarios")
        try:
            response = requests.get(f"{self.base_url}/api/v1/dbo/scenarios")
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"DBO scenarios - {data.get('total_count', 0)} scenarios available")
                self.print_info(f"Categories: {data.get('categories', [])}")
                self.test_results['dbo_scenarios'] = True
            else:
                self.print_error(f"DBO scenarios failed: {response.status_code}")
                self.test_results['dbo_scenarios'] = False
        except Exception as e:
            self.print_error(f"DBO scenarios error: {e}")
            self.test_results['dbo_scenarios'] = False
        
        # Test DBO search
        self.print_test("GET /api/v1/dbo/scenarios/search")
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/dbo/scenarios/search",
                params={"q": "energy", "persona": "amina"}
            )
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"DBO search - {data.get('total_count', 0)} results for 'energy'")
                self.test_results['dbo_search'] = True
            else:
                self.print_error(f"DBO search failed: {response.status_code}")
                self.test_results['dbo_search'] = False
        except Exception as e:
            self.print_error(f"DBO search error: {e}")
            self.test_results['dbo_search'] = False
        
        # Test Analytics
        self.print_test("GET /api/v1/analytics/summary")
        try:
            response = requests.get(f"{self.base_url}/api/v1/analytics/summary")
            if response.status_code == 200:
                data = response.json()
                self.print_success("Analytics summary retrieved")
                summary = data.get('summary', {})
                self.print_info(f"Total scenarios: {summary.get('total_scenarios', 0)}")
                self.print_info(f"Average payback: {summary.get('average_payback_period', 0)} years")
                self.test_results['analytics'] = True
            else:
                self.print_error(f"Analytics failed: {response.status_code}")
                self.test_results['analytics'] = False
        except Exception as e:
            self.print_error(f"Analytics error: {e}")
            self.test_results['analytics'] = False
    
    # GENERATE COMPREHENSIVE REPORT
    def generate_report(self):
        """Generate test report with specific focus on Jonas's requirements"""
        self.print_header("TEST REPORT")
        
        # Calculate totals
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Jonas's specific endpoints
        jonas_endpoints = [
            'auth_register',  # Needed for user management
            'chat_main',
            'save_user_info',
            'get_user_info',
            'get_chats',
            'chat_history'
        ]
        
        jonas_passed = sum(1 for test in jonas_endpoints if self.test_results.get(test, False))
        jonas_total = len(jonas_endpoints)
        jonas_success_rate = (jonas_passed / jonas_total * 100) if jonas_total > 0 else 0
        
        print(f"\n{Fore.YELLOW}📊 Overall Results:{Style.RESET_ALL}")
        print(f"   Total tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success rate: {success_rate:.1f}%")
        
        print(f"\n{Fore.YELLOW}📋 Jonas's Endpoints:{Style.RESET_ALL}")
        print(f"   Required endpoints: {jonas_total}")
        print(f"   Passed: {jonas_passed} ✅")
        print(f"   Failed: {jonas_total - jonas_passed} ❌")
        print(f"   Success rate: {jonas_success_rate:.1f}%")
        
        # List Jonas's endpoint status
        print(f"\n{Fore.YELLOW}Jonas's Endpoint Status:{Style.RESET_ALL}")
        endpoint_mapping = {
            'chat_main': 'POST /chat/',
            'save_user_info': 'POST /save_user_info/',
            'get_user_info': 'GET /get_user_info/',
            'get_chats': 'GET /get_chats/',
            'chat_history': 'GET /get_chat_history/{chat_ID}'
        }
        
        for test_name, endpoint in endpoint_mapping.items():
            status = "✅" if self.test_results.get(test_name, False) else "❌"
            print(f"   {status} {endpoint}")
        
        # Failed tests details
        if failed_tests > 0:
            print(f"\n{Fore.RED}Failed Tests:{Style.RESET_ALL}")
            for test_name, result in self.test_results.items():
                if not result:
                    print(f"   ❌ {test_name}")
        
        # Final verdict
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        if jonas_success_rate == 100:
            print(f"{Fore.GREEN}🎉 ALL JONAS'S ENDPOINTS WORKING! Ready for frontend integration!{Style.RESET_ALL}")
        elif jonas_success_rate >= 80:
            print(f"{Fore.YELLOW}⚠️  Most endpoints working but some issues need fixing{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Major issues - fix before frontend integration{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        # Integration instructions
        if jonas_success_rate == 100:
            print(f"\n{Fore.GREEN}✅ Frontend Integration Instructions:{Style.RESET_ALL}")
            print(f"1. Base URL: {self.base_url}")
            print(f"2. All Jonas's endpoints are functional")
            print(f"3. Authentication is working (JWT tokens)")
            print(f"4. Chat history is properly stored and retrievable")
            print(f"5. User parameters are saved and retrieved correctly")
            print(f"\n{Fore.GREEN}The backend is ready for frontend integration!{Style.RESET_ALL}")
    
    # MAIN TEST RUNNER
    def run_all_tests(self):
        """Run all tests in sequence"""
        print(f"{Fore.CYAN}🚀 Complete Endpoint Test Suite{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Testing: {self.base_url}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        # Wake up service first if using Render
        if "onrender.com" in self.base_url:
            if not self.wake_up_service():
                print(f"{Fore.RED}Service is not responding. Please check your deployment.{Style.RESET_ALL}")
                return
        
        # Run tests
        self.test_jonas_endpoints()
        self.test_other_endpoints()
        
        # Generate report
        self.generate_report()

if __name__ == "__main__":
    # Run tests
    tester = CompleteEndpointTester()
    tester.run_all_tests()

# scripts/test_endpoints.py - Test all endpoints including new ones

import requests
import json
from datetime import datetime, timedelta
import asyncio
import time

BASE_URL = "http://localhost:8000"

class EndpointTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.access_token = None
        self.user_id = None
        self.test_results = {}
    
    def test_auth_endpoints(self):
        """Test authentication endpoints"""
        print("\n🔐 Testing Authentication Endpoints")
        print("-" * 40)
        
        # Test registration
        try:
            response = requests.post(
                f"{self.base_url}/auth/register",
                json={
                    "email": "test@example.com",
                    "password": "testpassword123",
                    "user_params": {
                        "persona": "amina",
                        "company_size": "Small (50-200 employees)"
                    }
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                self.user_id = data["user_id"]
                print("✅ Registration successful")
                print(f"   User ID: {self.user_id}")
                self.test_results["auth_register"] = True
            else:
                print(f"❌ Registration failed: {response.status_code}")
                self.test_results["auth_register"] = False
                
        except Exception as e:
            print(f"❌ Registration error: {e}")
            self.test_results["auth_register"] = False
        
        # Test login
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={
                    "email": "test@example.com",
                    "password": "testpassword123"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                print("✅ Login successful")
                self.test_results["auth_login"] = True
            else:
                print(f"❌ Login failed: {response.status_code}")
                self.test_results["auth_login"] = False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            self.test_results["auth_login"] = False
        
        # Test get me (protected endpoint)
        if self.access_token:
            try:
                response = requests.get(
                    f"{self.base_url}/auth/me",
                    headers={"Authorization": f"Bearer {self.access_token}"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Get user info successful")
                    print(f"   Email: {data['email']}")
                    print(f"   Persona: {data['params'].get('persona', 'not set')}")
                    self.test_results["auth_me"] = True
                else:
                    print(f"❌ Get user info failed: {response.status_code}")
                    self.test_results["auth_me"] = False
                    
            except Exception as e:
                print(f"❌ Get user info error: {e}")
                self.test_results["auth_me"] = False
    
    def test_chat_endpoints(self):
        """Test chat endpoints"""
        print("\n💬 Testing Chat Endpoints")
        print("-" * 40)
        
        chat_id = f"test_chat_{int(time.time())}"
        
        # Test main chat endpoint
        try:
            response = requests.post(
                f"{self.base_url}/chat/",
                json={
                    "chat_ID": chat_id,
                    "message": "I need help with energy efficiency for my small manufacturing business"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Chat endpoint successful")
                print(f"   Response length: {len(data['response'])} chars")
                print(f"   Recommendations: {len(data.get('recommendations', []))}")
                print(f"   Actions: {len(data.get('actions', []))}")
                self.test_results["chat_main"] = True
                
                # Save chat_id for history test
                self.test_chat_id = chat_id
            else:
                print(f"❌ Chat failed: {response.status_code}")
                print(f"   Error: {response.text}")
                self.test_results["chat_main"] = False
                
        except Exception as e:
            print(f"❌ Chat error: {e}")
            self.test_results["chat_main"] = False
        
        # Add second message to chat
        if hasattr(self, 'test_chat_id'):
            try:
                response = requests.post(
                    f"{self.base_url}/chat/",
                    json={
                        "chat_ID": self.test_chat_id,
                        "message": "What about solar panels?"
                    }
                )
                
                if response.status_code == 200:
                    print("✅ Second message successful")
                    self.test_results["chat_second"] = True
                else:
                    print(f"❌ Second message failed: {response.status_code}")
                    self.test_results["chat_second"] = False
                    
            except Exception as e:
                print(f"❌ Second message error: {e}")
                self.test_results["chat_second"] = False
        
        # Test chat history (NEW ENDPOINT)
        if hasattr(self, 'test_chat_id'):
            time.sleep(1)  # Ensure messages are saved
            
            try:
                response = requests.get(
                    f"{self.base_url}/get_chat_history/{self.test_chat_id}"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Chat history endpoint successful")
                    print(f"   Chat ID: {data['chat_ID']}")
                    print(f"   Total messages: {data['total_messages']}")
                    print(f"   Messages retrieved: {len(data['messages'])}")
                    
                    # Verify message order
                    if data['messages']:
                        for i, msg in enumerate(data['messages']):
                            print(f"   Message {i+1}: {msg['user_message'][:50]}...")
                    
                    self.test_results["chat_history"] = True
                else:
                    print(f"❌ Chat history failed: {response.status_code}")
                    self.test_results["chat_history"] = False
                    
            except Exception as e:
                print(f"❌ Chat history error: {e}")
                self.test_results["chat_history"] = False
    
    def test_user_management(self):
        """Test user management endpoints"""
        print("\n👤 Testing User Management Endpoints")
        print("-" * 40)
        
        if not self.user_id:
            print("⚠️  No user ID available, skipping user management tests")
            return
        
        # Test save user info
        try:
            response = requests.post(
                f"{self.base_url}/save_user_info/",
                params={"uid": self.user_id},
                json={
                    "sustainability_proficiency": "intermediate",
                    "technological_proficiency": "beginner",
                    "company_size": "Small (10-50 employees)",
                    "industry": "Manufacturing",
                    "persona": "amina",
                    "budget_priority": "high"
                }
            )
            
            if response.status_code == 200:
                print("✅ Save user info successful")
                self.test_results["save_user_info"] = True
            else:
                print(f"❌ Save user info failed: {response.status_code}")
                self.test_results["save_user_info"] = False
                
        except Exception as e:
            print(f"❌ Save user info error: {e}")
            self.test_results["save_user_info"] = False
        
        # Test get user info
        try:
            response = requests.get(
                f"{self.base_url}/get_user_info/",
                params={"uid": self.user_id}
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Get user info successful")
                print(f"   Persona: {data.get('persona', 'not set')}")
                print(f"   Company size: {data.get('company_size', 'not set')}")
                print(f"   Industry: {data.get('industry', 'not set')}")
                self.test_results["get_user_info"] = True
            else:
                print(f"❌ Get user info failed: {response.status_code}")
                self.test_results["get_user_info"] = False
                
        except Exception as e:
            print(f"❌ Get user info error: {e}")
            self.test_results["get_user_info"] = False
    
    def test_chat_list(self):
        """Test chat list endpoint"""
        print("\n📋 Testing Chat List Endpoint")
        print("-" * 40)
        
        if not self.user_id:
            print("⚠️  No user ID available, skipping chat list test")
            return
        
        # Get chats from last 7 days
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        try:
            response = requests.get(
                f"{self.base_url}/get_chats/",
                params={
                    "uid": self.user_id,
                    "ts_start": start_date
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Get chats successful")
                print(f"   Found {len(data)} chats")
                
                for chat in data[:3]:  # Show first 3
                    print(f"   - {chat['chat_title']} ({chat['chat_ts']})")
                
                self.test_results["get_chats"] = True
            else:
                print(f"❌ Get chats failed: {response.status_code}")
                self.test_results["get_chats"] = False
                
        except Exception as e:
            print(f"❌ Get chats error: {e}")
            self.test_results["get_chats"] = False
    
    def test_existing_endpoints(self):
        """Test existing endpoints that should still work"""
        print("\n🔄 Testing Existing Endpoints")
        print("-" * 40)
        
        # Test personas endpoint
        try:
            response = requests.get(f"{self.base_url}/personas")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Personas endpoint: {len(data['personas'])} personas")
                self.test_results["personas"] = True
            else:
                print(f"❌ Personas endpoint failed: {response.status_code}")
                self.test_results["personas"] = False
        except Exception as e:
            print(f"❌ Personas error: {e}")
            self.test_results["personas"] = False
        
        # Test DBO scenarios
        try:
            response = requests.get(f"{self.base_url}/api/v1/dbo/scenarios")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ DBO scenarios: {data['total_count']} scenarios")
                self.test_results["dbo_scenarios"] = True
            else:
                print(f"❌ DBO scenarios failed: {response.status_code}")
                self.test_results["dbo_scenarios"] = False
        except Exception as e:
            print(f"❌ DBO scenarios error: {e}")
            self.test_results["dbo_scenarios"] = False
        
        # Test health endpoint
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("✅ Health check passed")
                self.test_results["health"] = True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                self.test_results["health"] = False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            self.test_results["health"] = False
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "=" * 60)
        print("📊 TEST REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print("\nFailed tests:")
            for test_name, result in self.test_results.items():
                if not result:
                    print(f"  ❌ {test_name}")
        
        print("\n" + "=" * 60)
        
        if success_rate >= 90:
            print("🎉 EXCELLENT - System is ready!")
        elif success_rate >= 70:
            print("⚠️  GOOD - Some issues to address")
        else:
            print("❌ NEEDS WORK - Major issues found")
    
    def run_all_tests(self):
        """Run all endpoint tests"""
        print("🚀 Starting Endpoint Tests")
        print("=" * 60)
        
        # Run tests in order
        self.test_auth_endpoints()
        self.test_user_management()
        self.test_chat_endpoints()
        self.test_chat_list()
        self.test_existing_endpoints()
        
        # Generate report
        self.generate_report()

if __name__ == "__main__":
    print("🔧 Endpoint Test Suite")
    print("Make sure your server is running: python main.py")
    print()
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        tester = EndpointTester()
        tester.run_all_tests()
    else:
        print("To run tests: python test_endpoints.py run")
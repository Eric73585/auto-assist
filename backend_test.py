import requests
import sys
from datetime import datetime
import json

class AutoAssistAPITester:
    def __init__(self, base_url="https://6408165d-b94a-460d-a488-88c3f097cd04.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.user_data = None
        self.company_id = None
        self.car_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if not endpoint.startswith('http') else endpoint
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)

            print(f"   Status Code: {response.status_code}")
            
            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    if isinstance(response_data, list) and len(response_data) > 0:
                        print(f"   Response: Found {len(response_data)} items")
                    elif isinstance(response_data, dict):
                        print(f"   Response keys: {list(response_data.keys())}")
                    return success, response_data
                except:
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   Error: {error_detail}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timeout")
            return False, {}
        except requests.exceptions.ConnectionError:
            print(f"❌ Failed - Connection error")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test the root API endpoint"""
        return self.run_test("Root API Endpoint", "GET", "", 200)

    def test_register_user(self):
        """Test user registration"""
        timestamp = datetime.now().strftime('%H%M%S')
        test_user = {
            "username": f"testuser_{timestamp}",
            "password": "TestPass123!"
        }
        
        success, response = self.run_test(
            "User Registration",
            "POST",
            "register",
            200,
            data=test_user
        )
        
        if success:
            self.user_data = test_user
            print(f"   Registered user: {test_user['username']}")
        
        return success

    def test_login_user(self):
        """Test user login"""
        if not self.user_data:
            print("❌ Cannot test login - no user registered")
            return False
            
        success, response = self.run_test(
            "User Login",
            "POST",
            "login",
            200,
            data=self.user_data
        )
        
        if success and 'user' in response:
            print(f"   Logged in user: {response['user']['username']}")
        
        return success

    def test_get_companies(self):
        """Test getting car companies"""
        success, response = self.run_test(
            "Get Car Companies",
            "GET",
            "companies",
            200
        )
        
        if success and isinstance(response, list) and len(response) > 0:
            self.company_id = response[0]['id']
            print(f"   Found companies: {[c['name'] for c in response]}")
            print(f"   Using company ID: {self.company_id}")
        
        return success

    def test_get_cars_by_company(self):
        """Test getting cars by company"""
        if not self.company_id:
            print("❌ Cannot test cars - no company ID available")
            return False
            
        success, response = self.run_test(
            "Get Cars by Company",
            "GET",
            f"companies/{self.company_id}/cars",
            200
        )
        
        if success and isinstance(response, list) and len(response) > 0:
            self.car_id = response[0]['id']
            print(f"   Found cars: {[c['name'] for c in response]}")
            print(f"   Using car ID: {self.car_id}")
        
        return success

    def test_get_car_components(self):
        """Test getting car components"""
        if not self.car_id:
            print("❌ Cannot test components - no car ID available")
            return False
            
        success, response = self.run_test(
            "Get Car Components",
            "GET",
            f"cars/{self.car_id}/components",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found components: {[c['name'] for c in response]}")
        
        return success

    def test_get_faqs(self):
        """Test getting FAQs"""
        success, response = self.run_test(
            "Get FAQs",
            "GET",
            "faqs",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found FAQs: {len(response)} questions")
        
        return success

    def test_get_driving_guide(self):
        """Test getting driving guide"""
        success, response = self.run_test(
            "Get Driving Guide",
            "GET",
            "driving-guide",
            200
        )
        
        if success and 'steps' in response:
            print(f"   Found driving guide with {len(response['steps'])} steps")
        
        return success

    def test_get_insurance_policy(self):
        """Test getting insurance policy info"""
        success, response = self.run_test(
            "Get Insurance Policy",
            "GET",
            "insurance-policy",
            200
        )
        
        if success and 'sections' in response:
            print(f"   Found insurance info with {len(response['sections'])} sections")
        
        return success

    def test_get_contact_info(self):
        """Test getting contact information"""
        success, response = self.run_test(
            "Get Contact Info",
            "GET",
            "contact",
            200
        )
        
        if success and 'server_name' in response:
            print(f"   Contact: {response['server_name']}")
        
        return success

def main():
    print("🚀 Starting AutoAssist API Testing...")
    print("=" * 60)
    
    tester = AutoAssistAPITester()
    
    # Test sequence
    test_results = []
    
    # Basic API tests
    test_results.append(tester.test_root_endpoint())
    test_results.append(tester.test_register_user())
    test_results.append(tester.test_login_user())
    
    # Data retrieval tests
    test_results.append(tester.test_get_companies())
    test_results.append(tester.test_get_cars_by_company())
    test_results.append(tester.test_get_car_components())
    test_results.append(tester.test_get_faqs())
    test_results.append(tester.test_get_driving_guide())
    test_results.append(tester.test_get_insurance_policy())
    test_results.append(tester.test_get_contact_info())
    
    # Print final results
    print("\n" + "=" * 60)
    print("📊 FINAL TEST RESULTS")
    print("=" * 60)
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Tests Failed: {tester.tests_run - tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed! Backend API is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the details above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
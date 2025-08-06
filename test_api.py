import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_agents_list():
    """Test the agents list endpoint"""
    print("Testing agents list endpoint...")
    response = requests.get(f"{BASE_URL}/agents")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_test_strategy():
    """Test the test strategy endpoint"""
    print("Testing test strategy endpoint...")
    data = {
        "prd_text": "Build a user authentication system with login, registration, and password reset functionality."
    }
    response = requests.post(f"{BASE_URL}/test-strategy", json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Strategy generated successfully. Length: {len(result['strategy']['content'])} characters")
        print(f"First 200 characters: {result['strategy']['content'][:200]}...")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_test_plan():
    """Test the test plan endpoint"""
    print("Testing test plan endpoint...")
    data = {
        "requirements_text": "The system should allow users to create accounts, login securely, and manage their profiles."
    }
    response = requests.post(f"{BASE_URL}/test-plan", json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Test plan generated successfully. Length: {len(result['test_plan']['content'])} characters")
        print(f"First 200 characters: {result['test_plan']['content'][:200]}...")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_test_cases():
    """Test the test cases endpoint"""
    print("Testing test cases endpoint...")
    data = {
        "user_stories_text": "As a user, I want to be able to login to my account so that I can access my personal dashboard."
    }
    response = requests.post(f"{BASE_URL}/test-cases", json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Test cases generated successfully. Length: {len(result['test_cases']['content'])} characters")
        print(f"First 200 characters: {result['test_cases']['content'][:200]}...")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_bug_triage():
    """Test the bug triage endpoint"""
    print("Testing bug triage endpoint...")
    data = {
        "bug_reports_text": "Bug 1: Login page crashes when invalid email is entered. Bug 2: Password reset email not being sent."
    }
    response = requests.post(f"{BASE_URL}/bug-triage", json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Bug triage analysis generated successfully. Length: {len(result['triage_analysis']['content'])} characters")
        print(f"First 200 characters: {result['triage_analysis']['content'][:200]}...")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

if __name__ == "__main__":
    print("AI Testing Agents API Test Suite")
    print("=" * 50)
    
    # Test all endpoints
    test_health()
    test_agents_list()
    test_test_strategy()
    test_test_plan()
    test_test_cases()
    test_bug_triage()
    
    print("All tests completed!")

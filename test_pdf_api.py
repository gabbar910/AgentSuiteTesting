import requests
import json
from pathlib import Path

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_pdf_endpoint_with_sample():
    """Test the PDF endpoint with a sample PDF file"""
    print("Testing PDF test case generation endpoint...")
    
    # Create a sample PDF for testing (you would replace this with an actual PDF file)
    pdf_file_path = "sample_requirements.pdf"
    
    # Check if sample PDF exists
    if not Path(pdf_file_path).exists():
        print(f"Sample PDF file '{pdf_file_path}' not found.")
        print("Please create a sample PDF with requirements or use an existing one.")
        print("You can test with any PDF containing requirements, specifications, or user stories.")
        return
    
    try:
        # Test with different parameters
        test_cases = [
            {"test_category": "All", "priority_filter": "All"},
            {"test_category": "Frontend", "priority_filter": "High"},
            {"test_category": "Backend", "priority_filter": "All"},
            {"test_category": "Integration", "priority_filter": "Medium"}
        ]
        
        for i, params in enumerate(test_cases):
            print(f"\n--- Test Case {i+1}: {params} ---")
            
            with open(pdf_file_path, 'rb') as pdf_file:
                files = {'file': (pdf_file_path, pdf_file, 'application/pdf')}
                data = {
                    'test_category': params['test_category'],
                    'priority_filter': params['priority_filter']
                }
                
                response = requests.post(f"{BASE_URL}/test-cases/pdf", files=files, data=data)
                
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    test_cases_content = result['test_cases']['content']
                    print(f"✅ Test cases generated successfully!")
                    print(f"Source: {result['test_cases']['source']}")
                    print(f"Filename: {result['test_cases']['filename']}")
                    print(f"Filters applied: {result['test_cases']['filters']}")
                    print(f"Content length: {len(test_cases_content)} characters")
                    print(f"First 300 characters: {test_cases_content[:300]}...")
                else:
                    print(f"❌ Error: {response.status_code}")
                    print(f"Response: {response.text}")
                
                print("-" * 80)
                
    except FileNotFoundError:
        print(f"❌ File '{pdf_file_path}' not found")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_pdf_endpoint_validation():
    """Test PDF endpoint validation with invalid inputs"""
    print("\nTesting PDF endpoint validation...")
    
    # Test 1: No file uploaded
    print("\n--- Test: No file uploaded ---")
    try:
        response = requests.post(f"{BASE_URL}/test-cases/pdf", data={})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Test 2: Invalid file type (text file)
    print("\n--- Test: Invalid file type ---")
    try:
        # Create a temporary text file
        with open("temp_test.txt", "w") as f:
            f.write("This is not a PDF file")
        
        with open("temp_test.txt", 'rb') as txt_file:
            files = {'file': ('test.txt', txt_file, 'text/plain')}
            data = {'test_category': 'All', 'priority_filter': 'All'}
            
            response = requests.post(f"{BASE_URL}/test-cases/pdf", files=files, data=data)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        
        # Clean up
        Path("temp_test.txt").unlink()
        
    except Exception as e:
        print(f"Error: {str(e)}")

def create_sample_pdf_instructions():
    """Provide instructions for creating a sample PDF"""
    print("\n" + "="*80)
    print("SAMPLE PDF CREATION INSTRUCTIONS")
    print("="*80)
    print("""
To test the PDF endpoint, you need a PDF file with requirements or specifications.
You can create one by:

1. Creating a document with sample requirements like:
   ---
   User Authentication System Requirements
   
   1. User Registration
   - Users should be able to register with email and password
   - Email validation is required
   - Password must be at least 8 characters
   
   2. User Login
   - Users should be able to login with email/password
   - Failed login attempts should be tracked
   - Account lockout after 5 failed attempts
   
   3. Password Reset
   - Users should be able to reset password via email
   - Reset links should expire after 24 hours
   ---

2. Save it as a PDF named 'sample_requirements.pdf' in the current directory

3. Run this test script again

Alternatively, you can use any existing PDF with requirements or specifications.
""")

def test_agents_list():
    """Test that the new PDF agent appears in the agents list"""
    print("\nTesting agents list to verify PDF agent is included...")
    try:
        response = requests.get(f"{BASE_URL}/agents")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            agents = response.json()['agents']
            pdf_agent = next((agent for agent in agents if 'PDF' in agent['name']), None)
            
            if pdf_agent:
                print("✅ PDF agent found in agents list:")
                print(json.dumps(pdf_agent, indent=2))
            else:
                print("❌ PDF agent not found in agents list")
        else:
            print(f"❌ Error getting agents list: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("AI Testing Agents - PDF Endpoint Test Suite")
    print("=" * 50)
    
    # Test agents list first
    test_agents_list()
    
    # Test PDF endpoint validation
    test_pdf_endpoint_validation()
    
    # Test with sample PDF if available
    test_pdf_endpoint_with_sample()
    
    # Provide instructions for creating sample PDF
    create_sample_pdf_instructions()
    
    print("\nPDF endpoint tests completed!")

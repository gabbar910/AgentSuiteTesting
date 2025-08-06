import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

class TestCaseGenAgentWrapper:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3)
        
        self.prompt_template = """
You are a test case generation specialist. I will provide you with user stories or requirements, and you will generate comprehensive test cases covering frontend, backend, and integration scenarios.

### Instructions
1. Analyze the provided user stories/requirements
2. Identify all testable scenarios including:
    - Happy path scenarios
    - Edge cases and boundary conditions
    - Error handling scenarios
    - Integration points
3. Generate test cases in the following format for each scenario:
    - Test Case ID
    - Test Case Title
    - Test Category (Frontend/Backend/Integration)
    - Priority (High/Medium/Low)
    - Preconditions
    - Test Steps
    - Expected Results
    - Test Data Requirements
4. Cover the following types of testing:
    - Functional Testing
    - UI/UX Testing
    - API Testing
    - Database Testing
    - Integration Testing
    - Negative Testing
5. Ensure test cases are clear, actionable, and cover all acceptance criteria

### User Stories/Requirements:
{user_stories}
"""

    def run(self, user_stories_text: str) -> str:
        prompt = self.prompt_template.format(user_stories=user_stories_text)
        return self.llm.invoke(prompt)

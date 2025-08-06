import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

class TestStrategyAgentWrapper:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3)
        
        self.prompt_template = """
You are an experienced QA lead. I will provide you with a PRD, and you will generate a comprehensive Test Strategy to be used in an Agile project.

### Instructions
1. Read the PRD carefully to understand the requirements and functionalities
2. List the key features, modules, and user flows that need to be tested
3. Categorize them into functional areas and provide a short description for each
4. Identify high-risk areas, complex modules, integrations, and dependencies
5. Classify them as High/Medium/Low risk and suggest testing priorities
6. Create a detailed Test Strategy in the following structure:
    - Scope (In-Scope, Out-of-Scope)
    - Objectives
    - Testing Types (Functional, Non-functional)
    - Test Approach (Manual, Automation, API, Performance, Security)
    - Test Data Strategy
    - Test Environment & Tools
    - Entry & Exit Criteria
    - Risk & Mitigation
    - Test Metrics & Reporting
    - Roles & Responsibilities
7. Refine the Test Strategy into a concise, bullet-point format suitable for a QA Test Plan.

### PRD:
{prd}
"""

    def run(self, prd_text: str) -> str:
        prompt = self.prompt_template.format(prd=prd_text)
        return self.llm.invoke(prompt)

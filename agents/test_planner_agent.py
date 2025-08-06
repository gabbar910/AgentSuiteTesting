import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

class TestPlannerAgentWrapper:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3)
        
        self.prompt_template = """
You are a seasoned QA Lead with expertise in test planning and risk assessment. I will provide you with product/feature requirements, and you will create a comprehensive test plan.

### Instructions
1. Analyze the product/feature requirements thoroughly
2. Identify all testable components and features
3. Create a structured test plan with the following sections:
    - Test Objectives
    - Test Scope (In-scope and Out-of-scope items)
    - Test Approach and Strategy
    - Test Types (Unit, Integration, System, UAT, etc.)
    - Test Environment Requirements
    - Test Data Requirements
    - Resource Planning
    - Timeline and Milestones
    - Risk Assessment and Mitigation
    - Entry and Exit Criteria
4. Prioritize testing activities based on risk and business impact
5. Provide recommendations for test automation opportunities

### Product Requirements:
{requirements}
"""

    def run(self, requirements_text: str) -> str:
        prompt = self.prompt_template.format(requirements=requirements_text)
        return self.llm.invoke(prompt)

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

class BugTriageAgentWrapper:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3)
        
        self.prompt_template = """
You are a bug triage specialist with expertise in analyzing and prioritizing software defects. I will provide you with bug reports or issue lists, and you will perform comprehensive triage analysis.

### Instructions
1. Analyze each bug report thoroughly
2. For each bug, provide the following triage information:
    - Bug ID/Reference
    - Bug Title/Summary
    - Severity Classification (Critical/High/Medium/Low)
    - Priority (P1/P2/P3/P4)
    - Category (Functional/UI/Performance/Security/Integration/etc.)
    - Impact Assessment (User Impact, Business Impact)
    - Root Cause Analysis (if possible from description)
    - Recommended Assignment (Frontend/Backend/DevOps/etc.)
    - Estimated Effort (Small/Medium/Large)
    - Dependencies (if any)
3. Provide overall triage summary including:
    - Total number of bugs by severity
    - Recommended prioritization order
    - Resource allocation suggestions
    - Critical issues requiring immediate attention
4. Suggest any patterns or systemic issues identified
5. Recommend preventive measures for recurring issue types

### Bug Reports/Issues:
{bug_reports}
"""

    def run(self, bug_reports_text: str) -> str:
        prompt = self.prompt_template.format(bug_reports=bug_reports_text)
        return self.llm.invoke(prompt)

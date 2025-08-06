from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
from agents.test_strategy_agent import TestStrategyAgentWrapper
from agents.test_planner_agent import TestPlannerAgentWrapper
from agents.test_case_gen_agent import TestCaseGenAgentWrapper
from agents.test_case_gen_agent_doc import TestCaseGenDocAgentWrapper
from agents.bug_triage_agent import BugTriageAgentWrapper

router = APIRouter()

# Input models
class PRDInput(BaseModel):
    prd_text: str

class RequirementsInput(BaseModel):
    requirements_text: str

class UserStoriesInput(BaseModel):
    user_stories_text: str

class BugReportsInput(BaseModel):
    bug_reports_text: str

# Initialize agent wrappers
test_strategy = TestStrategyAgentWrapper()
test_planner = TestPlannerAgentWrapper()
test_case_gen = TestCaseGenAgentWrapper()
test_case_gen_doc = TestCaseGenDocAgentWrapper()
bug_triage = BugTriageAgentWrapper()

@router.post("/test-strategy")
def generate_test_strategy(input: PRDInput):
    """Generate a comprehensive test strategy from PRD text"""
    try:
        result = test_strategy.run(input.prd_text)
        return {"strategy": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-plan")
def generate_test_plan(input: RequirementsInput):
    """Create a comprehensive test plan from product requirements"""
    try:
        result = test_planner.run(input.requirements_text)
        return {"test_plan": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-cases")
def generate_test_cases(input: UserStoriesInput):
    """Generate test cases from user stories or requirements"""
    try:
        result = test_case_gen.run(input.user_stories_text)
        return {"test_cases": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-cases/pdf")
async def generate_test_cases_from_pdf(
    file: UploadFile = File(..., description="PDF file containing requirements or specifications"),
    test_category: Optional[str] = Form("All", description="Filter by test category (Frontend/Backend/Integration/API/Database/All)"),
    priority_filter: Optional[str] = Form("All", description="Filter by priority (High/Medium/Low/All)")
):
    """Generate comprehensive test cases from uploaded PDF document"""
    try:
        result = test_case_gen_doc.process_pdf(file, test_category, priority_filter)
        return {
            "test_cases": {
                "content": result,
                "source": "PDF Document",
                "filename": file.filename,
                "filters": {
                    "test_category": test_category,
                    "priority_filter": priority_filter
                }
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@router.post("/bug-triage")
def perform_bug_triage(input: BugReportsInput):
    """Analyze and prioritize bugs from issue lists or JIRA exports"""
    try:
        result = bug_triage.run(input.bug_reports_text)
        return {"triage_analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "AI Testing Agents API is running"}

@router.get("/agents")
def list_agents():
    """List all available agents and their endpoints"""
    return {
        "agents": [
            {
                "name": "Test Strategy Agent",
                "endpoint": "/test-strategy",
                "description": "Generate comprehensive test strategies from PRD text",
                "input_field": "prd_text",
                "input_type": "text"
            },
            {
                "name": "Test Planner Agent",
                "endpoint": "/test-plan",
                "description": "Create comprehensive test plans from product requirements",
                "input_field": "requirements_text",
                "input_type": "text"
            },
            {
                "name": "Test Case Generator Agent",
                "endpoint": "/test-cases",
                "description": "Generate test cases from user stories or requirements",
                "input_field": "user_stories_text",
                "input_type": "text"
            },
            {
                "name": "Test Case Generator (PDF) Agent",
                "endpoint": "/test-cases/pdf",
                "description": "Generate comprehensive test cases from uploaded PDF documents containing requirements or specifications",
                "input_field": "file",
                "input_type": "file",
                "supported_formats": ["PDF"],
                "optional_parameters": {
                    "test_category": "Filter by test category (Frontend/Backend/Integration/API/Database/All)",
                    "priority_filter": "Filter by priority (High/Medium/Low/All)"
                }
            },
            {
                "name": "Bug Triage Agent",
                "endpoint": "/bug-triage",
                "description": "Analyze and prioritize bugs from issue lists or JIRA exports",
                "input_field": "bug_reports_text",
                "input_type": "text"
            }
        ]
    }

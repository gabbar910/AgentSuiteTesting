from crewai import Task

def create_test_strategy_task(agent, prd_text: str):
    """Create a task for generating test strategy from PRD"""
    return Task(
        description=f"""
        Analyze the provided PRD and generate a comprehensive test strategy.
        
        PRD Content:
        {prd_text}
        
        Generate a detailed test strategy that includes:
        1. Test scope and objectives
        2. Risk assessment and mitigation
        3. Testing approach and methodologies
        4. Resource requirements
        5. Timeline and deliverables
        """,
        agent=agent,
        expected_output="A comprehensive test strategy document with all required sections"
    )

def create_test_plan_task(agent, requirements_text: str):
    """Create a task for generating test plan from requirements"""
    return Task(
        description=f"""
        Create a comprehensive test plan based on the provided requirements.
        
        Requirements:
        {requirements_text}
        
        Generate a detailed test plan that includes:
        1. Test objectives and scope
        2. Test approach and strategy
        3. Test types and levels
        4. Test environment and data requirements
        5. Entry and exit criteria
        6. Risk assessment
        """,
        agent=agent,
        expected_output="A detailed test plan document with all necessary sections"
    )

def create_test_cases_task(agent, user_stories_text: str):
    """Create a task for generating test cases from user stories"""
    return Task(
        description=f"""
        Generate comprehensive test cases based on the provided user stories.
        
        User Stories:
        {user_stories_text}
        
        Create test cases that cover:
        1. Functional testing scenarios
        2. Edge cases and boundary conditions
        3. Error handling scenarios
        4. Integration testing
        5. UI/UX testing
        6. API testing where applicable
        """,
        agent=agent,
        expected_output="A comprehensive set of test cases with detailed steps and expected results"
    )

def create_bug_triage_task(agent, bug_reports_text: str):
    """Create a task for bug triage analysis"""
    return Task(
        description=f"""
        Perform comprehensive bug triage analysis on the provided bug reports.
        
        Bug Reports:
        {bug_reports_text}
        
        Analyze and provide:
        1. Severity and priority classification
        2. Impact assessment
        3. Root cause analysis
        4. Assignment recommendations
        5. Resolution timeline estimates
        6. Pattern identification
        """,
        agent=agent,
        expected_output="A detailed triage analysis with prioritized bug list and recommendations"
    )

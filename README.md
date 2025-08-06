# AI Testing Agents API

A FastAPI service that exposes AI agents for testing-related tasks using CrewAI and OpenAI. This project provides a set of specialized agents that can help with various aspects of software testing and quality assurance.

## Features

- **Test Strategy Agent**: Generate comprehensive test strategies from Product Requirements Documents (PRDs)
- **Test Planner Agent**: Create detailed test plans from product requirements
- **Test Case Generator Agent**: Generate test cases from user stories or requirements
- **Bug Triage Agent**: Analyze and prioritize bugs from issue lists or JIRA exports

## Project Structure

```
test-agent-suite/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (OpenAI API key)
├── README.md              # Project documentation
├── agents/                # AI agent implementations
│   ├── __init__.py
│   ├── test_strategy_agent.py
│   ├── test_planner_agent.py
│   ├── test_case_gen_agent.py
│   └── bug_triage_agent.py
├── api/                   # FastAPI routes and models
│   ├── __init__.py
│   └── routes.py
└── tasks/                 # CrewAI task definitions
    ├── __init__.py
    └── task_definitions.py
```

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd test-agent-suite
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv myenv
   # On Windows
   myenv\Scripts\activate
   # On macOS/Linux
   source myenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the application**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Available Endpoints

#### 1. Test Strategy Generation
- **Endpoint**: `POST /test-strategy`
- **Description**: Generate a comprehensive test strategy from PRD text
- **Request Body**:
  ```json
  {
    "prd_text": "Your PRD content here..."
  }
  ```
- **Response**:
  ```json
  {
    "strategy": "Generated test strategy..."
  }
  ```

#### 2. Test Plan Generation
- **Endpoint**: `POST /test-plan`
- **Description**: Create a comprehensive test plan from product requirements
- **Request Body**:
  ```json
  {
    "requirements_text": "Your requirements here..."
  }
  ```
- **Response**:
  ```json
  {
    "test_plan": "Generated test plan..."
  }
  ```

#### 3. Test Case Generation
- **Endpoint**: `POST /test-cases`
- **Description**: Generate test cases from user stories or requirements
- **Request Body**:
  ```json
  {
    "user_stories_text": "Your user stories here..."
  }
  ```
- **Response**:
  ```json
  {
    "test_cases": "Generated test cases..."
  }
  ```

#### 4. Bug Triage Analysis
- **Endpoint**: `POST /bug-triage`
- **Description**: Analyze and prioritize bugs from issue lists
- **Request Body**:
  ```json
  {
    "bug_reports_text": "Your bug reports here..."
  }
  ```
- **Response**:
  ```json
  {
    "triage_analysis": "Bug triage analysis..."
  }
  ```

#### 5. Health Check
- **Endpoint**: `GET /health`
- **Description**: Check API health status

#### 6. List Agents
- **Endpoint**: `GET /agents`
- **Description**: Get information about all available agents

### API Documentation

Once the server is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Usage Examples

### Using curl

```bash
# Test Strategy Generation
curl -X POST "http://localhost:8000/test-strategy" \
     -H "Content-Type: application/json" \
     -d '{"prd_text": "Build a user authentication system with login, registration, and password reset functionality."}'

# Test Plan Generation
curl -X POST "http://localhost:8000/test-plan" \
     -H "Content-Type: application/json" \
     -d '{"requirements_text": "The system should allow users to create accounts, login securely, and manage their profiles."}'

# Test Case Generation
curl -X POST "http://localhost:8000/test-cases" \
     -H "Content-Type: application/json" \
     -d '{"user_stories_text": "As a user, I want to be able to login to my account so that I can access my personal dashboard."}'

# Bug Triage
curl -X POST "http://localhost:8000/bug-triage" \
     -H "Content-Type: application/json" \
     -d '{"bug_reports_text": "Bug 1: Login page crashes when invalid email is entered. Bug 2: Password reset email not being sent."}'
```

### Using Python requests

```python
import requests

# Test Strategy Generation
response = requests.post(
    "http://localhost:8000/test-strategy",
    json={"prd_text": "Your PRD content here..."}
)
print(response.json())
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Model Configuration

The agents are configured to use GPT-4 with a temperature of 0.3 for consistent and focused responses. You can modify the model settings in each agent's wrapper class.

## Development

### Adding New Agents

1. Create a new agent file in the `agents/` directory
2. Implement the agent wrapper class following the existing pattern
3. Add the import to `agents/__init__.py`
4. Create corresponding API endpoints in `api/routes.py`
5. Add task definitions in `tasks/task_definitions.py` if needed

### Testing

You can test the API using the built-in FastAPI documentation at `/docs` or by making HTTP requests to the endpoints.

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**: Ensure your `.env` file contains a valid OpenAI API key
2. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
3. **Port Already in Use**: Change the port in `main.py` or kill the process using port 8000

### Logs

The application provides verbose logging for debugging. Check the console output for detailed information about agent execution.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

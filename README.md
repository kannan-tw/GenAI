# GenAI - AI-Powered Software Development Lifecycle Automation

A comprehensive collection of AI applications demonstrating automated SDLC processes, multi-agent systems, and intelligent code analysis using LangGraph, FastAPI, and Streamlit.

## 🚀 Overview

This repository showcases practical implementations of AI agents for software development automation, including:

- **SDLC Automation**: End-to-end automation from requirements gathering to deployment
- **Code Analysis**: Neo4j-powered semantic code understanding and querying
- **Multi-Agent Systems**: Collaborative AI agents for complex task orchestration
- **Task Management**: Full-stack applications with modern web technologies

## 🏗️ Project Structure

```
GenAI/
├── chat-with-codebase/          # Neo4j-powered code analysis system
├── copilot/daily-tasks-app/     # Full-stack task management application
├── sdlc-automation-blogs/       # SDLC automation workflows
├── Traveller_App/               # Multi-agent travel planning system
├── Docs/                        # Documentation
└── .vscode/                     # VS Code configuration with MCP
```

## 🔧 Core Components

### 1. Chat with Codebase
**Location**: `chat-with-codebase/`

AI-powered code analysis system that ingests codebases into Neo4j and enables natural language querying.

**Features**:
- Code hierarchy extraction and parsing
- Neo4j graph database storage
- LangGraph-based query processing
- Natural language to Cypher translation

**Key Files**:
- `api.py` - FastAPI endpoints for code ingestion and querying
- `lg_neo4j.py` - LangGraph workflow for query processing
- `neo4j_lib.py` - Neo4j database operations

### 2. Daily Tasks App
**Location**: `copilot/daily-tasks-app/`

Modern full-stack task management application demonstrating best practices.

**Architecture**:
- **Backend**: FastAPI with SQLAlchemy ORM
- **Frontend**: Streamlit interactive UI
- **Database**: SQLite for development

**Setup**:
```bash
# Backend
cd copilot/daily-tasks-app/backend
pip install -r requirements.txt
uvicorn app:app --reload

# Frontend
cd ../frontend
pip install -r requirements.txt
streamlit run app.py
```

### 3. SDLC Automation
**Location**: `sdlc-automation-blogs/`

Complete automation of software development lifecycle using AI agents.

**Workflow**:
1. **Requirements Gathering** → SRS generation
2. **High-Level Design** → Architecture documentation
3. **Coding** → Microservice implementation
4. **Testing** → Test case generation
5. **Deployment** → Infrastructure as Code

**Key Notebooks**:
- `requirement_gathering.ipynb` - Requirements to SRS automation
- `hld/HLDv1.0.ipynb` - Architecture design generation
- `coding/Coding.ipynb` - Code generation workflows
- `deployment/Deployment v1.0.ipynb` - IaC script generation

### 4. Traveller App
**Location**: `Traveller_App/`

Multi-agent system for travel planning with JSON-RPC communication.

**Components**:
- `aggregator_app/` - Main orchestration agent
- `flight_app/` - Flight booking specialist
- `hotel_app/` - Accommodation specialist

**Features**:
- Agent-to-agent communication via JSON-RPC 2.0
- Service discovery with agent cards
- Streamlit UIs for each service

## 🛠️ Technology Stack

- **AI/ML**: LangGraph, LangChain, OpenAI GPT models
- **Backend**: FastAPI, Pydantic, SQLAlchemy
- **Frontend**: Streamlit
- **Database**: Neo4j, SQLite, PostgreSQL
- **Infrastructure**: Terraform, Ansible
- **Integration**: Azure DevOps (via MCP)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Neo4j (for code analysis features)
- OpenAI API key

### Environment Setup
```bash
# Clone the repository
git clone https://github.com/kannan-tw/GenAI.git
cd GenAI

# Set up environment variables
export OPENAI_API_KEY="your-api-key"
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your-password"
export MODEL_NAME="gpt-4o-mini"
```

### Running Applications

**Chat with Codebase**:
```bash
cd chat-with-codebase
pip install -r requirements.txt
uvicorn api:app --reload --port 8000
```

**Daily Tasks App**:
```bash
# Backend
cd copilot/daily-tasks-app/backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8001

# Frontend (new terminal)
cd copilot/daily-tasks-app/frontend
streamlit run app.py --server.port 8501
```

**SDLC Automation**:
```bash
cd sdlc-automation-blogs
jupyter notebook
# Open and run the desired automation notebooks
```

## 🔧 Development Patterns

### LangGraph Workflows
```python
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

class State(TypedDict):
    messages: Annotated[list, add_messages]
    max_iteration: int
    iteration: int

workflow = StateGraph(State)
workflow.add_node("agent_name", agent_function)
workflow.add_conditional_edges("node", condition_func, {"option": "target"})
```

### FastAPI + Streamlit Architecture
- Backend: FastAPI with Pydantic models and CORS middleware
- Frontend: Streamlit with session state management
- Communication: HTTP/JSON-RPC for service interaction

### Multi-Agent Communication
- JSON-RPC 2.0 for standardized agent communication
- Agent discovery via `/.well-known/agent.json` endpoints
- State persistence using LangGraph checkpointers

## 🔗 Azure DevOps Integration

This project includes Azure DevOps integration via Model Context Protocol (MCP):

```json
{
  "servers": {
    "ado": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@azure-devops/mcp@next", "${input:ado_org}"]
    }
  }
}
```

## 📚 Documentation

- **Architecture Decisions**: See `sdlc-automation-blogs/hld/output/`
- **API Documentation**: Available at `/docs` endpoint for each FastAPI service
- **Code Examples**: Comprehensive examples in each component directory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the established patterns (see `.github/copilot-instructions.md`)
4. Submit a pull request

## 📄 License

This project is for educational and demonstration purposes. Please see individual component licenses where applicable.

## 🔍 Key Features Showcase

- **Intelligent Code Analysis**: Parse and query codebases using natural language
- **Automated Documentation**: Generate comprehensive technical documentation
- **Multi-Agent Orchestration**: Coordinate multiple AI agents for complex tasks
- **Full-Stack Applications**: Modern web applications with AI integration
- **Infrastructure Automation**: Generate deployment scripts and configurations

---

**Note**: This is a demonstration project showcasing AI-powered development workflows. Adapt the patterns and implementations to your specific use cases.
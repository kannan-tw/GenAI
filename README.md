# GenAI - AI-Powered Software Development Lifecycle Automation

<p align="left">
  <a href="https://www.python.org/downloads/" target="_blank"><img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://platform.openai.com/" target="_blank"><img src="https://img.shields.io/badge/OpenAI-API-412991?logo=openai&logoColor=white" alt="OpenAI API"></a>
  <a href="https://neo4j.com" target="_blank"><img src="https://img.shields.io/badge/Graph-NEO4J-008CC1?logo=neo4j&logoColor=white" alt="Neo4j"></a>
  <a href="#-azure-devops-integration"><img src="https://img.shields.io/badge/Azure%20DevOps-MCP%20Integration-0078D7?logo=azuredevops&logoColor=white" alt="Azure DevOps MCP"></a>
  <img src="https://img.shields.io/badge/Status-Experimental-orange" alt="Project Status" />
</p>

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

## 🧩 High-Level Architecture

```mermaid
flowchart LR
  subgraph SDLC[SDLC Automation Notebooks]
    R[Requirements Notebook]
    H[HLD Notebook]
    C[Code Gen Notebook]
    D[Deployment Notebook]
  end

  subgraph CodeAnalysis[Chat With Codebase]
    Ingest[Ingestion API]
    LG[LangGraph Workflow]
    CY[Cypher Generator]
  end

  subgraph GraphDB[Neo4j]
    G[(Code Graph)]
  end

  subgraph Tasks[Daily Tasks App]
    BE[FastAPI Backend]
    FE[Streamlit Frontend]
    DB[(SQLite)]
  end

  subgraph Travel[Traveller App]
    Agg[Aggregator Agent]
    Flight[Flight Agent]
    Hotel[Hotel Agent]
  end

  DevUser([Developer / User]) -->|prompts & inputs| SDLC
  SDLC -->|generated artifacts| CodeAnalysis
  Ingest --> G
  FE --> BE
  DevUser --> FE
  DevUser --> Agg
  Agg --> Flight
  Agg --> Hotel

  SDLC -->|deployment scripts| DevOps[(Terraform / Ansible)]
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
### 2. Daily Tasks App
**Location**: `copilot/daily-tasks-app/`

Modern full-stack task management application demonstrating best practices.

**Architecture**:
- **Backend**: FastAPI with SQLAlchemy ORM
**Setup**:
```bash
uvicorn app:app --reload

# Frontend
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

## � Environment Variables

| Name | Required | Default | Used By | Description |
|------|----------|---------|---------|-------------|
| `OPENAI_API_KEY` | Yes | — | All AI workflows | OpenAI model access token |
| `MODEL_NAME` | No | `gpt-4o-mini` | LangGraph agents | Default LLM model identifier |
| `NEO4J_URI` | For code analysis | `bolt://localhost:7687` | Chat with Codebase | Neo4j connection URI |
| `NEO4J_USER` | For code analysis | `neo4j` | Chat with Codebase | Neo4j username |
| `NEO4J_PASSWORD` | For code analysis | — | Chat with Codebase | Neo4j password |
| `PYTHONPATH` | No | — | Notebooks / tooling | Optional path adjustments |
| `ADO_ORG` | When using ADO MCP | — | Azure DevOps integration | Azure DevOps organization name |

Export (example):
```bash
export OPENAI_API_KEY="sk-..."
export MODEL_NAME="gpt-4o-mini"
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="password"
```

## �🚀 Quick Start

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
cd sdlc-automation-blogs
jupyter notebook
## �️ Service Run Matrix

| Service | Path | Purpose | Start Command | Default Port | Notes |
|---------|------|---------|---------------|--------------|-------|
| Chat with Codebase API | `chat-with-codebase/` | Ingest & query code graph | `uvicorn api:app --reload --port 8000` | 8000 | Requires Neo4j running |
| Daily Tasks Backend | `copilot/daily-tasks-app/backend/` | Task CRUD & persistence | `uvicorn app:app --reload --port 8001` | 8001 | SQLite dev DB |
| Daily Tasks Frontend | `copilot/daily-tasks-app/frontend/` | Task UI (Streamlit) | `streamlit run app.py --server.port 8501` | 8501 | Connects to backend |
| Traveller Aggregator | `Traveller_App/aggregator_app/` | Orchestrates travel agents | `streamlit run ui.py --server.port 8601` | 8601* | Port suggestion (configure) |
| Traveller Flight Agent | `Traveller_App/flight_app/` | Flight domain logic | `streamlit run ui.py --server.port 8602` | 8602* | Independent agent UI |
| Traveller Hotel Agent | `Traveller_App/hotel_app/` | Hotel domain logic | `streamlit run ui.py --server.port 8603` | 8603* | Independent agent UI |
| SDLC Notebooks | `sdlc-automation-blogs/` | Automated SDLC phases | `jupyter notebook` | 8888* | Browser UI |

*Ports marked with * are suggested; adjust as needed to avoid conflicts.

## �🔧 Development Patterns

### LangGraph Workflows
```python
from langgraph.graph import StateGraph
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


| Issue | Symptoms | Resolution |
|-------|----------|------------|
| Neo4j connection fails | `ServiceUnavailable` / cannot connect | Ensure Neo4j running on `NEO4J_URI`, correct credentials, bolt port open |
| Empty Cypher results | Queries return nothing though code exists | Re-run ingestion; confirm language extensions supported; verify capitalization of class/function names |
| OpenAI auth error | 401 / invalid key | Confirm `OPENAI_API_KEY` exported in current shell and not truncated |
| Port already in use | `OSError: [Errno 48] Address already in use` | Change `--port` or terminate existing process (macOS: `lsof -i :8000`) |
| Streamlit auto-reload loop | Continuous reruns | Clear `.streamlit` config; avoid writing large files in working directory during run |
3. How to add a new agent? → Create service module, define LangGraph node functions, register endpoints or JSON-RPC method, document in architecture.
4. How to deploy? → Use generated Terraform & Ansible from deployment notebooks as a baseline; review before production.
5. Is this production-ready? → Marked Experimental; harden security, observability, and testing before production use.

## 🤝 Contributing
We welcome improvements, refactors, and new automation experiments.

5. Run / smoke test affected services

### Commit Conventions
Use conventional style where possible:
`feat: add neo4j ingestion batching`
`fix: correct cypher generation for nested calls`

### PR Checklist
- [ ] Feature / fix explained in description
- [ ] README or notebook updated if behavior user-facing
- [ ] No secrets committed
- [ ] Lint / formatting respected (black / isort if adopted locally)
- [ ] Added small test or manual reproduction steps

### Adding a New Agent or Service
1. Place code under a new directory (e.g., `agents/<name>`)
2. Provide a minimal `README.md` in that directory
3. Expose FastAPI or Streamlit entrypoint
4. Document env vars / ports in main README tables

### Roadmap (Initial)
- Short term: Refine code ingestion performance; add graph schema visualization
- Short term: Add automated test generation & execution harness
- Mid term: Integrate vector store hybrid search option
- Mid term: Add authentication layer for APIs
- Long term: CI/CD with Azure Pipelines & artifact versioning
- Long term: Pluggable model abstraction (Anthropic, Azure OpenAI, local LLMs)

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
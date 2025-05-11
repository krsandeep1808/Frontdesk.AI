# Salon AI Agent - Human-in-the-Loop System

## Overview
A simulated AI agent system for a fictional salon that handles customer inquiries, escalates unknown questions to human supervisors, and automatically updates its knowledge base.

## Features
- AI agent with initial salon knowledge
- Human escalation for unknown questions
- Supervisor web interface
- Automatic knowledge base updates
- Request lifecycle tracking

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/salon-ai-agent.git
cd salon-ai-agent
```

2. Set up Python environment:
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

3. Initialize database:
```bash
python -c "from backend.db import Base, engine; Base.metadata.create_all(bind=engine)"
```

## Usage

1. Start the backend:
```bash
uvicorn backend.app:app --reload
```

2. Start the AI agent (in another terminal):
```bash
python backend/agent.py
```

3. Access supervisor UI at:
```
http://localhost:8000
```

## System Components
- **AI Agent**: Simulates customer calls and handles responses
- **Backend API**: FastAPI server for data management
- **Supervisor UI**: Web interface for handling requests
- **SQLite Database**: Stores requests and knowledge base

## API Endpoints
- `POST /api/help-requests/` - Create help request
- `GET /api/help-requests/` - List requests
- `POST /api/help-requests/{id}/resolve` - Resolve request
- `GET /api/knowledge/` - List knowledge entries

## Configuration
Create `.env` file for:
- Database connection
- Future telephony integration

## Future Enhancements
- Real telephony integration
- Enhanced NLP capabilities
- Customer notification system

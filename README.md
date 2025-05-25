# Betablu

<p align="center">
  <img src="docs/betablu_logo.png" alt="Betablu Logo">
</p>

![License](https://img.shields.io/badge/license-UNLICENSE-blue.svg)
![Docker](https://img.shields.io/badge/docker-supported-green.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![JavaScript](https://img.shields.io/badge/javascript-ES6+-yellow.svg)

## Overview

Betablu is an open-source project aimed at replicating the capabilities of the IntelliAgent AI agent, a groundbreaking general-purpose AI developed by Monica. IntelliAgent is known for its ability to autonomously execute complex tasks—ranging from personalized travel planning to stock analysis—surpassing models like GPT-4 on the GAIA benchmark. Betablu seeks to bring these capabilities to the open-source community using a modular, containerized framework built with Docker, Python, and JavaScript.

This repository provides a starting point for developers and researchers to build, deploy, and experiment with a multi-agent AI system. Our goal is to create a flexible and extensible platform that mirrors IntelliAgent's autonomous task execution while fostering community contributions.

## Features

- **Multi-Agent System**: Collaborative AI agents working together to solve complex tasks.
- **Dockerized Environment**: Easy setup and deployment with containerization.
- **Task Execution**: Supports tasks like travel planning, data analysis, and content generation.
- **Tool Integration**: Web browsing, code execution, and data retrieval capabilities.
- **Modular Design**: Easily extendable with new agents, tools, or features.
- **Community-Driven**: Open to contributions and enhancements.

## Prerequisites

Before you begin, ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/) (version 20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 1.29 or higher)
- [Node.js](https://nodejs.org/) (version 20.18 or higher, for local development)
- [Python](https://python.org/) (version 3.9 or higher, for local development)
- Git (for cloning and contributing)

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/henryalps/OpenManus.git
cd Betablu
```

### 2. Build and Run with Docker
```bash
# Build and start all containers
docker-compose up --build
```

This will launch:
- Backend container with the multi-agent system and integrated tools
- Frontend container serving the Next.js web interface
- FastAPI server for task delegation and execution

### 3. Test the System
Once running, you can interact with Betablu via:
- CLI: Use the provided Python client (`python client.py`)
- API: Send requests to http://localhost:8000 (see API docs below)
- Web UI: Access http://localhost:3000

Example CLI command:
```bash
python client.py --task "Plan a 3-day trip to Tokyo"
```

### Project Structure
```
Betablu/
├── docker/               # Docker configurations
│   ├── frontend/        # Next.js frontend container
│   │   └── Dockerfile   # Frontend container configuration
│   └── unified/         # Backend container configuration
│       ├── Dockerfile   # Backend container configuration
│       └── start.sh     # Container startup script
├── src/                 # Source code
│   ├── agents/          # Multi-agent logic (Python)
│   │   ├── nodes/       # Agent node implementations
│   │   ├── browser_agent.py
│   │   ├── coder_agent.py
│   │   ├── coordinator.py
│   │   ├── reporter_agent.py
│   │   └── research_agent.py
│   ├── components/      # React components
│   ├── config/          # Configuration files
│   ├── graph/           # Graph-based workflow
│   ├── llms/            # LLM integrations
│   ├── pages/           # Next.js pages
│   ├── prompts/         # Agent prompts
│   ├── service/         # Backend services
│   ├── tools/           # Tool implementations
│   ├── utils/           # Utility functions
│   ├── workflow/        # Workflow management
│   ├── client.py        # CLI client for testing
│   └── server.py        # FastAPI server
├── docs/                # Documentation and API specs
├── package.json         # Next.js frontend dependencies
├── next.config.js       # Next.js configuration
├── docker-compose.yml   # Docker Compose configuration
└── README.md           # This file
```

### Configuration
Edit the `docker-compose.yml` file to customize:
```yaml
services:
  backend:
    build: 
      context: .
      dockerfile: docker/unified/Dockerfile
    ports:
      - "8000:8000"  # FastAPI port
    environment:
      - WEB_BROWSER_API_KEY=your_key_here
    volumes:
      - ./src:/app/src
      - ./data:/app/data

  frontend:
    build:
      context: .
      dockerfile: docker/frontend/Dockerfile
    ports:
      - "3000:3000"  # Web UI port
    depends_on:
      - backend
```

### API Documentation
The agent server exposes a REST API at http://localhost:8000. Key endpoints:

**POST /task**: Submit a task for execution.
```json
Body: { "task": "Analyze Tesla stock trends" }
Response: { "status": "success", "result": "..." }
```

**GET /status**: Check system health.
```json
Response: { "status": "running" }
```

Full API docs are available in `docs/api.md`.

### Contributing
We welcome contributions! To get started:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

Please read `CONTRIBUTING.md` for guidelines.

### Roadmap
- Implement core multi-agent coordination.
- Add support for GAIA benchmark tasks.
- Integrate advanced NLP models (e.g., LLaMA, Grok).
- Enhance toolset with real-time web scraping and visualization.
- Release v1.0 with stable task execution.

### Inspiration
Betablu is inspired by:
- The langmanus project (GitHub).
- The official Manus project (manus.im).
- The open-Manus community effort (GitHub).
- GAIA benchmark for general AI assistants (arXiv).

### License
This project is licensed under the UNLICENSE. See `LICENSE` for details.

### Contact
For questions or collaboration, reach out via GitHub Issues or email [contact@betablu.com](mailto:contact@betablu.com).

Happy coding! Let's build the future of AI agents together!
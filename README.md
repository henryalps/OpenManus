# OpenManus

<p align="center">
  <img src="docs/logo.png" alt="OpenManus Logo">
</p>

![License](https://img.shields.io/badge/license-UNLICENSE-blue.svg)
![Docker](https://img.shields.io/badge/docker-supported-green.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![JavaScript](https://img.shields.io/badge/javascript-ES6+-yellow.svg)

## Overview

OpenManus is an open-source project aimed at replicating the capabilities of the Manus AI agent, a groundbreaking general-purpose AI developed by Monica. Manus is known for its ability to autonomously execute complex tasks—ranging from personalized travel planning to stock analysis—surpassing models like GPT-4 on the GAIA benchmark. OpenManus seeks to bring these capabilities to the open-source community using a modular, containerized framework built with Docker, Python, and JavaScript.

This repository provides a starting point for developers and researchers to build, deploy, and experiment with a multi-agent AI system. Our goal is to create a flexible and extensible platform that mirrors Manus's autonomous task execution while fostering community contributions.

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
cd OpenManus
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

### 3. Configure API Keys (Required)

Before you can use OpenManus, you need to configure your LLM API keys. See the [Configuration](#configuration) section below for detailed instructions.

### 4. Test the System
Once configured, you can interact with OpenManus via:
- **CLI**: Use the provided Python client
  ```bash
  python src/client.py --task "Plan a 3-day trip to Tokyo"
  ```
- **Web UI**: Access http://localhost:3000 in your browser
- **API**: Send requests directly to http://localhost:8000 (see API docs below)

Example CLI commands:
```bash
# Simple question
python src/client.py --task "What's the weather like in Tokyo?"

# Complex task
python src/client.py --task "Analyze Tesla stock trends for the last month"
```

### Project Structure
```
OpenManus/
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

#### API Keys Setup (Required for AI functionality)

Create a `.env` file in the project root directory with your LLM API keys:

```env
# Basic LLM (used for most agents)
BASIC_API_KEY=your-openai-api-key-here
BASIC_BASE_URL=https://api.openai.com/v1
BASIC_MODEL=gpt-3.5-turbo

# Reasoning LLM (for complex tasks) - Optional
REASONING_API_KEY=your-deepseek-api-key
REASONING_BASE_URL=https://api.deepseek.com/v1
REASONING_MODEL=deepseek-r1

# Vision-Language LLM (for image tasks) - Optional
VL_API_KEY=your-api-key-here
VL_BASE_URL=https://api.openai.com/v1
VL_MODEL=gpt-4o
```

**Supported LLM Providers:**
- OpenAI (GPT-3.5, GPT-4, GPT-4o)
- DeepSeek (deepseek-r1)
- Google Gemini
- Azure OpenAI
- Any OpenAI-compatible API

After creating the `.env` file, restart the containers:
```bash
docker-compose restart unified
```

#### Docker Compose Configuration

The current `docker-compose.yml` structure:
```yaml
services:
  unified:
    build:
      context: .
      dockerfile: docker/unified/Dockerfile
    ports:
      - "8000:8000"  # FastAPI backend server

  frontend:
    build:
      context: .
      dockerfile: docker/frontend/Dockerfile
    ports:
      - "3000:3000"  # Next.js web interface
    depends_on:
      - unified
```

Environment variables are loaded from the `.env` file automatically.

### API Documentation
The agent server exposes a REST API at http://localhost:8000. Key endpoints:

**POST /api/chat/stream**: Submit a message and receive streaming response.
```bash
curl -X POST http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello, how are you?"}]}'
```

Response format (Server-Sent Events):
```
event: message
data: {"content": "AI response here", "role": "assistant"}
```

**GET /docs**: Interactive API documentation (Swagger UI)
- Access at http://localhost:8000/docs

For more details, see the auto-generated API docs at `/docs` when the server is running.

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
OpenManus is inspired by:
- The langmanus project (GitHub).
- The official Manus project (manus.im).
- The open-Manus community effort (GitHub).
- GAIA benchmark for general AI assistants (arXiv).

### License
This project is licensed under the UNLICENSE. See `LICENSE` for details.

### Contact
For questions or collaboration, reach out via GitHub Issues or email [henryalps@gmail.com](mailto:henryalps@gmail.com).

Happy coding! Let's build the future of AI agents together!

[![Powered by DartNode](https://dartnode.com/branding/DN-Open-Source-sm.png)](https://dartnode.com "Powered by DartNode - Free VPS for Open Source")

CDN acceleration and security protection for this project are sponsored by Tencent EdgeOne.

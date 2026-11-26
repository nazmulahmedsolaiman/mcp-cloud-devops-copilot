# MCP Cloud & DevOps Operations Copilot

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/Model%20Context%20Protocol-MCP-6E40C9?style=flat-square)](https://modelcontextprotocol.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

A **Model Context Protocol (MCP)** powered **Cloud & DevOps Operations Copilot** built with **Python**, **FastAPI**, and **Docker**. It exposes standardized MCP tools for infrastructure health monitoring, least-privilege IAM policy validation, and automated incident runbook execution.

---

## Architecture

```mermaid
flowchart LR
    A[LLM Client / Agent] -->|MCP Tool Call| B[MCP Server & FastAPI Gateway]
    B --> C[check_service_health]
    B --> D[validate_least_privilege_iam]
    B --> E[execute_incident_runbook]
    C --> F[Infrastructure Telemetry]
    D --> G[IAM Policy Evaluator]
    E --> H[Automated Remediation Log]
```

## MCP Tools Exposed

- `check_service_health`: Evaluates CPU, memory, and endpoint latency against production thresholds.
- `validate_least_privilege_iam`: Audits IAM role JSON policies for wildcard actions (`*`) or missing MFA conditions.
- `execute_incident_runbook`: Runs safe, idempotent remediation steps (cache flush, service restart, alert escalation).

## Project Structure

```text
mcp-cloud-devops-copilot/
├── .github/workflows/ci.yml   # Automated pytest CI
├── src/
│   ├── __init__.py
│   ├── config.py              # Threshold & environment settings
│   ├── models.py              # Pydantic request/response schemas
│   ├── mcp_server.py          # MCP tool registry & DevOps handlers
│   └── main.py                # FastAPI + MCP tool router
├── tests/
│   └── test_copilot.py        # Unit tests for MCP DevOps tools
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── LICENSE
└── requirements.txt
```

## Quickstart

### 1. Local Setup
```bash
git clone https://github.com/nazmulahmedsolaiman/mcp-cloud-devops-copilot.git
cd mcp-cloud-devops-copilot
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn src.main:app --reload
```

### 2. Docker Compose
```bash
docker compose up --build
```
Open Swagger UI at `http://localhost:8000/docs`.

## Running Tests
```bash
python -m pytest -v
```

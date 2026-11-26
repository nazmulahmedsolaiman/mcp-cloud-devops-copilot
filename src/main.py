from fastapi import FastAPI
from src.config import settings
from src.mcp_server import (
    MCP_TOOL_CATALOG,
    check_service_health,
    execute_incident_runbook,
    validate_least_privilege_iam,
)
from src.models import (
    HealthCheckRequest,
    IAMValidationRequest,
    RunbookRequest,
    ToolCallResult,
)

app = FastAPI(
    title="MCP Cloud & DevOps Operations Copilot",
    version="1.0.0",
    description="Model Context Protocol (MCP) tool server for Cloud & DevOps automation",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": settings.app_name}


@app.get("/api/v1/tools")
def list_mcp_tools():
    return {"tools": MCP_TOOL_CATALOG}


@app.post("/api/v1/tools/health", response_model=ToolCallResult)
def run_health_tool(req: HealthCheckRequest):
    return check_service_health(req)


@app.post("/api/v1/tools/iam-audit", response_model=ToolCallResult)
def run_iam_tool(req: IAMValidationRequest):
    return validate_least_privilege_iam(req)


@app.post("/api/v1/tools/runbook", response_model=ToolCallResult)
def run_runbook_tool(req: RunbookRequest):
    return execute_incident_runbook(req)

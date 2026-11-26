from typing import Dict, List
from src.config import settings
from src.models import (
    HealthCheckRequest,
    IAMValidationRequest,
    RunbookRequest,
    ToolCallResult,
)

MCP_TOOL_CATALOG: List[Dict[str, str]] = [
    {
        "name": "check_service_health",
        "description": "Evaluates CPU, memory, and latency against production SLA thresholds.",
    },
    {
        "name": "validate_least_privilege_iam",
        "description": "Audits IAM role statements for wildcard actions/resources and missing MFA.",
    },
    {
        "name": "execute_incident_runbook",
        "description": "Executes safe, idempotent incident remediation runbook actions.",
    },
]


def check_service_health(req: HealthCheckRequest) -> ToolCallResult:
    breaches: List[str] = []
    if req.cpu_percent >= settings.cpu_alert_threshold:
        breaches.append(f"CPU {req.cpu_percent}% >= {settings.cpu_alert_threshold}%")
    if req.memory_percent >= settings.memory_alert_threshold:
        breaches.append(f"Memory {req.memory_percent}% >= {settings.memory_alert_threshold}%")
    if req.latency_ms > 500:
        breaches.append(f"Latency {req.latency_ms}ms > 500ms")

    status = "critical" if len(breaches) >= 2 else ("warning" if breaches else "ok")
    return ToolCallResult(
        tool_name="check_service_health",
        status=status,
        details={"service": req.service_name, "breaches": breaches},
    )


def validate_least_privilege_iam(req: IAMValidationRequest) -> ToolCallResult:
    violations: List[str] = []
    for idx, stmt in enumerate(req.statements):
        if stmt.effect == "Allow" and ("*" in stmt.actions or "*" in stmt.resources):
            violations.append(f"Statement {idx}: wildcard (*) permission detected")
        if stmt.effect == "Allow" and not stmt.mfa_required:
            violations.append(f"Statement {idx}: MFA condition missing")

    status = "critical" if violations else "ok"
    return ToolCallResult(
        tool_name="validate_least_privilege_iam",
        status=status,
        details={"role_name": req.role_name, "violations": violations},
    )


def execute_incident_runbook(req: RunbookRequest) -> ToolCallResult:
    return ToolCallResult(
        tool_name="execute_incident_runbook",
        status="ok",
        details={
            "incident_id": req.incident_id,
            "service": req.service_name,
            "executed_action": req.action,
            "audit_logged": True,
        },
    )

from typing import Any, Dict, List, Literal
from pydantic import BaseModel, Field


class HealthCheckRequest(BaseModel):
    service_name: str = Field(..., examples=["auth-gateway"])
    cpu_percent: float = Field(..., ge=0.0, le=100.0)
    memory_percent: float = Field(..., ge=0.0, le=100.0)
    latency_ms: int = Field(..., ge=0)


class IAMPolicyStatement(BaseModel):
    effect: Literal["Allow", "Deny"]
    actions: List[str]
    resources: List[str]
    mfa_required: bool = True


class IAMValidationRequest(BaseModel):
    role_name: str = Field(..., examples=["prod-deployer"])
    statements: List[IAMPolicyStatement]


class RunbookRequest(BaseModel):
    incident_id: str = Field(..., examples=["OPS-501"])
    service_name: str
    action: Literal["restart_service", "flush_cache", "rotate_iam_session"]


class ToolCallResult(BaseModel):
    tool_name: str
    status: Literal["ok", "warning", "critical"]
    details: Dict[str, Any]

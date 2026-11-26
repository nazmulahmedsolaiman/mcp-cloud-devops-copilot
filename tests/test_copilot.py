from src.mcp_server import (
    check_service_health,
    execute_incident_runbook,
    validate_least_privilege_iam,
)
from src.models import (
    HealthCheckRequest,
    IAMPolicyStatement,
    IAMValidationRequest,
    RunbookRequest,
)


def test_health_check_warning():
    res = check_service_health(
        HealthCheckRequest(
            service_name="api-gateway",
            cpu_percent=91.0,
            memory_percent=60.0,
            latency_ms=120,
        )
    )
    assert res.status == "warning"
    assert len(res.details["breaches"]) == 1


def test_iam_wildcard_violation():
    res = validate_least_privilege_iam(
        IAMValidationRequest(
            role_name="admin-role",
            statements=[
                IAMPolicyStatement(
                    effect="Allow",
                    actions=["*"],
                    resources=["arn:aws:s3:::prod-bucket/*"],
                    mfa_required=False,
                )
            ],
        )
    )
    assert res.status == "critical"
    assert len(res.details["violations"]) == 2


def test_runbook_execution():
    res = execute_incident_runbook(
        RunbookRequest(
            incident_id="OPS-99",
            service_name="cache-cluster",
            action="flush_cache",
        )
    )
    assert res.status == "ok"
    assert res.details["audit_logged"] is True

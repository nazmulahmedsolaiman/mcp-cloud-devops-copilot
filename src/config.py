from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "mcp-cloud-devops-copilot"
    log_level: str = "INFO"
    cpu_alert_threshold: float = 85.0
    memory_alert_threshold: float = 85.0

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

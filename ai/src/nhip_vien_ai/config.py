from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="AI_",
        extra="ignore",
    )

    env: str = "development"
    model_provider: str = "rule_based"
    model_version: str = "route-ranker-v1"
    request_timeout_seconds: float = Field(default=5.0, gt=0, le=30)
    governance_policy_path: str = "config/governance-policy.yaml"


@lru_cache
def get_settings() -> Settings:
    return Settings()

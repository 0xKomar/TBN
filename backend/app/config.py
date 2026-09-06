import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "UrbanFlow API"
    app_mode: str = "DEMO"
    frontend_origin: str = "http://localhost:5173"
    live_max_age_seconds: int = 30
    stale_max_age_seconds: int = 90


def get_settings() -> Settings:
    return Settings(
        app_mode=os.getenv("APP_MODE", "DEMO").upper(),
        frontend_origin=os.getenv("FRONTEND_ORIGIN", "http://localhost:5173"),
    )
